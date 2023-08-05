from typing import List as _py_List
from typing import TypeVar as _py_TypeVar
from typing import Type as _py_Type
from typing import Generic as _py_Generic
from typing import overload
import java.io
import java.lang
import java.util.function


class AtomicBoolean(java.io.Serializable):
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, boolean: bool): ...
    def compareAndSet(self, boolean: bool, boolean2: bool) -> bool: ...
    def get(self) -> bool: ...
    def getAndSet(self, boolean: bool) -> bool: ...
    def lazySet(self, boolean: bool) -> None: ...
    def set(self, boolean: bool) -> None: ...
    def toString(self) -> str: ...
    def weakCompareAndSet(self, boolean: bool, boolean2: bool) -> bool: ...

class AtomicInteger(java.lang.Number, java.io.Serializable):
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, int: int): ...
    def accumulateAndGet(self, int: int, intBinaryOperator: java.util.function.IntBinaryOperator) -> int: ...
    def addAndGet(self, int: int) -> int: ...
    def compareAndSet(self, int: int, int2: int) -> bool: ...
    def decrementAndGet(self) -> int: ...
    def doubleValue(self) -> float: ...
    def floatValue(self) -> float: ...
    def get(self) -> int: ...
    def getAndAccumulate(self, int: int, intBinaryOperator: java.util.function.IntBinaryOperator) -> int: ...
    def getAndAdd(self, int: int) -> int: ...
    def getAndDecrement(self) -> int: ...
    def getAndIncrement(self) -> int: ...
    def getAndSet(self, int: int) -> int: ...
    def getAndUpdate(self, intUnaryOperator: java.util.function.IntUnaryOperator) -> int: ...
    def incrementAndGet(self) -> int: ...
    def intValue(self) -> int: ...
    def lazySet(self, int: int) -> None: ...
    def longValue(self) -> int: ...
    def set(self, int: int) -> None: ...
    def toString(self) -> str: ...
    def updateAndGet(self, intUnaryOperator: java.util.function.IntUnaryOperator) -> int: ...
    def weakCompareAndSet(self, int: int, int2: int) -> bool: ...

class AtomicIntegerArray(java.io.Serializable):
    @overload
    def __init__(self, int: int): ...
    @overload
    def __init__(self, intArray: _py_List[int]): ...
    def accumulateAndGet(self, int: int, int2: int, intBinaryOperator: java.util.function.IntBinaryOperator) -> int: ...
    def addAndGet(self, int: int, int2: int) -> int: ...
    def compareAndSet(self, int: int, int2: int, int3: int) -> bool: ...
    def decrementAndGet(self, int: int) -> int: ...
    def get(self, int: int) -> int: ...
    def getAndAccumulate(self, int: int, int2: int, intBinaryOperator: java.util.function.IntBinaryOperator) -> int: ...
    def getAndAdd(self, int: int, int2: int) -> int: ...
    def getAndDecrement(self, int: int) -> int: ...
    def getAndIncrement(self, int: int) -> int: ...
    def getAndSet(self, int: int, int2: int) -> int: ...
    def getAndUpdate(self, int: int, intUnaryOperator: java.util.function.IntUnaryOperator) -> int: ...
    def incrementAndGet(self, int: int) -> int: ...
    def lazySet(self, int: int, int2: int) -> None: ...
    def length(self) -> int: ...
    def set(self, int: int, int2: int) -> None: ...
    def toString(self) -> str: ...
    def updateAndGet(self, int: int, intUnaryOperator: java.util.function.IntUnaryOperator) -> int: ...
    def weakCompareAndSet(self, int: int, int2: int, int3: int) -> bool: ...

