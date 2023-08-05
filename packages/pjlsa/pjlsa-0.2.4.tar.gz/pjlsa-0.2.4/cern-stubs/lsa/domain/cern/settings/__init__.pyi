from typing import Any as _py_Any
from typing import List as _py_List
from typing import TypeVar as _py_TypeVar
from typing import Type as _py_Type
from typing import ClassVar as _py_ClassVar
from typing import overload
import cern.lsa.domain.settings
import com.google.common.collect
import java.io
import java.lang
import java.util


class BeamProcessTypeOpticTransitionInfo(java.io.Serializable):
    def __init__(self, double: float, string: str, string2: str, double2: float, double3: float): ...
    def getDuration(self) -> float: ...
    def getEndOptic(self) -> str: ...
    def getParabolicFraction(self) -> float: ...
    def getStartOptic(self) -> str: ...
    def getStartTime(self) -> float: ...

class CernContextCategory(java.lang.Enum['CernContextCategory'], cern.lsa.domain.settings.ContextCategory):
    MD: _py_ClassVar['CernContextCategory'] = ...
    OBSOLETE: _py_ClassVar['CernContextCategory'] = ...
    OPERATIONAL: _py_ClassVar['CernContextCategory'] = ...
    TEST: _py_ClassVar['CernContextCategory'] = ...
    ARCHIVED: _py_ClassVar['CernContextCategory'] = ...
    def getName(self) -> str: ...
    def isArchived(self) -> bool: ...
    @classmethod
    @overload
    def valueOf(cls, string: str) -> 'CernContextCategory': ...
    _valueOf_1__T = _py_TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @classmethod
    @overload
    def valueOf(cls, class_: _py_Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
    @classmethod
    def values(cls) -> _py_List['CernContextCategory']: ...

class DeviceReDriveResponse:
    def getDeviceName(self) -> str: ...
    def getParameterReDriveResponses(self) -> java.util.Set['ParameterReDriveResponse']: ...

class ParameterReDriveResponse:
    def containsError(self) -> bool: ...
    def getContextName(self) -> str: ...
    def getJapcParameterNameToExceptionMessage(self) -> java.util.Map[str, str]: ...
    def getLsaExceptionMessage(self) -> str: ...
    def getParameterName(self) -> str: ...

class ReDriveRequest:
    def getDeviceNamesToReDrive(self) -> java.util.Set[str]: ...

class ReDriveResponse:
    def getDeviceReDriveResponses(self) -> java.util.Collection[DeviceReDriveResponse]: ...

class DefaultDeviceReDriveResponse(DeviceReDriveResponse):
    @classmethod
    def builder(cls) -> 'DefaultDeviceReDriveResponse.Builder': ...
    @classmethod
    def copyOf(cls, deviceReDriveResponse: DeviceReDriveResponse) -> 'DefaultDeviceReDriveResponse': ...
    def equals(self, object: _py_Any) -> bool: ...
    def getDeviceName(self) -> str: ...
    @overload
    def getParameterReDriveResponses(self) -> com.google.common.collect.ImmutableSet[ParameterReDriveResponse]: ...
    @overload
    def getParameterReDriveResponses(self) -> java.util.Set: ...
    def hashCode(self) -> int: ...
    def toString(self) -> str: ...
    def withDeviceName(self, string: str) -> 'DefaultDeviceReDriveResponse': ...
    @overload
    def withParameterReDriveResponses(self, parameterReDriveResponseArray: _py_List[ParameterReDriveResponse]) -> 'DefaultDeviceReDriveResponse': ...
    @overload
    def withParameterReDriveResponses(self, iterable: java.lang.Iterable[ParameterReDriveResponse]) -> 'DefaultDeviceReDriveResponse': ...
    class Builder:
        def addAllParameterReDriveResponses(self, iterable: java.lang.Iterable[ParameterReDriveResponse]) -> 'DefaultDeviceReDriveResponse.Builder': ...
        def addParameterReDriveResponse(self, parameterReDriveResponse: ParameterReDriveResponse) -> 'DefaultDeviceReDriveResponse.Builder': ...
        def addParameterReDriveResponses(self, parameterReDriveResponseArray: _py_List[ParameterReDriveResponse]) -> 'DefaultDeviceReDriveResponse.Builder': ...
        def build(self) -> 'DefaultDeviceReDriveResponse': ...
        def deviceName(self, string: str) -> 'DefaultDeviceReDriveResponse.Builder': ...
        def parameterReDriveResponses(self, iterable: java.lang.Iterable[ParameterReDriveResponse]) -> 'DefaultDeviceReDriveResponse.Builder': ...

class DefaultParameterReDriveResponse(ParameterReDriveResponse):
    @classmethod
    def builder(cls) -> 'DefaultParameterReDriveResponse.Builder': ...
    def containsError(self) -> bool: ...
    @classmethod
    def copyOf(cls, parameterReDriveResponse: ParameterReDriveResponse) -> 'DefaultParameterReDriveResponse': ...
    def equals(self, object: _py_Any) -> bool: ...
    def getContextName(self) -> str: ...
    @overload
    def getJapcParameterNameToExceptionMessage(self) -> com.google.common.collect.ImmutableMap[str, str]: ...
    @overload
    def getJapcParameterNameToExceptionMessage(self) -> java.util.Map: ...
    def getLsaExceptionMessage(self) -> str: ...
    def getParameterName(self) -> str: ...
    def hashCode(self) -> int: ...
    def toString(self) -> str: ...
    def withContainsError(self, boolean: bool) -> 'DefaultParameterReDriveResponse': ...
    def withContextName(self, string: str) -> 'DefaultParameterReDriveResponse': ...
    def withJapcParameterNameToExceptionMessage(self, map: java.util.Map[str, str]) -> 'DefaultParameterReDriveResponse': ...
    def withLsaExceptionMessage(self, string: str) -> 'DefaultParameterReDriveResponse': ...
    def withParameterName(self, string: str) -> 'DefaultParameterReDriveResponse': ...
    class Builder:
        def build(self) -> 'DefaultParameterReDriveResponse': ...
        def containsError(self, boolean: bool) -> 'DefaultParameterReDriveResponse.Builder': ...
        def contextName(self, string: str) -> 'DefaultParameterReDriveResponse.Builder': ...
        def japcParameterNameToExceptionMessage(self, map: java.util.Map[str, str]) -> 'DefaultParameterReDriveResponse.Builder': ...
        def lsaExceptionMessage(self, string: str) -> 'DefaultParameterReDriveResponse.Builder': ...
        def parameterName(self, string: str) -> 'DefaultParameterReDriveResponse.Builder': ...
        def putAllJapcParameterNameToExceptionMessage(self, map: java.util.Map[str, str]) -> 'DefaultParameterReDriveResponse.Builder': ...
        @overload
        def putJapcParameterNameToExceptionMessage(self, string: str, string2: str) -> 'DefaultParameterReDriveResponse.Builder': ...
        @overload
        def putJapcParameterNameToExceptionMessage(self, entry: java.util.Map.Entry[str, str]) -> 'DefaultParameterReDriveResponse.Builder': ...

class DefaultReDriveRequest(ReDriveRequest):
    @classmethod
    def builder(cls) -> 'DefaultReDriveRequest.Builder': ...
    @classmethod
    def copyOf(cls, reDriveRequest: ReDriveRequest) -> 'DefaultReDriveRequest': ...
    def equals(self, object: _py_Any) -> bool: ...
    @overload
    def getDeviceNamesToReDrive(self) -> com.google.common.collect.ImmutableSet[str]: ...
    @overload
    def getDeviceNamesToReDrive(self) -> java.util.Set: ...
    def hashCode(self) -> int: ...
    def toString(self) -> str: ...
    @overload
    def withDeviceNamesToReDrive(self, iterable: java.lang.Iterable[str]) -> 'DefaultReDriveRequest': ...
    @overload
    def withDeviceNamesToReDrive(self, stringArray: _py_List[str]) -> 'DefaultReDriveRequest': ...
    class Builder:
        def addAllDeviceNamesToReDrive(self, iterable: java.lang.Iterable[str]) -> 'DefaultReDriveRequest.Builder': ...
        @overload
        def addDeviceNamesToReDrive(self, string: str) -> 'DefaultReDriveRequest.Builder': ...
        @overload
        def addDeviceNamesToReDrive(self, stringArray: _py_List[str]) -> 'DefaultReDriveRequest.Builder': ...
        def build(self) -> 'DefaultReDriveRequest': ...
        def deviceNamesToReDrive(self, iterable: java.lang.Iterable[str]) -> 'DefaultReDriveRequest.Builder': ...

class DefaultReDriveResponse(ReDriveResponse):
    @classmethod
    def builder(cls) -> 'DefaultReDriveResponse.Builder': ...
    @classmethod
    def copyOf(cls, reDriveResponse: ReDriveResponse) -> 'DefaultReDriveResponse': ...
    def equals(self, object: _py_Any) -> bool: ...
    def getDeviceReDriveResponses(self) -> java.util.Collection[DeviceReDriveResponse]: ...
    def hashCode(self) -> int: ...
    def toString(self) -> str: ...
    def withDeviceReDriveResponses(self, collection: java.util.Collection[DeviceReDriveResponse]) -> 'DefaultReDriveResponse': ...
    class Builder:
        def build(self) -> 'DefaultReDriveResponse': ...
        def deviceReDriveResponses(self, collection: java.util.Collection[DeviceReDriveResponse]) -> 'DefaultReDriveResponse.Builder': ...
