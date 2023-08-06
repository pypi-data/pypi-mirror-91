from collections import defaultdict, Counter
from typing import Iterable, Generic, Set as TSet, List as TList, Dict as TDict, Counter as TCounter

from finq.constants import *
from finq.typevars import *


class FINQ(Iterable[T]):
    """Wrapper class for Iterables which simplifies processing of data"""

    def __init__(self, source: Iterable[T]):
        self._source = source

    def __iter__(self):
        for item in self._source:
            yield item

    def self(self, extension: Callable[['FINQ[T]'], TOut]):
        return extension(self)

    def concat(self, b: Iterable[T]) -> 'FINQ[T]':
        """Concatenates two sequences, creating sequence that contains items of the
         first iterable then of second iterable."""
        return FINQConcat(self, b)

    def map(self, func: Callable[[T], TOut]) -> 'FINQ[TOut]':
        """Applies given function to every element of sequence. """
        return FINQ(map(func, self))

    def zip(self, *b: TList[Iterable[T2]]) -> 'FINQ[Tuple[T2, ...]]':
        """Pairs corresponding elements of two sequences in pairs."""
        return FINQ(zip(self, *b))

    def flat_map(self, func: Callable[[T], Iterable[T2]] = Identity) -> 'FINQ[T2]':
        """Applies given function to every element to get collection, then glues these collections."""
        return FINQFlatMap(self, func)

    def flatten(self, flattener: Callable[[T], T2] = Identity) -> 'FINQ[T2]':
        """Applies given function to every element to get collection, then glues these collections.
        Repeats until all elements are non iterable."""
        return FINQFlatten(self, flattener)

    def filter(self, predicate: Callable[[T], T2]) -> 'FINQ[T]':
        """Removes elements that doesn't satisfy predicate from sequence."""
        return FINQ(filter(predicate, self))

    def distinct(self, func: Callable[[T], T2] = Identity) -> 'FINQ[T]':
        """Skips elements which `f(element)` repeated."""
        return FINQDistinct(self, func)

    def sort(self, func: Callable[[T], float] = Identity, /, reverse=False) -> 'FINQ[T2]':
        """Sorts sequence elements by key given by `f`."""
        return FINQ(sorted(self, key=func, reverse=reverse))

    def skip(self, count: int) -> 'FINQ[T]':
        """Skips `count` elements from sequence."""
        return FINQ(o for i, o in enumerate(self, 0) if i >= count)

    def take(self, count: int) -> 'FINQ[T]':
        """Limits sequence by `count` elements, dropping others."""
        return FINQ(o for i, o in enumerate(self, 0) if i < count)

    def cartesian_product(self, b: Iterable[T2], mapping: Callable[[Tuple], T] = None) -> 'FINQ[Tuple[T,T2]]':
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

    def group_by(self, func: Callable[[T], T2] = Identity) -> 'FINQ[TList[T]]':
        """Splits sequence into sequence of lists of elements which `f(x)` is the same."""
        return FINQGroupBy(self, func)

    def random(self, percentage: float) -> 'FINQ[T]':
        """Takes roughly `percentage*100%` of random elements of sequence."""
        return FINQ(i for i in self if random() < percentage)

    def shuffle(self) -> 'FINQ[T]':
        """Shuffles sequence."""
        return self.sort(OneArgRandom)

    def join_str(self, delimiter: str = '') -> str:
        """Joins sequence by `delimiter`."""
        return delimiter.join(self)

    def join(self, sequence: Iterable[T2], condition: Callable[[T, T2], bool],
             aggregate: Callable[[T, T2], T3]) -> 'FINQ[T3]':
        """Joins two sequences. Two values are aggregated if `condition` is true"""
        return FINQJoin(self, sequence, condition, aggregate)

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

    def to_list(self) -> TList[T]:
        """Creates default python-list containing all sequence elements."""
        return list(self)

    def to_set(self) -> TSet[T]:
        """Creates default python-set containing all distinct sequence elements."""
        return set(self)

    def to_counter(self) -> TCounter[T]:
        """Creates Counter containing all sequence elements."""
        return Counter(self)

    def to_dict(self, key: Callable[[T], T1] = First, value: Callable[[T], T2] = Second) -> TDict[T1, T2]:
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

    def reduce(self, reducer: Callable[[T, T], T], /, first: T = None) -> T:
        """Applies function to first two elements, then to result and next element until elements end.
         Allows to specify first element."""
        return FINQReduce(self, reducer, first)

    def fold(self, mapper: Callable[[T], T2], aggregator: Callable[[T2, T2], T2], /) -> T2:
        """Applies mapper to each element, then aggregates pairs of T2 into single T2 until elements end.
        Equivalent to `finq.map(mapper).reduce(aggregator)`"""
        return FINQFold(self, mapper, aggregator)


