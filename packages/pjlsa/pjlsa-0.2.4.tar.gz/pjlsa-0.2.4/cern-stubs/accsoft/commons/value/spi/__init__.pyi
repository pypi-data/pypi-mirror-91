from typing import Any as _py_Any
from typing import List as _py_List
from typing import overload
import cern.accsoft.commons.value
import cern.accsoft.commons.value.operation
import cern.accsoft.commons.value.spi.operation
import cern.japc.value
import cern.japc.value.spi.value.simple
import java.io
import java.util


class AbstractValue(cern.accsoft.commons.value.Value):
    def clone(self) -> _py_Any: ...
    @classmethod
    @overload
    def createValue(cls, type: cern.accsoft.commons.value.Type) -> cern.japc.value.spi.value.simple.AbstractSimpleValue: ...
    @classmethod
    @overload
    def createValue(cls, type: cern.accsoft.commons.value.Type, object: _py_Any) -> cern.japc.value.spi.value.simple.AbstractSimpleValue: ...
    @classmethod
    @overload
    def createValue(cls, object: _py_Any) -> cern.japc.value.spi.value.simple.AbstractSimpleValue: ...
    def equals(self, object: _py_Any) -> bool: ...
    def getType(self) -> cern.accsoft.commons.value.Type: ...
    def getValueDescriptor(self) -> cern.accsoft.commons.value.ValueDescriptor: ...
    def hashCode(self) -> int: ...
    def isDefined(self) -> bool: ...
    def makeMutable(self) -> cern.accsoft.commons.value.Value: ...
    def setDefined(self, boolean: bool) -> None: ...
    def setValueDescriptor(self, valueDescriptor: cern.accsoft.commons.value.ValueDescriptor) -> None: ...
    def toString(self) -> str: ...

class IOUtils:
    def __init__(self): ...
    @classmethod
    def parseCSV(cls, file: java.io.File) -> java.util.Map[str, cern.accsoft.commons.value.ImmutableValue]: ...
    @classmethod
    def toCSV(cls, file: java.io.File, map: java.util.Map[str, cern.accsoft.commons.value.ImmutableValue]) -> None: ...

class ValueDescriptorImpl(cern.accsoft.commons.value.ValueDescriptor):
    def __init__(self): ...
    @overload
    def clone(self) -> cern.accsoft.commons.value.ValueDescriptor: ...
    @overload
    def clone(self) -> 'ValueDescriptorImpl': ...
    @overload
    def clone(self) -> _py_Any: ...
    def containsMeanings(self) -> bool: ...
    def getAbsoluteTolerance(self) -> float: ...
    def getBooleanType(self) -> cern.japc.value.BooleanType: ...
    def getColumnCount(self) -> int: ...
    def getEnumType(self) -> cern.japc.value.EnumType: ...
    def getMax(self) -> float: ...
    def getMeaning(self, object: _py_Any) -> cern.japc.value.SimpleValueStandardMeaning: ...
    def getMin(self) -> float: ...
    def getRelativeTolerance(self) -> float: ...
    def getRowCount(self) -> int: ...
    def getXPrecision(self) -> int: ...
    def getXUnit(self) -> str: ...
    def getYPrecision(self) -> int: ...
    def getYUnit(self) -> str: ...
    def isSettable(self, object: _py_Any) -> bool: ...
    def setAbsoluteTolerance(self, double: float) -> None: ...
    def setBooleanType(self, booleanType: cern.japc.value.BooleanType) -> None: ...
    def setColumnCount(self, integer: int) -> None: ...
    def setEnumType(self, enumType: cern.japc.value.EnumType) -> None: ...
    def setMax(self, double: float) -> None: ...
    def setMin(self, double: float) -> None: ...
    def setPrecision(self, integer: int) -> None: ...
    def setRelativeTolerance(self, double: float) -> None: ...
    def setRowCount(self, integer: int) -> None: ...
    def setXPrecision(self, integer: int) -> None: ...
    def setXUnit(self, string: str) -> None: ...
    def setYPrecision(self, integer: int) -> None: ...
    def setYUnit(self, string: str) -> None: ...
    def toString(self) -> str: ...

