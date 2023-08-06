import inspect
from logging import getLogger
from typing import Callable

from .rewrite_source_code import rewrite_source_code

logger = getLogger('verbosify')


def exception_error_message(func_name: str, e: Exception) -> str:
    return f"""
The following error has occurred wile verbosifying '{func_name}' function:
>>> {e}
The function was return unverbosified.
"""


def verbosify(func: Callable, verbose_word: str = ' verbose: ') -> Callable:
    if not inspect.isfunction(func):
        raise TypeError('verbosify can only be applied to a function')

    try:
        source_code = inspect.getsource(func)
        source_code = rewrite_source_code(source_code, verbose_word)
        exec(source_code)
        return locals()[func.__name__]

    except Exception as e:
        logger.warning(exception_error_message(func.__name__, e))
        return func


def verbosify_with(verbose_word: str) -> Callable:
    return lambda func: verbosify(func, verbose_word)
