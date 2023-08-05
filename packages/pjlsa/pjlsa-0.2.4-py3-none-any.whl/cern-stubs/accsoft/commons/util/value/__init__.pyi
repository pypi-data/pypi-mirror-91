from typing import Any as _py_Any
from typing import List as _py_List
from typing import TypeVar as _py_TypeVar
from typing import ClassVar as _py_ClassVar
from typing import Generic as _py_Generic
from typing import overload
import com.google.common.collect
import java.io
import java.lang
import java.util.function


_Either__L = _py_TypeVar('_Either__L')  # <L>
_Either__R = _py_TypeVar('_Either__R')  # <R>
class Either(_py_Generic[_Either__L, _Either__R]):
    def accept(self, consumer: java.util.function.Consumer[_Either__L], consumer2: java.util.function.Consumer[_Either__R]) -> None: ...
    _bimap__LM = _py_TypeVar('_bimap__LM')  # <LM>
    _bimap__RM = _py_TypeVar('_bimap__RM')  # <RM>
    def bimap(self, function: java.util.function.Function[_Either__L, _bimap__LM], function2: java.util.function.Function[_Either__R, _bimap__RM]) -> 'Either'[_bimap__LM, _bimap__RM]: ...
    _either__L = _py_TypeVar('_either__L')  # <L>
    _either__R = _py_TypeVar('_either__R')  # <R>
    @classmethod
    def either(cls, l: _either__L, r: _either__R) -> 'Either'[_either__L, _either__R]: ...
    _fold__T = _py_TypeVar('_fold__T')  # <T>
    def fold(self, function: java.util.function.Function[_Either__L, _fold__T], function2: java.util.function.Function[_Either__R, _fold__T]) -> _fold__T: ...
    def ifLeft(self, consumer: java.util.function.Consumer[_Either__L]) -> None: ...
    def ifRight(self, consumer: java.util.function.Consumer[_Either__R]) -> None: ...
    def isLeft(self) -> bool: ...
    def isRight(self) -> bool: ...
    @overload
    def left(self) -> _Either__L: ...
    _left_1__L = _py_TypeVar('_left_1__L')  # <L>
    _left_1__R = _py_TypeVar('_left_1__R')  # <R>
    @classmethod
    @overload
    def left(cls, l: _left_1__L) -> 'Either'[_left_1__L, _left_1__R]: ...
    def leftOrElse(self, l: _Either__L) -> _Either__L: ...
    def leftOrElseGet(self, supplier: java.util.function.Supplier[_Either__L]) -> _Either__L: ...
    @overload
    def leftOrThrow(self, exception: java.lang.Exception) -> _Either__L: ...
    @overload
    def leftOrThrow(self, supplier: java.util.function.Supplier[java.lang.Exception]) -> _Either__L: ...
    _mapLeft__LM = _py_TypeVar('_mapLeft__LM')  # <LM>
    def mapLeft(self, function: java.util.function.Function[_Either__L, _mapLeft__LM]) -> 'Either'[_mapLeft__LM, _Either__R]: ...
    _mapRight__RM = _py_TypeVar('_mapRight__RM')  # <RM>
    def mapRight(self, function: java.util.function.Function[_Either__R, _mapRight__RM]) -> 'Either'[_Either__L, _mapRight__RM]: ...
    @overload
    def right(self) -> _Either__R: ...
    _right_1__L = _py_TypeVar('_right_1__L')  # <L>
    _right_1__R = _py_TypeVar('_right_1__R')  # <R>
    @classmethod
    @overload
    def right(cls, r: _right_1__R) -> 'Either'[_right_1__L, _right_1__R]: ...
    def rightOrElse(self, r: _Either__R) -> _Either__R: ...
    def rightOrElseGet(self, supplier: java.util.function.Supplier[_Either__R]) -> _Either__R: ...
    @overload
    def rightOrThrow(self, exception: java.lang.Exception) -> _Either__R: ...
    @overload
    def rightOrThrow(self, supplier: java.util.function.Supplier[java.lang.Exception]) -> _Either__R: ...
    def swap(self) -> 'Either'[_Either__R, _Either__L]: ...