class ScalarArrayView(AbstractValue, cern.accsoft.commons.value.ScalarArray, java.io.Serializable):
    def __init__(self, scalarArray: cern.accsoft.commons.value.ScalarArray, int: int, int2: int): ...
    def clone(self) -> _py_Any: ...
    def equals(self, object: _py_Any) -> bool: ...
    @overload
    def execute(self, indexing: cern.accsoft.commons.value.spi.operation.Indexing) -> cern.accsoft.commons.value.Scalar: ...
    @overload
    def execute(self, binaryOperation: cern.accsoft.commons.value.operation.BinaryOperation, immutableValue: cern.accsoft.commons.value.ImmutableValue) -> None: ...
    @overload
    def execute(self, unaryOperation: cern.accsoft.commons.value.operation.UnaryOperation) -> None: ...
    def getArray2D(self) -> cern.japc.value.Array2D: ...
    @overload
    def getBoolean(self) -> bool: ...
    @overload
    def getBoolean(self, int: int) -> bool: ...
    @overload
    def getBooleans(self) -> _py_List[bool]: ...
    @overload
    def getBooleans(self, int: int, int2: int) -> _py_List[bool]: ...
    @overload
    def getByte(self) -> int: ...
    @overload
    def getByte(self, int: int) -> int: ...
    @overload
    def getBytes(self) -> _py_List[int]: ...
    @overload
    def getBytes(self, int: int, int2: int) -> _py_List[int]: ...
    @overload
    def getDouble(self) -> float: ...
    @overload
    def getDouble(self, int: int) -> float: ...
    @overload
    def getDoubles(self) -> _py_List[float]: ...
    @overload
    def getDoubles(self, int: int, int2: int) -> _py_List[float]: ...
    @overload
    def getFloat(self) -> float: ...
    @overload
    def getFloat(self, int: int) -> float: ...
    @overload
    def getFloats(self) -> _py_List[float]: ...
    @overload
    def getFloats(self, int: int, int2: int) -> _py_List[float]: ...
    @overload
    def getInt(self) -> int: ...
    @overload
    def getInt(self, int: int) -> int: ...
    @overload
    def getInts(self) -> _py_List[int]: ...
    @overload
    def getInts(self, int: int, int2: int) -> _py_List[int]: ...
    def getLength(self) -> int: ...
    @overload
    def getLong(self) -> int: ...
    @overload
    def getLong(self, int: int) -> int: ...
    @overload
    def getLongs(self) -> _py_List[int]: ...
    @overload
    def getLongs(self, int: int, int2: int) -> _py_List[int]: ...
    @overload
    def getObject(self) -> _py_Any: ...
    @overload
    def getObject(self, int: int) -> _py_Any: ...
    def getScalar(self, int: int) -> cern.accsoft.commons.value.ImmutableScalar: ...
    def getScalars(self) -> _py_List[cern.accsoft.commons.value.ImmutableScalar]: ...
    @overload
    def getShort(self) -> int: ...
    @overload
    def getShort(self, int: int) -> int: ...
    @overload
    def getShorts(self) -> _py_List[int]: ...
    @overload
    def getShorts(self, int: int, int2: int) -> _py_List[int]: ...
    @overload
    def getString(self) -> str: ...
    @overload
    def getString(self, int: int) -> str: ...
    @overload
    def getStrings(self) -> _py_List[str]: ...
    @overload
    def getStrings(self, int: int, int2: int) -> _py_List[str]: ...
    def getType(self) -> cern.accsoft.commons.value.Type: ...
    def getValueDescriptor(self) -> cern.accsoft.commons.value.ValueDescriptor: ...
    def hashCode(self) -> int: ...
    def indexOf(self, object: _py_Any) -> int: ...
    def insert(self, int: int, double: float) -> None: ...
    def insertAll(self, intArray: _py_List[int], doubleArray: _py_List[float]) -> None: ...
    def isDefined(self) -> bool: ...
    def makeMutable(self) -> cern.accsoft.commons.value.Value: ...
    def remove(self, int: int) -> None: ...
    def removeAll(self, intArray: _py_List[int]) -> None: ...
    @overload
    def setBoolean(self, boolean: bool) -> None: ...
    @overload
    def setBoolean(self, int: int, boolean: bool) -> None: ...
    def setBooleans(self, booleanArray: _py_List[bool]) -> None: ...
    @overload
    def setByte(self, byte: int) -> None: ...
    @overload
    def setByte(self, int: int, byte: int) -> None: ...
    def setBytes(self, byteArray: _py_List[int]) -> None: ...
    @overload
    def setDouble(self, double: float) -> None: ...
    @overload
    def setDouble(self, int: int, double: float) -> None: ...
    def setDoubles(self, doubleArray: _py_List[float]) -> None: ...
    @overload
    def setFloat(self, float: float) -> None: ...
    @overload
    def setFloat(self, int: int, float: float) -> None: ...
    def setFloats(self, floatArray: _py_List[float]) -> None: ...
    @overload
    def setInt(self, int: int) -> None: ...
    @overload
    def setInt(self, int: int, int2: int) -> None: ...
    def setInts(self, intArray: _py_List[int]) -> None: ...
    @overload
    def setLong(self, int: int, long: int) -> None: ...
    @overload
    def setLong(self, long: int) -> None: ...
    def setLongs(self, longArray: _py_List[int]) -> None: ...
    def setObject(self, object: _py_Any) -> None: ...
    def setScalar(self, int: int, immutableScalar: cern.accsoft.commons.value.ImmutableScalar) -> None: ...
    def setScalars(self, immutableScalarArray: _py_List[cern.accsoft.commons.value.ImmutableScalar]) -> None: ...
    @overload
    def setShort(self, int: int, short: int) -> None: ...
    @overload
    def setShort(self, short: int) -> None: ...
    def setShorts(self, shortArray: _py_List[int]) -> None: ...
    @overload
    def setString(self, int: int, string: str) -> None: ...
    @overload
    def setString(self, string: str) -> None: ...
    def setStrings(self, stringArray: _py_List[str]) -> None: ...
    def subArray(self, int: int, int2: int) -> cern.accsoft.commons.value.ScalarArray: ...
    def toSimpleParameterValue(self) -> cern.japc.value.SimpleParameterValue: ...
    def toString(self) -> str: ...