_AtomicIntegerFieldUpdater__T = _py_TypeVar('_AtomicIntegerFieldUpdater__T')  # <T>
class AtomicIntegerFieldUpdater(_py_Generic[_AtomicIntegerFieldUpdater__T]):
    def accumulateAndGet(self, t: _AtomicIntegerFieldUpdater__T, int: int, intBinaryOperator: java.util.function.IntBinaryOperator) -> int: ...
    def addAndGet(self, t: _AtomicIntegerFieldUpdater__T, int: int) -> int: ...
    def compareAndSet(self, t: _AtomicIntegerFieldUpdater__T, int: int, int2: int) -> bool: ...
    def decrementAndGet(self, t: _AtomicIntegerFieldUpdater__T) -> int: ...
    def get(self, t: _AtomicIntegerFieldUpdater__T) -> int: ...
    def getAndAccumulate(self, t: _AtomicIntegerFieldUpdater__T, int: int, intBinaryOperator: java.util.function.IntBinaryOperator) -> int: ...
    def getAndAdd(self, t: _AtomicIntegerFieldUpdater__T, int: int) -> int: ...
    def getAndDecrement(self, t: _AtomicIntegerFieldUpdater__T) -> int: ...
    def getAndIncrement(self, t: _AtomicIntegerFieldUpdater__T) -> int: ...
    def getAndSet(self, t: _AtomicIntegerFieldUpdater__T, int: int) -> int: ...
    def getAndUpdate(self, t: _AtomicIntegerFieldUpdater__T, intUnaryOperator: java.util.function.IntUnaryOperator) -> int: ...
    def incrementAndGet(self, t: _AtomicIntegerFieldUpdater__T) -> int: ...
    def lazySet(self, t: _AtomicIntegerFieldUpdater__T, int: int) -> None: ...
    _newUpdater__U = _py_TypeVar('_newUpdater__U')  # <U>
    @classmethod
    def newUpdater(cls, class_: _py_Type[_newUpdater__U], string: str) -> 'AtomicIntegerFieldUpdater'[_newUpdater__U]: ...
    def set(self, t: _AtomicIntegerFieldUpdater__T, int: int) -> None: ...
    def updateAndGet(self, t: _AtomicIntegerFieldUpdater__T, intUnaryOperator: java.util.function.IntUnaryOperator) -> int: ...
    def weakCompareAndSet(self, t: _AtomicIntegerFieldUpdater__T, int: int, int2: int) -> bool: ...

class AtomicLong(java.lang.Number, java.io.Serializable):
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, long: int): ...
    def accumulateAndGet(self, long: int, longBinaryOperator: java.util.function.LongBinaryOperator) -> int: ...
    def addAndGet(self, long: int) -> int: ...
    def compareAndSet(self, long: int, long2: int) -> bool: ...
    def decrementAndGet(self) -> int: ...
    def doubleValue(self) -> float: ...
    def floatValue(self) -> float: ...
    def get(self) -> int: ...
    def getAndAccumulate(self, long: int, longBinaryOperator: java.util.function.LongBinaryOperator) -> int: ...
    def getAndAdd(self, long: int) -> int: ...
    def getAndDecrement(self) -> int: ...
    def getAndIncrement(self) -> int: ...
    def getAndSet(self, long: int) -> int: ...
    def getAndUpdate(self, longUnaryOperator: java.util.function.LongUnaryOperator) -> int: ...
    def incrementAndGet(self) -> int: ...
    def intValue(self) -> int: ...
    def lazySet(self, long: int) -> None: ...
    def longValue(self) -> int: ...
    def set(self, long: int) -> None: ...
    def toString(self) -> str: ...
    def updateAndGet(self, longUnaryOperator: java.util.function.LongUnaryOperator) -> int: ...
    def weakCompareAndSet(self, long: int, long2: int) -> bool: ...

class AtomicLongArray(java.io.Serializable):
    @overload
    def __init__(self, int: int): ...
    @overload
    def __init__(self, longArray: _py_List[int]): ...
    def accumulateAndGet(self, int: int, long: int, longBinaryOperator: java.util.function.LongBinaryOperator) -> int: ...
    def addAndGet(self, int: int, long: int) -> int: ...
    def compareAndSet(self, int: int, long: int, long2: int) -> bool: ...
    def decrementAndGet(self, int: int) -> int: ...
    def get(self, int: int) -> int: ...
    def getAndAccumulate(self, int: int, long: int, longBinaryOperator: java.util.function.LongBinaryOperator) -> int: ...
    def getAndAdd(self, int: int, long: int) -> int: ...
    def getAndDecrement(self, int: int) -> int: ...
    def getAndIncrement(self, int: int) -> int: ...
    def getAndSet(self, int: int, long: int) -> int: ...
    def getAndUpdate(self, int: int, longUnaryOperator: java.util.function.LongUnaryOperator) -> int: ...
    def incrementAndGet(self, int: int) -> int: ...
    def lazySet(self, int: int, long: int) -> None: ...
    def length(self) -> int: ...
    def set(self, int: int, long: int) -> None: ...
    def toString(self) -> str: ...
    def updateAndGet(self, int: int, longUnaryOperator: java.util.function.LongUnaryOperator) -> int: ...
    def weakCompareAndSet(self, int: int, long: int, long2: int) -> bool: ...