_FailSafe__E = _py_TypeVar('_FailSafe__E', bound=java.lang.Exception)  # <E>
_FailSafe__T = _py_TypeVar('_FailSafe__T')  # <T>
class FailSafe(_py_Generic[_FailSafe__E, _FailSafe__T]):
    def accept(self, consumer: java.util.function.Consumer[_FailSafe__E], consumer2: java.util.function.Consumer[_FailSafe__T]) -> None: ...
    def exception(self) -> _FailSafe__E: ...
    _flatMap__NE = _py_TypeVar('_flatMap__NE', bound=java.lang.Exception)  # <NE>
    _flatMap__U = _py_TypeVar('_flatMap__U')  # <U>
    def flatMap(self, function: java.util.function.Function[_FailSafe__T, 'FailSafe'[_flatMap__NE, _flatMap__U]]) -> 'FailSafe'[_FailSafe__E, _flatMap__U]: ...
    _fold__V = _py_TypeVar('_fold__V')  # <V>
    def fold(self, function: java.util.function.Function[_FailSafe__E, _fold__V], function2: java.util.function.Function[_FailSafe__T, _fold__V]) -> _fold__V: ...
    def ifValuePresent(self, consumer: java.util.function.Consumer[_FailSafe__T]) -> None: ...
    def isEmpty(self) -> bool: ...
    def isException(self) -> bool: ...
    def isValue(self) -> bool: ...
    _map__U = _py_TypeVar('_map__U')  # <U>
    def map(self, function: java.util.function.Function[_FailSafe__T, _map__U]) -> 'FailSafe'[_FailSafe__E, _map__U]: ...
    _of_0__E = _py_TypeVar('_of_0__E', bound=java.lang.Exception)  # <E>
    _of_0__T = _py_TypeVar('_of_0__T')  # <T>
    @classmethod
    @overload
    def of(cls, e: _of_0__E) -> 'FailSafe'[_of_0__E, _of_0__T]: ...
    _of_1__E = _py_TypeVar('_of_1__E', bound=java.lang.Exception)  # <E>
    _of_1__T = _py_TypeVar('_of_1__T')  # <T>
    @classmethod
    @overload
    def of(cls, t: _of_1__T) -> 'FailSafe'[_of_1__E, _of_1__T]: ...
    def orElse(self, t: _FailSafe__T) -> _FailSafe__T: ...
    def orElseGet(self, supplier: java.util.function.Supplier[_FailSafe__T]) -> _FailSafe__T: ...
    @overload
    def orElseThrow(self) -> _FailSafe__T: ...
    @overload
    def orElseThrow(self, exception: java.lang.Exception) -> _FailSafe__T: ...
    @overload
    def orElseThrow(self, supplier: java.util.function.Supplier[java.lang.Exception]) -> _FailSafe__T: ...
    def value(self) -> _FailSafe__T: ...

_FailSafeValue__V = _py_TypeVar('_FailSafeValue__V')  # <V>
class FailSafeValue(_py_Generic[_FailSafeValue__V]):
    @overload
    def __init__(self, exception: java.lang.Exception): ...
    @overload
    def __init__(self, v: _FailSafeValue__V): ...
    def containsException(self) -> bool: ...
    def containsValue(self) -> bool: ...
    _emptyValue__V = _py_TypeVar('_emptyValue__V')  # <V>
    @classmethod
    def emptyValue(cls) -> 'FailSafeValue'[_emptyValue__V]: ...
    def getException(self) -> java.lang.Exception: ...
    def getValue(self) -> _FailSafeValue__V: ...
    def isEmpty(self) -> bool: ...
    def toString(self) -> str: ...

_Pair__E = _py_TypeVar('_Pair__E')  # <E>
_Pair__T = _py_TypeVar('_Pair__T')  # <T>
class Pair(java.io.Serializable, _py_Generic[_Pair__E, _Pair__T]):
    def __init__(self, e: _Pair__E, t: _Pair__T): ...
    def equals(self, object: _py_Any) -> bool: ...
    def getFirst(self) -> _Pair__E: ...
    def getSecond(self) -> _Pair__T: ...
    def hashCode(self) -> int: ...
    _newInstance__R = _py_TypeVar('_newInstance__R')  # <R>
    _newInstance__S = _py_TypeVar('_newInstance__S')  # <S>
    @classmethod
    def newInstance(cls, r: _newInstance__R, s: _newInstance__S) -> 'Pair'[_newInstance__R, _newInstance__S]: ...
    def toString(self) -> str: ...