class ScalarImpl(AbstractValue, cern.accsoft.commons.value.Scalar):
    def __init__(self, type: cern.accsoft.commons.value.Type, simpleParameterValue: cern.japc.value.SimpleParameterValue): ...
    def asMatrix(self, intArray: _py_List[int]) -> cern.accsoft.commons.value.ScalarArray2D: ...
    def asVector(self, int: int) -> cern.accsoft.commons.value.ScalarArray: ...
    def clone(self) -> _py_Any: ...
    def equals(self, object: _py_Any) -> bool: ...
    @overload
    def execute(self, binaryOperation: cern.accsoft.commons.value.operation.BinaryOperation, immutableValue: cern.accsoft.commons.value.ImmutableValue) -> None: ...
    @overload
    def execute(self, unaryOperation: cern.accsoft.commons.value.operation.UnaryOperation) -> None: ...
    def getBoolean(self) -> bool: ...
    def getByte(self) -> int: ...
    def getDouble(self) -> float: ...
    def getFloat(self) -> float: ...
    def getInt(self) -> int: ...
    def getLong(self) -> int: ...
    def getObject(self) -> _py_Any: ...
    def getShort(self) -> int: ...
    def getString(self) -> str: ...
    def hashCode(self) -> int: ...
    def setBoolean(self, boolean: bool) -> None: ...
    def setByte(self, byte: int) -> None: ...
    def setDouble(self, double: float) -> None: ...
    def setFloat(self, float: float) -> None: ...
    def setInt(self, int: int) -> None: ...
    def setLong(self, long: int) -> None: ...
    def setObject(self, object: _py_Any) -> None: ...
    def setShort(self, short: int) -> None: ...
    def setString(self, string: str) -> None: ...
    def toSimpleParameterValue(self) -> cern.japc.value.SimpleParameterValue: ...
    def toString(self) -> str: ...

class PointImpl(ScalarImpl, cern.accsoft.commons.value.Point):
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, immutablePoint: cern.accsoft.commons.value.ImmutablePoint): ...
    @overload
    def __init__(self, double: float, double2: float): ...
    def equals(self, object: _py_Any) -> bool: ...
    def getX(self) -> float: ...
    def getY(self) -> float: ...
    def hashCode(self) -> int: ...
    @classmethod
    def interpolate(cls, pointImpl: 'PointImpl', pointImpl2: 'PointImpl', double: float) -> cern.accsoft.commons.value.Point: ...
    def isContinueWith(self, value: cern.accsoft.commons.value.Value) -> bool: ...
    def setX(self, double: float) -> None: ...
    def setY(self, double: float) -> None: ...
    def toString(self) -> str: ...

