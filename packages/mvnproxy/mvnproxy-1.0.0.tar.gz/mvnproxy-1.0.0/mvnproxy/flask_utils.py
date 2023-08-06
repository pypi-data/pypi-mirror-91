import functools
import inspect
from flask import request, jsonify  # type: ignore

from typing import TypeVar, Callable

T = TypeVar("T")


def form_params(f: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator that will read the form parameters for the request.
    The names of the variables are the names that are mapped in the function.
    """
    parameter_names = inspect.getargspec(f).args

    @functools.wraps(f)
    def logic(*args, **kw) -> T:
        params = dict(kw)

        parameter_name: str
        for parameter_name in parameter_names:
            if parameter_name in request.form and parameter_name not in kw:
                params[parameter_name] = request.form.get(parameter_name)

        return f(**params)

    return logic


def form_content(parameter_name: str) -> Callable[..., Callable[..., T]]:
    def wrapper_builder(f: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(f)
        def wrapper(*args, **kw) -> T:
            kw[parameter_name] = "yolo"
            return f(*args, **kw)

        return wrapper

    return wrapper_builder


def query_params(f: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator that will read the query parameters for the request.
    The names are the names that are mapped in the function.
    """
    parameter_names = inspect.getargspec(f).args

    @functools.wraps(f)
    def logic(*args, **kw):
        params = dict(kw)

        parameter_name: str
        for parameter_name in parameter_names:
            if parameter_name in request.args and parameter_name not in kw:
                params[parameter_name] = request.args.get(parameter_name)

        return f(**params)

    return logic


def query_json_params(*parameters: str) -> Callable[..., Callable[..., T]]:
    """
    Decorator that will read the given parameters from the request
    decode them as JSON, and pass them down the stack chain.
    """

    def wrapper(f: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(f)
        def logic(*args, **kw) -> T:
            for parameter_name in parameters:
                if parameter_name in request.args:
                    kw[parameter_name] = request.args.get(parameter_name)
                else:
                    kw[parameter_name] = None

            return f(**kw)

        return logic

    return wrapper


def json_result(f: Callable[..., T]) -> Callable[..., str]:
    """
    Serialize the result of the function as JSON.
    """
    # FIXME: what to do with error results, or results that
    # are already flask based?
    @functools.wraps(f)
    def logic(*args, **kw) -> Callable[..., str]:
        result = f(*args, **kw)

        return jsonify(result)

    return logic
