from random import random
from typing import Tuple, Callable, NoReturn

from finq.typevars import T


def Identity(v: T) -> T:
    return v


def Consumer(_: T) -> NoReturn:
    """
    Consumes given value with no return
    """
    return None


def IdentityTrue(_: T) -> bool:
    """
    Returns True independently of given value
    """
    return True


def IdentityFalse(_: T) -> bool:
    """
    Returns False independently of given value
    """
    return False


def Sum(a: T, b: T) -> T:
    """
    Returns sum of two given value
    """
    return a + b


def PairSum(t: Tuple[T, T]) -> T:
    """
    Returns sum of first two values of Ordered Collection
    """
    return t[0] + t[1]


def First(t):
    """
    Returns first value of Ordered Collection
    """
    return t[0]


def Second(t):
    """
    Returns second value of Ordered Collection
    """
    return t[1]


def Multiply(a: T, b: T) -> T:
    """
    Returns product of two given values
    """
    return a * b


def Square(a: T) -> T:
    """
    Returns square of given value
    """
    return a * a


def OneArgRandom(_: T) -> float:
    """
    Returns random value independent of given value
    """
    return random()


def PairWith(*func: Callable[[T], T]):
    """Returns function that, when applied to value `e` returns `e, f1(f2(...fn(e)...))`"""

    def f(a):
        res = a
        for g in func:
            res = g(res)
        return a, res

    return f


def RPairWith(*func: Callable[[T], T]):
    """Returns function that, when applied to value `e` returns `f1(f2(...fn(e)...)), e`"""

    def f(a):
        res = a
        for g in func:
            res = g(res)
        return res, a

    return f


def TupleSum(t: Tuple) -> T:
    """Returns sum of given Ordered Collection"""
    if len(t) == 0:
        return 0
    tuple_sum = t[0]
    for i in range(1, len(t)):
        tuple_sum += t[i]
    return tuple_sum


def Compose(*func: Callable[[T], T]):
    """Returns function that, when applied to value `e` returns `f1(f2(...fn(e)...))` """

    def h(x):
        res = x
        for f in func:
            res = f(res)
        return res

    return h