_AtomicLongFieldUpdater__T = _py_TypeVar('_AtomicLongFieldUpdater__T')  # <T>
class AtomicLongFieldUpdater(_py_Generic[_AtomicLongFieldUpdater__T]):
    def accumulateAndGet(self, t: _AtomicLongFieldUpdater__T, long: int, longBinaryOperator: java.util.function.LongBinaryOperator) -> int: ...
    def addAndGet(self, t: _AtomicLongFieldUpdater__T, long: int) -> int: ...
    def compareAndSet(self, t: _AtomicLongFieldUpdater__T, long: int, long2: int) -> bool: ...
    def decrementAndGet(self, t: _AtomicLongFieldUpdater__T) -> int: ...
    def get(self, t: _AtomicLongFieldUpdater__T) -> int: ...
    def getAndAccumulate(self, t: _AtomicLongFieldUpdater__T, long: int, longBinaryOperator: java.util.function.LongBinaryOperator) -> int: ...
    def getAndAdd(self, t: _AtomicLongFieldUpdater__T, long: int) -> int: ...
    def getAndDecrement(self, t: _AtomicLongFieldUpdater__T) -> int: ...
    def getAndIncrement(self, t: _AtomicLongFieldUpdater__T) -> int: ...
    def getAndSet(self, t: _AtomicLongFieldUpdater__T, long: int) -> int: ...
    def getAndUpdate(self, t: _AtomicLongFieldUpdater__T, longUnaryOperator: java.util.function.LongUnaryOperator) -> int: ...
    def incrementAndGet(self, t: _AtomicLongFieldUpdater__T) -> int: ...
    def lazySet(self, t: _AtomicLongFieldUpdater__T, long: int) -> None: ...
    _newUpdater__U = _py_TypeVar('_newUpdater__U')  # <U>
    @classmethod
    def newUpdater(cls, class_: _py_Type[_newUpdater__U], string: str) -> 'AtomicLongFieldUpdater'[_newUpdater__U]: ...
    def set(self, t: _AtomicLongFieldUpdater__T, long: int) -> None: ...
    def updateAndGet(self, t: _AtomicLongFieldUpdater__T, longUnaryOperator: java.util.function.LongUnaryOperator) -> int: ...
    def weakCompareAndSet(self, t: _AtomicLongFieldUpdater__T, long: int, long2: int) -> bool: ...

_AtomicMarkableReference__V = _py_TypeVar('_AtomicMarkableReference__V')  # <V>
class AtomicMarkableReference(_py_Generic[_AtomicMarkableReference__V]):
    def __init__(self, v: _AtomicMarkableReference__V, boolean: bool): ...
    def attemptMark(self, v: _AtomicMarkableReference__V, boolean: bool) -> bool: ...
    def compareAndSet(self, v: _AtomicMarkableReference__V, v2: _AtomicMarkableReference__V, boolean: bool, boolean2: bool) -> bool: ...
    def get(self, booleanArray: _py_List[bool]) -> _AtomicMarkableReference__V: ...
    def getReference(self) -> _AtomicMarkableReference__V: ...
    def isMarked(self) -> bool: ...
    def set(self, v: _AtomicMarkableReference__V, boolean: bool) -> None: ...
    def weakCompareAndSet(self, v: _AtomicMarkableReference__V, v2: _AtomicMarkableReference__V, boolean: bool, boolean2: bool) -> bool: ...