class ScalarArrayImpl(ScalarImpl, cern.accsoft.commons.value.ScalarArray):
    def __init__(self, type: cern.accsoft.commons.value.Type, simpleParameterValue: cern.japc.value.SimpleParameterValue): ...
    def asMatrix(self, intArray: _py_List[int]) -> cern.accsoft.commons.value.ScalarArray2D: ...
    def asVector(self, int: int) -> cern.accsoft.commons.value.ScalarArray: ...
    def equals(self, object: _py_Any) -> bool: ...
    @overload
    def execute(self, indexing: cern.accsoft.commons.value.spi.operation.Indexing) -> cern.accsoft.commons.value.Scalar: ...
    @overload
    def execute(self, binaryOperation: cern.accsoft.commons.value.operation.BinaryOperation, immutableValue: cern.accsoft.commons.value.ImmutableValue) -> None: ...
    @overload
    def execute(self, unaryOperation: cern.accsoft.commons.value.operation.UnaryOperation) -> None: ...
    def getArray2D(self) -> cern.japc.value.Array2D: ...
    @overload
    def getBoolean(self, int: int) -> bool: ...
    @overload
    def getBoolean(self) -> bool: ...
    @overload
    def getBooleans(self) -> _py_List[bool]: ...
    @overload
    def getBooleans(self, int: int, int2: int) -> _py_List[bool]: ...
    @overload
    def getByte(self, int: int) -> int: ...
    @overload
    def getByte(self) -> int: ...
    @overload
    def getBytes(self) -> _py_List[int]: ...
    @overload
    def getBytes(self, int: int, int2: int) -> _py_List[int]: ...
    def getColumnCount(self) -> int: ...
    @overload
    def getDouble(self, int: int) -> float: ...
    @overload
    def getDouble(self) -> float: ...
    @overload
    def getDoubles(self) -> _py_List[float]: ...
    @overload
    def getDoubles(self, int: int, int2: int) -> _py_List[float]: ...
    @overload
    def getFloat(self, int: int) -> float: ...
    @overload
    def getFloat(self) -> float: ...
    @overload
    def getFloats(self) -> _py_List[float]: ...
    @overload
    def getFloats(self, int: int, int2: int) -> _py_List[float]: ...
    @overload
    def getInt(self, int: int) -> int: ...
    @overload
    def getInt(self) -> int: ...
    @overload
    def getInts(self) -> _py_List[int]: ...
    @overload
    def getInts(self, int: int, int2: int) -> _py_List[int]: ...
    def getLength(self) -> int: ...
    @overload
    def getLong(self, int: int) -> int: ...
    @overload
    def getLong(self) -> int: ...
    @overload
    def getLongs(self) -> _py_List[int]: ...
    @overload
    def getLongs(self, int: int, int2: int) -> _py_List[int]: ...
    @overload
    def getObject(self, int: int) -> _py_Any: ...
    @overload
    def getObject(self) -> _py_Any: ...
    def getRowCount(self) -> int: ...
    def getScalar(self, int: int) -> cern.accsoft.commons.value.ImmutableScalar: ...
    def getScalars(self) -> _py_List[cern.accsoft.commons.value.ImmutableScalar]: ...
    @overload
    def getShort(self, int: int) -> int: ...
    @overload
    def getShort(self) -> int: ...
    @overload
    def getShorts(self) -> _py_List[int]: ...
    @overload
    def getShorts(self, int: int, int2: int) -> _py_List[int]: ...
    @overload
    def getString(self, int: int) -> str: ...
    @overload
    def getString(self) -> str: ...
    @overload
    def getStrings(self) -> _py_List[str]: ...
    @overload
    def getStrings(self, int: int, int2: int) -> _py_List[str]: ...
    def hashCode(self) -> int: ...
    def indexOf(self, object: _py_Any) -> int: ...
    def insert(self, int: int, double: float) -> None: ...
    def insertAll(self, intArray: _py_List[int], doubleArray: _py_List[float]) -> None: ...
    def remove(self, int: int) -> None: ...
    def removeAll(self, intArray: _py_List[int]) -> None: ...
    @overload
    def setBoolean(self, int: int, boolean: bool) -> None: ...
    @overload
    def setBoolean(self, boolean: bool) -> None: ...
    def setBooleans(self, booleanArray: _py_List[bool]) -> None: ...
    @overload
    def setByte(self, int: int, byte: int) -> None: ...
    @overload
    def setByte(self, byte: int) -> None: ...
    def setBytes(self, byteArray: _py_List[int]) -> None: ...
    @overload
    def setDouble(self, int: int, double: float) -> None: ...
    @overload
    def setDouble(self, double: float) -> None: ...
    def setDoubles(self, doubleArray: _py_List[float]) -> None: ...
    @overload
    def setFloat(self, int: int, float: float) -> None: ...
    @overload
    def setFloat(self, float: float) -> None: ...
    def setFloats(self, floatArray: _py_List[float]) -> None: ...
    @overload
    def setInt(self, int: int, int2: int) -> None: ...
    @overload
    def setInt(self, int: int) -> None: ...
    def setInts(self, intArray: _py_List[int]) -> None: ...
    @overload
    def setLong(self, int: int, long: int) -> None: ...
    @overload
    def setLong(self, long: int) -> None: ...
    def setLongs(self, longArray: _py_List[int]) -> None: ...
    def setObject(self, object: _py_Any) -> None: ...
    def setScalar(self, int: int, immutableScalar: cern.accsoft.commons.value.ImmutableScalar) -> None: ...
    def setScalars(self, immutableScalarArray: _py_List[cern.accsoft.commons.value.ImmutableScalar]) -> None: ...
    @overload
    def setShort(self, int: int, short: int) -> None: ...
    @overload
    def setShort(self, short: int) -> None: ...
    def setShorts(self, shortArray: _py_List[int]) -> None: ...
    @overload
    def setString(self, int: int, string: str) -> None: ...
    @overload
    def setString(self, string: str) -> None: ...
    def setStrings(self, stringArray: _py_List[str]) -> None: ...
    def subArray(self, int: int, int2: int) -> cern.accsoft.commons.value.ScalarArray: ...