class FINQFlatMap(FINQ[T]):
    """Applies given function to every element to get collection, then glues these collections."""

    def __init__(self, source: Iterable[T], mapper: Callable[[T], T2]):
        super().__init__(source)
        self.mapper = mapper

    def __iter__(self):
        for item in self._source:
            for sub_item in self.mapper(item):
                yield sub_item

    def self(self, extension: Callable[['FINQFlatMap[T]'], TOut]):
        return extension(self)


class FINQPairs(FINQ[T]):
    """Returns Cartesian square of sequence. Equivalent to Cartesian square with Identity mapping."""

    def __init__(self, source: Iterable[T]):
        super().__init__(source)

    def __iter__(self):
        src_list = list(self._source)
        for i in src_list:
            for item2 in src_list:
                yield i, item2

    def self(self, extension: Callable[['FINQPairs[T]'], TOut]):
        return extension(self)


class FINQPeek(FINQ[T]):
    """Applies function to each element in sequence leaving sequence unchanged."""

    def __init__(self, source: Iterable[T], func: NoReturn):
        super().__init__(source)
        self.func = func

    def __iter__(self):
        for item in self._source:
            self.func(item)
            yield item

    def self(self, extension: Callable[['FINQPeek[T]'], TOut]):
        return extension(self)


class FINQReduce(FINQ[T]):
    """Applies function to first two elements, then to result and next element until elements end.
    Allows to specify first element."""

    def __init__(self, source: Iterable[T], reducer: Callable[[T, T], T], first=None):
        super().__init__(source)
        self.reducer = reducer
        self.firstValue = first

    def __iter__(self):
        result = self.firstValue
        for item in self._source:
            if not result:
                result = item
                continue
            result = self.reducer(result, item)
        yield result

    def self(self, extension: Callable[['FINQReduce[T]'], TOut]):
        return extension(self)


class FINQFold(FINQ[T], Generic[T, T2]):
    """Applies mapper to each element, then aggregates pairs of T2 into single T2 until elements end.
    Allows to specify first element."""

    def __init__(self, source: Iterable[T], mapper: Callable[[T], T2], aggregator: Callable[[T2, T2], T2]):
        super().__init__(source)
        self.mapper = mapper
        self.aggregator = aggregator

    def __iter__(self):
        result = None
        for item in self._source:
            if not result:
                result = self.mapper(item)
                continue
            result = self.aggregator(result, self.mapper(item))
        yield result

    def self(self, extension: Callable[['FINQFold[T,T2]'], TOut]):
        return extension(self)


class FINQCartesianProduct(FINQ[T], Generic[T, T2]):
    """Returns Cartesian product of two sequences after application of mapping if specified."""

    def __init__(self, source: Iterable[T], b: Iterable[T2], mapping: Callable[[Tuple[T, T2]], T] = None):
        super().__init__(source)
        self.mapping = mapping
        self.b = b

    def __iter__(self) -> Iterable[Tuple[T, T2]]:
        b_list = list(self.b)
        if self.mapping is not None:
            for item in self._source:
                for b in b_list:
                    yield self.mapping((item, b))
        else:
            for item in self._source:
                for b in b_list:
                    yield item, b

    def self(self, extension: Callable[['FINQCartesianProduct[T, T2]'], TOut]):
        return extension(self)


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

    def self(self, extension: Callable[['FINQCartesianPower[T]'], TOut]):
        return extension(self)


class FINQGroupBy(FINQ[TList[T]]):
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

    def self(self, extension: Callable[['FINQGroupBy[T]'], TOut]):
        return extension(self)


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

    def self(self, extension: Callable[['FINQDistinct[T]'], TOut]):
        return extension(self)


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

    def self(self, extension: Callable[['FINQConcat[T]'], TOut]):
        return extension(self)


class FINQFlatten(FINQ[T]):
    """Applies given function to every element to get collection, then glues these collections.
    Repeats until all elements are non iterable."""

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

    def self(self, extension: Callable[['FINQFlatten[T]'], TOut]):
        return extension(self)


class FINQJoin(FINQ[T], Generic[T, T2, T3]):
    def __init__(self, source: Iterable[T], joined_sequence: Iterable[T2], condition: Callable[[T, T2], bool],
                 aggregator: Callable[[T, T2], T3]):
        super().__init__(source)
        self.aggregator = aggregator
        self.condition = condition
        self.joined_sequence = joined_sequence

    def __iter__(self):
        seq_list = list(self.joined_sequence)
        for i in self._source:
            for j in seq_list:
                if self.condition(i, j):
                    yield self.aggregator(i, j)

    def self(self, extension: Callable[['FINQJoin[T,T2, T3]'], TOut]):
        return extension(self)