_AtomicReference__V = _py_TypeVar('_AtomicReference__V')  # <V>
class AtomicReference(java.io.Serializable, _py_Generic[_AtomicReference__V]):
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, v: _AtomicReference__V): ...
    def accumulateAndGet(self, v: _AtomicReference__V, binaryOperator: java.util.function.BinaryOperator[_AtomicReference__V]) -> _AtomicReference__V: ...
    def compareAndSet(self, v: _AtomicReference__V, v2: _AtomicReference__V) -> bool: ...
    def get(self) -> _AtomicReference__V: ...
    def getAndAccumulate(self, v: _AtomicReference__V, binaryOperator: java.util.function.BinaryOperator[_AtomicReference__V]) -> _AtomicReference__V: ...
    def getAndSet(self, v: _AtomicReference__V) -> _AtomicReference__V: ...
    def getAndUpdate(self, unaryOperator: java.util.function.UnaryOperator[_AtomicReference__V]) -> _AtomicReference__V: ...
    def lazySet(self, v: _AtomicReference__V) -> None: ...
    def set(self, v: _AtomicReference__V) -> None: ...
    def toString(self) -> str: ...
    def updateAndGet(self, unaryOperator: java.util.function.UnaryOperator[_AtomicReference__V]) -> _AtomicReference__V: ...
    def weakCompareAndSet(self, v: _AtomicReference__V, v2: _AtomicReference__V) -> bool: ...

_AtomicReferenceArray__E = _py_TypeVar('_AtomicReferenceArray__E')  # <E>
class AtomicReferenceArray(java.io.Serializable, _py_Generic[_AtomicReferenceArray__E]):
    @overload
    def __init__(self, int: int): ...
    @overload
    def __init__(self, eArray: _py_List[_AtomicReferenceArray__E]): ...
    def accumulateAndGet(self, int: int, e: _AtomicReferenceArray__E, binaryOperator: java.util.function.BinaryOperator[_AtomicReferenceArray__E]) -> _AtomicReferenceArray__E: ...
    def compareAndSet(self, int: int, e: _AtomicReferenceArray__E, e2: _AtomicReferenceArray__E) -> bool: ...
    def get(self, int: int) -> _AtomicReferenceArray__E: ...
    def getAndAccumulate(self, int: int, e: _AtomicReferenceArray__E, binaryOperator: java.util.function.BinaryOperator[_AtomicReferenceArray__E]) -> _AtomicReferenceArray__E: ...
    def getAndSet(self, int: int, e: _AtomicReferenceArray__E) -> _AtomicReferenceArray__E: ...
    def getAndUpdate(self, int: int, unaryOperator: java.util.function.UnaryOperator[_AtomicReferenceArray__E]) -> _AtomicReferenceArray__E: ...
    def lazySet(self, int: int, e: _AtomicReferenceArray__E) -> None: ...
    def length(self) -> int: ...
    def set(self, int: int, e: _AtomicReferenceArray__E) -> None: ...
    def toString(self) -> str: ...
    def updateAndGet(self, int: int, unaryOperator: java.util.function.UnaryOperator[_AtomicReferenceArray__E]) -> _AtomicReferenceArray__E: ...
    def weakCompareAndSet(self, int: int, e: _AtomicReferenceArray__E, e2: _AtomicReferenceArray__E) -> bool: ...

_AtomicReferenceFieldUpdater__T = _py_TypeVar('_AtomicReferenceFieldUpdater__T')  # <T>
_AtomicReferenceFieldUpdater__V = _py_TypeVar('_AtomicReferenceFieldUpdater__V')  # <V>
class AtomicReferenceFieldUpdater(_py_Generic[_AtomicReferenceFieldUpdater__T, _AtomicReferenceFieldUpdater__V]):
    def accumulateAndGet(self, t: _AtomicReferenceFieldUpdater__T, v: _AtomicReferenceFieldUpdater__V, binaryOperator: java.util.function.BinaryOperator[_AtomicReferenceFieldUpdater__V]) -> _AtomicReferenceFieldUpdater__V: ...
    def compareAndSet(self, t: _AtomicReferenceFieldUpdater__T, v: _AtomicReferenceFieldUpdater__V, v2: _AtomicReferenceFieldUpdater__V) -> bool: ...
    def get(self, t: _AtomicReferenceFieldUpdater__T) -> _AtomicReferenceFieldUpdater__V: ...
    def getAndAccumulate(self, t: _AtomicReferenceFieldUpdater__T, v: _AtomicReferenceFieldUpdater__V, binaryOperator: java.util.function.BinaryOperator[_AtomicReferenceFieldUpdater__V]) -> _AtomicReferenceFieldUpdater__V: ...
    def getAndSet(self, t: _AtomicReferenceFieldUpdater__T, v: _AtomicReferenceFieldUpdater__V) -> _AtomicReferenceFieldUpdater__V: ...
    def getAndUpdate(self, t: _AtomicReferenceFieldUpdater__T, unaryOperator: java.util.function.UnaryOperator[_AtomicReferenceFieldUpdater__V]) -> _AtomicReferenceFieldUpdater__V: ...
    def lazySet(self, t: _AtomicReferenceFieldUpdater__T, v: _AtomicReferenceFieldUpdater__V) -> None: ...
    _newUpdater__U = _py_TypeVar('_newUpdater__U')  # <U>
    _newUpdater__W = _py_TypeVar('_newUpdater__W')  # <W>
    @classmethod
    def newUpdater(cls, class_: _py_Type[_newUpdater__U], class2: _py_Type[_newUpdater__W], string: str) -> 'AtomicReferenceFieldUpdater'[_newUpdater__U, _newUpdater__W]: ...
    def set(self, t: _AtomicReferenceFieldUpdater__T, v: _AtomicReferenceFieldUpdater__V) -> None: ...
    def updateAndGet(self, t: _AtomicReferenceFieldUpdater__T, unaryOperator: java.util.function.UnaryOperator[_AtomicReferenceFieldUpdater__V]) -> _AtomicReferenceFieldUpdater__V: ...
    def weakCompareAndSet(self, t: _AtomicReferenceFieldUpdater__T, v: _AtomicReferenceFieldUpdater__V, v2: _AtomicReferenceFieldUpdater__V) -> bool: ...

