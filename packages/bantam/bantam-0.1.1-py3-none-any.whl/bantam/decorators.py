import asyncio
import inspect
import json
import sys
from enum import Enum
from typing import Type, Any, Callable, Awaitable, AsyncIterator, Union, AsyncGenerator, Optional, Dict

from aiohttp.web import Request, Response
from aiohttp.web_response import StreamResponse


WebApi = Callable[..., Awaitable[Any]]


class RestMethod(Enum):
    GET = 'GET'
    POST = 'POST'


AsyncChunkIterator = Callable[[int], Awaitable[AsyncGenerator[None, bytes]]]
AsyncLineIterator = AsyncGenerator[None, str]
PreProcessor = Callable[[Request], Union[None, Dict[str, Any]]]
PostProcessor = Callable[[Union[Response, StreamResponse]], Union[Response, StreamResponse]]


def _convert_request_param(value: str, typ: Type) -> Any:
    """
    Convert rest request string value for parameter to given Python type, returning an instance of that type

    :param value: value to convert
    :param typ: Python Type to convert to
    :return: converted instance, of the given type
    :raises: TypeError if value can not be converted/deserialized
    """
    if hasattr(typ, '_name') and str(typ).startswith('typing.Union'):
        typ = typ.__args__[0]
        return _convert_request_param(value, typ)
    if hasattr(typ, 'deserialize'):
        return typ.deserialize(value)
    elif typ == bool:
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        raise ValueError(f"Expected one of 'true' or 'false' but found {value}")
    try:
        return typ(value)
    except Exception as e:
        raise TypeError(f"Converting web request string to Python type {typ}: {e}")


def _serialize_return_value(value: Any, encoding: str) -> bytes:
    """
    Serialize a Python value into bytes to return through a Rest API.  If a basic type such as str, int or float, a
    simple str conversion is done, then converted to bytes.  If more complex, the conversion will invoke the
    'serialize' method of the value, raising TypeError if such a method does not exist or does not have a bare
    (no-parameter) signature.

    :param value: value to convert
    :return: bytes serialized from value
    """
    if isinstance(value, (str, bool, int, float)):
        return str(value).encode(encoding)
    elif hasattr(value, 'serialize'):
        try:
            image = value.serialize()
        except Exception as e:
            raise TypeError(f"Unable to serialize Python response to string-seralized web response: {e}")
        if not isinstance(image, (str, bytes)):
            raise TypeError(f"Call to serialize {value} of type {type(value)} did not return 'str' as expected")
        if isinstance(image, str):
            return image.encode(encoding)
        return image


async def _invoke_get_api_wrapper(func: WebApi, content_type: str, request: Request, **addl_args: Any)\
        -> Union[Response, StreamResponse]:
    """
    Invoke the underlying GET web API from given request
    :param func:  async function to be called
    :param content_type: http header content-type
    :param request: request to be processed
    :return: http response object
    """
    from .web import WebApplication
    WebApplication._context[sys._getframe(0)] = request
    try:
        encoding = 'utf-8'
        items = content_type.split(';')
        for item in items:
            item = item.lower()
            if item.startswith('charset='):
                encoding = item.replace('charset=', '')
        annotations = dict(func.__annotations__)
        if async_annotations:
            raise TypeError("Cannot specify a parameter to be streamed for GET requests, you must use POST")
        if 'return' in annotations:
            del annotations['return']
        async_annotations = [a for a in annotations.items() if a[1] in (bytes, AsyncChunkIterator, AsyncLineIterator)]
        # report first param that doesn't match the Python signature:
        for k in [p for p in request.query if p not in annotations]:
            return Response(status=400,
                text=f"No such parameter or missing type hint for param {k} in method {func.__qualname__}")

        # convert incoming str values to proper type:
        kwargs = {k: _convert_request_param(v, annotations[k]) for k, v in request.query.items()}
        if addl_args:
            kwargs.update(addl_args)
        # call the underlying function:
        result = func(**kwargs)
        if inspect.isasyncgen(result):
            #################
            #  streamed response through async generator:
            #################
            # underlying function has yielded a result rather than turning
            # process the yielded value and allow execution to resume from yielding task
            content_type = "text-streamed; charset=x-user-defined"
            response = StreamResponse(status=200, reason='OK', headers={'Content-Type': content_type})
            await response.prepare(request)
            try:
                # iterate to get the one (and hopefully only) yielded element:
                async for res in result:
                    serialized = _serialize_return_value(res, encoding)
                    if not isinstance(res, bytes):
                        serialized += b'\n'
                    await response.write(serialized)
            except Exception as e:
                print(str(e))
            await response.write_eof()
            return response
        else:
            #################
            #  regular response
            #################
            result = _serialize_return_value(await result, encoding)
            return Response(status=200, body=result if result is not None else b"Success",
                            content_type=content_type)
    except TypeError as e:
        return Response(status=400, text=f"Improperly formatted query: {str(e)}")
    except Exception as e:
        return Response(status=500, text=str(e))
    finally:
        del WebApplication._context[sys._getframe(0)]


