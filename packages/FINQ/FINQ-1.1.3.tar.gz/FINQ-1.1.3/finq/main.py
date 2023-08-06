from collections import defaultdict, Counter
from random import random
from typing import Iterable, Callable, TypeVar, Generic, NoReturn, Set, List, Tuple, Dict, Counter as TCounter

T = TypeVar("T")
T1 = TypeVar("T1")
T2 = TypeVar("T2")


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


class FINQ(Iterable[T]):
    """Wrapper class for Iterables which simplifies processing of data"""

    def __init__(self, source: Iterable[T]):
        self._source = source

    def __iter__(self):
        for item in self._source:
            yield item

    def concat(self, b: Iterable[T]) -> 'FINQ[T]':
        """Concatenates two sequences, creating sequence that contains items of the
         first iterable then of second iterable."""
        return FINQConcat(self, b)

    def map(self, *func: Callable[[T], T]) -> 'FINQ[T]':
        """Applies composition of given functions to every element of sequence. """
        return FINQ(map(Compose(*func), self))

    def zip(self, *b: List[Iterable[T2]]) -> 'FINQ[Tuple]':
        """Pairs corresponding elements of two sequences in pairs."""
        return FINQ(zip(self, *b))

    def flat_map(self, func: Callable[[T], Iterable[T2]] = Identity) -> 'FINQ[T2]':
        """Applies given function to every element to get collection, then glues these collections."""
        return FINQFlatMap(self, func)

    def flatten(self, flattener: Callable[[T], T2] = Identity) -> 'FINQ[T2]':
        """Applies given function to every element to get collection, then glues these collections.
        Repeats while all elements are iterables."""
        return FINQFlatten(self, flattener)

    def filter(self, func: Callable[[T], T2]) -> 'FINQ[T2]':
        """Removes elements that doesn't satisfy predicate from sequence."""
        return FINQ(filter(func, self))

    def distinct(self, func: Callable[[T], T2] = Identity) -> 'FINQ[T]':
        """Skips elements which `f(element)` repeated."""
        return FINQDistinct(self, func)

    def sort(self, func: Callable[[T], float] = Identity, /, reverse=False) -> 'FINQ[T2]':
        """Sorts sequence elements by key given by `f`."""
        return FINQ(sorted(self, key=func, reverse=reverse))

    def skip(self, count: int) -> 'FINQ[T2]':
        """Skips `count` elements from sequence."""
        return FINQ(o for i, o in enumerate(self, 0) if i >= count)

    def take(self, count: int) -> 'FINQ[T2]':
        """Limits sequence by `count` elements, dropping others."""
        return FINQ(o for i, o in enumerate(self, 0) if i < count)

    def cartesian_product(self, b: Iterable[T1], mapping: Callable[[Tuple], T] = None) -> 'FINQ[Tuple[T,T1]]':
        """Returns Cartesian product of two sequences after application of mapping if specified."""
        return FINQCartesianProduct(self, b, mapping)

    def cartesian_power(self, power: int, mapping: Callable[[Tuple], T] = None) -> 'FINQ':
        """Returns Cartesian power of sequence after application of mapping if specified."""
        return FINQCartesianPower(self, power, mapping)

    def pairs(self) -> 'FINQ[Tuple[T,T]]':
        """Returns Cartesian square of sequence. Equivalent to Cartesian square with Identity mapping."""
        return FINQPairs(self)

    def enumerate(self, start: int = 0) -> 'FINQ[Tuple[int, T]]':
        """Maps sequence elements to pair which first value is index in sequence starting by `start`."""
        return FINQ(enumerate(self, start))

    def peek(self, func: NoReturn = Identity) -> 'FINQ[T]':
        """Applies function to each element in sequence leaving sequence unchanged."""
        return FINQPeek(self, func)

    def group_by(self, func: Callable[[T], T2] = Identity) -> 'FINQ[List[T]]':
        """Splits sequence into sequence of lists of elements which `f(x)` is the same."""
        return FINQGroupBy(self, func)

    def random(self, percentage: float) -> 'FINQ[T]':
        """Takes roughly `percentage*100%` of random elements of sequence."""
        return FINQ(i for i in self if random() < percentage)

    def sort_randomly(self) -> 'FINQ[T]':
        """Shuffles sequence."""
        return self.sort(OneArgRandom)

    def join(self, delimiter: str = '') -> str:
        """Joins sequence by `delimiter`."""
        return delimiter.join(self)

    def for_each(self, func: NoReturn = Consumer) -> NoReturn:
        """Calls `f` for every element of a sequence."""
        for item in self:
            func(item)

    def all(self, func: Callable[[T], bool] = IdentityTrue) -> bool:
        """Checks if all elements in sequence satisfy predicate."""
        for i in self:
            if not func(i):
                return False
        return True

    def any(self, func: Callable[[T], bool] = IdentityTrue) -> bool:
        """Checks if there exist element in sequence that satisfies predicate."""
        for i in self:
            if func(i):
                return True
        return False

    def none(self, func: Callable[[T], bool] = IdentityTrue) -> bool:
        """Checks if there no element in sequence that satisfies predicate."""
        for i in self:
            if func(i):
                return False
        return True

    def first(self) -> T:
        """Takes first element of sequence."""
        return next(iter(self))

    def to_list(self) -> List[T]:
        """Creates default python-list containing all sequence elements."""
        return list(self)

    def to_set(self) -> Set[T]:
        """Creates default python-set containing all distinct sequence elements."""
        return set(self)

    def to_counter(self) -> TCounter[T]:
        """Creates Counter containing all sequence elements."""
        return Counter(self)

    def to_dict(self, key: Callable[[T], T1] = First, value: Callable[[T], T2] = Second) -> Dict[T1, T2]:
        """Creates default python-dict containing mapping `(key(x), value(x))` for every `x` in sequence."""
        if key == First and value == Second:
            return dict(self)
        return dict(self.map(lambda t: (key(t), value(t))))

    def count(self) -> int:
        """Returns count of elements in sequence."""
        return len(list(self))

    def min(self) -> T:
        """Finds minimal element in sequence."""
        return min(self)

    def max(self) -> T:
        """Finds maximal element in sequence."""
        return max(self)

    def sum(self) -> T:
        """Sums all elements of sequence. Works only for summable types."""
        return sum(self) or 0

    def max_diff(self) -> T:
        """Counts maximal difference between elements. Equal to difference between max and min for sequence."""
        max_v, min_v = None, None
        for i in self:
            if max_v is None or i > max_v:
                max_v = i
            if min_v is None or i < min_v:
                min_v = i
        return max_v - min_v

    def reduce(self, reductor: Callable[[T, T], T], /, first: T = None) -> T:
        """Applies function to first two elements, then to result and next element until elements end.
         Allows to specify first element."""
        return next(iter(FINQReduce(self, reductor, first)))