_AtomicStampedReference__V = _py_TypeVar('_AtomicStampedReference__V')  # <V>
class AtomicStampedReference(_py_Generic[_AtomicStampedReference__V]):
    def __init__(self, v: _AtomicStampedReference__V, int: int): ...
    def attemptStamp(self, v: _AtomicStampedReference__V, int: int) -> bool: ...
    def compareAndSet(self, v: _AtomicStampedReference__V, v2: _AtomicStampedReference__V, int: int, int2: int) -> bool: ...
    def get(self, intArray: _py_List[int]) -> _AtomicStampedReference__V: ...
    def getReference(self) -> _AtomicStampedReference__V: ...
    def getStamp(self) -> int: ...
    def set(self, v: _AtomicStampedReference__V, int: int) -> None: ...
    def weakCompareAndSet(self, v: _AtomicStampedReference__V, v2: _AtomicStampedReference__V, int: int, int2: int) -> bool: ...

class Striped64(java.lang.Number): ...

class DoubleAccumulator(Striped64, java.io.Serializable):
    def __init__(self, doubleBinaryOperator: java.util.function.DoubleBinaryOperator, double2: float): ...
    def accumulate(self, double: float) -> None: ...
    def doubleValue(self) -> float: ...
    def floatValue(self) -> float: ...
    def get(self) -> float: ...
    def getThenReset(self) -> float: ...
    def intValue(self) -> int: ...
    def longValue(self) -> int: ...
    def reset(self) -> None: ...
    def toString(self) -> str: ...

class DoubleAdder(Striped64, java.io.Serializable):
    def __init__(self): ...
    def add(self, double: float) -> None: ...
    def doubleValue(self) -> float: ...
    def floatValue(self) -> float: ...
    def intValue(self) -> int: ...
    def longValue(self) -> int: ...
    def reset(self) -> None: ...
    def sum(self) -> float: ...
    def sumThenReset(self) -> float: ...
    def toString(self) -> str: ...

class LongAccumulator(Striped64, java.io.Serializable):
    def __init__(self, longBinaryOperator: java.util.function.LongBinaryOperator, long2: int): ...
    def accumulate(self, long: int) -> None: ...
    def doubleValue(self) -> float: ...
    def floatValue(self) -> float: ...
    def get(self) -> int: ...
    def getThenReset(self) -> int: ...
    def intValue(self) -> int: ...
    def longValue(self) -> int: ...
    def reset(self) -> None: ...
    def toString(self) -> str: ...

class LongAdder(Striped64, java.io.Serializable):
    def __init__(self): ...
    def add(self, long: int) -> None: ...
    def decrement(self) -> None: ...
    def doubleValue(self) -> float: ...
    def floatValue(self) -> float: ...
    def increment(self) -> None: ...
    def intValue(self) -> int: ...
    def longValue(self) -> int: ...
    def reset(self) -> None: ...
    def sum(self) -> int: ...
    def sumThenReset(self) -> int: ...
    def toString(self) -> str: ...