async def _invoke_post_api_wrapper(func: WebApi, content_type: str, request: Request, **addl_args: Any) -> Response:
    """
    Invoke the underlying POST web API from given request
    :param func:  async function to be called
    :param content_type: http header content-type
    :param request: request to be processed
    :return: http response object
    """
    from .web import  WebApplication
    WebApplication._context[sys._getframe(0)] = request
    encoding = 'utf-8'
    items = content_type.split(';')
    for item in items:
        if item.startswith('charset='):
            encoding = item.replace('charset=', '')
    if not request.can_read_body:
        raise TypeError("Cannot read body for request in POST operation")

    annotations = dict(func.__annotations__)
    if 'return' in annotations:
        del annotations['return']
    try:
        kwargs = None
        async_annotations = [a for a in annotations.items() if a[1] in (bytes, AsyncChunkIterator, AsyncLineIterator)]
        if async_annotations:
            if not len(async_annotations) == 1:
                raise ValueError("At most one parameter of holding onf of the types: bytes, AsyncChunkGenerator or AsynLineGenerator is allowed")
            key, typ = async_annotations[0]
            if typ == bytes:
                kwargs = {key: await request.read()}
            elif typ == AsyncLineIterator:
                async def iterator():
                    reader = request.content
                    while not reader.is_eof:
                        yield await reader.readline()
                kwargs = {key: iterator()}
            elif typ == AsyncChunkIterator:
                async def iterator(packet_size: int):
                    reader = request.content
                    while not reader.is_eof:
                        yield await reader.read(packet_size)
                kwargs = {key: iterator}
            kwargs.update({k: _convert_request_param(v, annotations[k]) for k, v in request.query.items()})
        else:
            # treat payload as json string:
            bytes_response = await request.read()
            json_dict = json.loads(bytes_response.decode('utf-8'))
            for k in [p for p in json_dict if p not in annotations]:
                return Response(status=400,
                    text=f"No such parameter or missing type hint for param {k} in method {func.__qualname__}")

            # convert incoming str values to proper type:
            kwargs = dict(json_dict)
            # kwargs = {k: _convert_request_param(v, annotations[k]) for k, v in json_dict.items()}
        # call the underlying function:
        if addl_args:
            kwargs.update(addl_args)
        awaitable = func(**kwargs)
        if inspect.isasyncgen(awaitable):
            #################
            #  streamed response through async generator:
            #################
            # underlying function has yielded a result rather than turning
            # process the yielded value and allow execution to resume from yielding task
            async_q = asyncio.Queue()
            content_type = "text/streamed; charset=x-user-defined"
            response = StreamResponse(status=200, reason='OK', headers={'Content-Type': content_type})
            await response.prepare(request)
            try:
                # iterate to get the one (and hopefully only) yielded element:
                async for res in awaitable:
                    serialized = _serialize_return_value(res, encoding)
                    if not isinstance(res, bytes):
                        serialized += b'\n'
                    await response.write(serialized)
            except Exception as e:
                print(str(e))
                await async_q.put(None)
            await response.write_eof()
        else:
            #################
            #  regular response
            #################
            from .web import WebApplication
            result = _serialize_return_value(await awaitable, encoding)
            return Response(status=200, body=result if result is not None else b"Success",
                            content_type=content_type)

    except TypeError as e:
        return Response(status=400, text=f"Improperly formatted query: {str(e)}")
    except Exception as e:
        return Response(status=500, text=str(e))
    finally:
        del WebApplication._context[sys._getframe(0)]


def web_api(content_type: str, method: RestMethod = RestMethod.GET,
            preprocess: Optional[PreProcessor] = None,
            postprocess: Optional[PostProcessor] = None) -> Callable[[WebApi], WebApi]:
    """
    Decorator for class async method to register it as an API with the `WebApplication` class
    Decorated functions should be static class methods with parameters that are convertible from a string
    (things like float, int, str, bool).  Type hints must be provided and will be used to dynamically convert
    query parameeter strings to the right type.

    >>> class MyResource:
    ...
    ...   @web_api(content_type="text/html")
    ...   @staticmethod
    ...   def say_hello(name: str):
    ...      return f"Hi there, {name}!"

    Only GET calls with explicit parameters in the URL are support for now.  The above registers a route
    of the form:

    http://<host>:port>/MyRestAPI?name=Jill


    :param content_type: content type to disply (e.g., "text/html")
    :param method: one of MethodEnum rest api methods (GET or POST)
    :return: callable decorator
    """
    from .web import WebApplication
    if not isinstance(content_type, str):
        raise Exception("@web_api must be provided one str argument which is the content type")

    def wrapper(func: WebApi) -> WebApi:
        if not isinstance(func, staticmethod):
            raise ValueError("the @web_api decorator can only be used on static class methods")
        elif not inspect.iscoroutinefunction(func.__func__) and not inspect.isasyncgenfunction(func.__func__):
            raise ValueError("the @web_api decorator can only be applied to methods that are coroutines (async)")
        func = func.__func__
        name = func.__qualname__
        name_parts = name.split('.')[-2:]
        route = '/' + '/'.join(name_parts)

        async def invoke(app: WebApplication, request: Request):
            nonlocal preprocess, postprocess
            try:
                preprocess = preprocess or app.preprocessor
                try:
                    addl_args = (preprocess(request) or {}) if preprocess else {}
                except Exception as e:
                    return Response(status=400, text=f"Error in preprocessing request: {e}")
                if method == RestMethod.GET:
                    response = await _invoke_get_api_wrapper(func, content_type=content_type, request=request,
                                                             **addl_args)
                elif method == RestMethod.POST:
                    response = await _invoke_post_api_wrapper(func, content_type=content_type, request=request,
                                                              **addl_args)
                else:
                    raise ValueError(f"Unknown method {method} in @web-api")
                try:
                    postprocess = postprocess or app.postprocessor
                    postprocess(response) if postprocess else response
                except Exception as e:
                    return Response(status=400, text=f"Error in post-processing of response: {e}")
                return response
            except Exception as e:
                return Response(status=500, text=f"Server error: {e}")

        if method == RestMethod.GET:
            WebApplication.register_route_get(route, invoke, func, content_type)
        elif method == RestMethod.POST:
            WebApplication.register_route_post(route, invoke, func, content_type)
        else:
            raise ValueError(f"Unknown method {method} in @web-api")
        return func
    return wrapper