class FINQFlatMap(FINQ[T]):
    """Applies given function to every element to get collection, then glues these collections."""

    def __init__(self, source: Iterable[T], mapper: Callable[[T], T2]):
        super().__init__(source)
        self.mapper = mapper

    def __iter__(self):
        for item in self._source:
            for sub_item in self.mapper(item):
                yield sub_item


class FINQPairs(FINQ[T]):
    """Returns Cartesian square of sequence. Equivalent to Cartesian square with Identity mapping."""

    def __init__(self, source: Iterable[T]):
        super().__init__(source)

    def __iter__(self):
        src_list = list(self._source)
        for i in src_list:
            for item2 in src_list:
                yield i, item2


class FINQPeek(FINQ[T]):
    """Applies function to each element in sequence leaving sequence unchanged."""

    def __init__(self, source: Iterable[T], func: NoReturn):
        super().__init__(source)
        self.func = func

    def __iter__(self):
        for item in self._source:
            self.func(item)
            yield item


class FINQReduce(FINQ[T]):
    """Applies function to first two elements, then to result and next element until elements end.
    Allows to specify first element."""

    def __init__(self, source: Iterable[T], reductor: Callable[[T, T], T], first=None):
        super().__init__(source)
        self.reductor = reductor
        self.firstValue = first

    def __iter__(self):
        result = self.firstValue
        for item in self._source:
            if not result:
                result = item
                continue
            result = self.reductor(result, item)
        yield result


class FINQCartesianProduct(FINQ[T], Generic[T, T1]):
    """Returns Cartesian product of two sequences after application of mapping if specified."""

    def __init__(self, source: Iterable[T], b: Iterable[T1], mapping: Callable[[Tuple], T] = None):
        super().__init__(source)
        self.mapping = mapping
        self.b = b

    def __iter__(self):
        b_list = list(self.b)
        if self.mapping is not None:
            for item in self._source:
                for b in b_list:
                    yield self.mapping((item, b))
        else:
            for item in self._source:
                for b in b_list:
                    yield item, b


class FINQCartesianPower(FINQ[T]):
    """Returns Cartesian power of sequence after application of mapping if specified."""

    def __init__(self, source: Iterable[T], power: int, mapping: Callable[[Tuple], T] = None):
        super().__init__(source)
        self.mapping = mapping
        self.power = power

    def __iter__(self):
        if self.power <= 0:
            return 0
        if self.power == 1:
            for k in self._source:
                yield k
            return
        items = list(self._source)
        for i in items:
            if self.mapping is not None:
                for j in FINQCartesianPower(items, self.power - 1):
                    if isinstance(j, tuple):
                        yield self.mapping((i, *j))
                    else:
                        yield self.mapping((i, j))
            else:
                for j in FINQCartesianPower(items, self.power - 1):
                    if isinstance(j, tuple):
                        yield i, *j
                    else:
                        yield i, j


class FINQGroupBy(FINQ[List[T]]):
    """Splits sequence into sequence of lists of elements which `f(x)` is the same."""

    def __init__(self, source: Iterable[T], func: Callable[[T], T2]):
        super().__init__(source)
        self.func = func

    def __iter__(self):
        groups = defaultdict(list)
        for i in self._source:
            groups[self.func(i)].append(i)
        for k in groups.keys():
            yield groups[k]


class FINQDistinct(FINQ[T]):
    """Skips elements which `f(element)` repeated."""

    def __init__(self, source: Iterable[T], func: Callable[[T], T2]):
        super().__init__(source)
        self.func = func

    def __iter__(self):
        looked = set()

        for item in self._source:
            var = self.func(item)
            if var not in looked:
                yield item
                looked.add(var)


class FINQConcat(FINQ[T]):
    """Concatenates two sequences, creating sequence that contains items of
    the first iterable then of second iterable."""

    def __init__(self, source: Iterable[T], b: Iterable[T]):
        super().__init__(source)
        self.b = b

    def __iter__(self):
        for i in self._source:
            yield i
        for i in self.b:
            yield i


class FINQFlatten(FINQ[T]):
    """Applies given function to every element to get collection, then glues these collections.
     Repeats while all elements are iterables."""

    def __init__(self, source: Iterable[T], flattener: Callable[[T], T2]):
        super().__init__(source)
        self.flattener = flattener

    def __iter__(self):
        for i in self._source:
            b = self.flattener(i)
            if isinstance(b, Iterable):
                yield from FINQFlatten(b, self.flattener)
            else:
                yield b