class Ranges:
    def __init__(self): ...
    class DoubleRanges:
        EMPTY_RANGE: _py_ClassVar[com.google.common.collect.Range] = ...
        def __init__(self): ...
        @classmethod
        def contains(cls, range: com.google.common.collect.Range[float], double: float) -> bool: ...
        @classmethod
        def getCenter(cls, range: com.google.common.collect.Range[float]) -> float: ...
        @classmethod
        def getLength(cls, range: com.google.common.collect.Range[float]) -> float: ...
    class LongRanges:
        def __init__(self): ...
        @classmethod
        def contains(cls, range: com.google.common.collect.Range[int], long: int) -> bool: ...
        @classmethod
        def getCenter(cls, range: com.google.common.collect.Range[int]) -> float: ...
        @classmethod
        def getLength(cls, range: com.google.common.collect.Range[int]) -> int: ...

_FailSafeImpl__E = _py_TypeVar('_FailSafeImpl__E', bound=java.lang.Exception)  # <E>
_FailSafeImpl__T = _py_TypeVar('_FailSafeImpl__T')  # <T>
class FailSafeImpl(FailSafe[_FailSafeImpl__E, _FailSafeImpl__T], _py_Generic[_FailSafeImpl__E, _FailSafeImpl__T]):
    def equals(self, object: _py_Any) -> bool: ...
    def exception(self) -> _FailSafeImpl__E: ...
    def hashCode(self) -> int: ...
    def isValue(self) -> bool: ...
    def toString(self) -> str: ...
    def value(self) -> _FailSafeImpl__T: ...

_Left__L = _py_TypeVar('_Left__L')  # <L>
_Left__R = _py_TypeVar('_Left__R')  # <R>
class Left(Either[_Left__L, _Left__R], _py_Generic[_Left__L, _Left__R]):
    def equals(self, object: _py_Any) -> bool: ...
    def hashCode(self) -> int: ...
    def isRight(self) -> bool: ...
    def left(self) -> _Left__L: ...
    def right(self) -> _Left__R: ...
    def toString(self) -> str: ...

_Right__L = _py_TypeVar('_Right__L')  # <L>
_Right__R = _py_TypeVar('_Right__R')  # <R>
class Right(Either[_Right__L, _Right__R], _py_Generic[_Right__L, _Right__R]):
    def equals(self, object: _py_Any) -> bool: ...
    def hashCode(self) -> int: ...
    def isRight(self) -> bool: ...
    def left(self) -> _Right__L: ...
    def right(self) -> _Right__R: ...
    def toString(self) -> str: ...

_SerializablePair__E = _py_TypeVar('_SerializablePair__E', bound=java.io.Serializable)  # <E>
_SerializablePair__T = _py_TypeVar('_SerializablePair__T', bound=java.io.Serializable)  # <T>
class SerializablePair(Pair[_SerializablePair__E, _SerializablePair__T], java.io.Serializable, _py_Generic[_SerializablePair__E, _SerializablePair__T]):
    @classmethod
    def main(cls, stringArray: _py_List[str]) -> None: ...
    _newInstance_0__R = _py_TypeVar('_newInstance_0__R')  # <R>
    _newInstance_0__S = _py_TypeVar('_newInstance_0__S')  # <S>
    @classmethod
    @overload
    def newInstance(cls, r: _newInstance_0__R, s: _newInstance_0__S) -> Pair[_newInstance_0__R, _newInstance_0__S]: ...
    _newInstance_1__R = _py_TypeVar('_newInstance_1__R', bound=java.io.Serializable)  # <R>
    _newInstance_1__S = _py_TypeVar('_newInstance_1__S', bound=java.io.Serializable)  # <S>
    @classmethod
    @overload
    def newInstance(cls, r: _newInstance_1__R, s: _newInstance_1__S) -> 'SerializablePair'[_newInstance_1__R, _newInstance_1__S]: ...