class ScalarArray2DImpl(ScalarArrayImpl, cern.accsoft.commons.value.ScalarArray2D):
    def __init__(self, type: cern.accsoft.commons.value.Type, simpleParameterValue: cern.japc.value.SimpleParameterValue): ...
    def equals(self, object: _py_Any) -> bool: ...
    @overload
    def execute(self, indexing: cern.accsoft.commons.value.spi.operation.Indexing) -> cern.accsoft.commons.value.Scalar: ...
    @overload
    def execute(self, indexing: cern.accsoft.commons.value.spi.operation.Indexing) -> cern.accsoft.commons.value.ScalarArray: ...
    @overload
    def execute(self, binaryOperation: cern.accsoft.commons.value.operation.BinaryOperation, immutableValue: cern.accsoft.commons.value.ImmutableValue) -> None: ...
    @overload
    def execute(self, unaryOperation: cern.accsoft.commons.value.operation.UnaryOperation) -> None: ...
    def getArray2D(self) -> cern.japc.value.Array2D: ...
    def getColumnCount(self) -> int: ...
    def getRowCount(self) -> int: ...
    def hashCode(self) -> int: ...
    def setBooleans2D(self, booleanArray: _py_List[bool], int: int, int2: int) -> None: ...
    def setBytes2D(self, byteArray: _py_List[int], int: int, int2: int) -> None: ...
    def setDoubles2D(self, doubleArray: _py_List[float], int: int, int2: int) -> None: ...
    def setFloats2D(self, floatArray: _py_List[float], int: int, int2: int) -> None: ...
    def setInts2D(self, intArray: _py_List[int], int2: int, int3: int) -> None: ...
    def setLongs2D(self, longArray: _py_List[int], int: int, int2: int) -> None: ...
    def setObjects2D(self, object: _py_Any, int: int, int2: int) -> None: ...
    def setShorts2D(self, shortArray: _py_List[int], int: int, int2: int) -> None: ...
    def setStrings2D(self, stringArray: _py_List[str], int: int, int2: int) -> None: ...
