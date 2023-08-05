from typing import Any as _py_Any
from typing import List as _py_List
from typing import TypeVar as _py_TypeVar
from typing import Type as _py_Type
from typing import ClassVar as _py_ClassVar
from typing import overload
import cern.accsoft.commons.domain
import cern.accsoft.commons.util
import cern.accsoft.commons.value
import cern.lsa.domain.cern.timing
import cern.lsa.domain.commons
import cern.lsa.domain.settings
import com.google.common.collect
import java.io
import java.lang
import java.time
import java.util


class ELTAG(java.lang.Enum['ELTAG']):
    FT1: _py_ClassVar['ELTAG'] = ...
    FT2: _py_ClassVar['ELTAG'] = ...
    FT3: _py_ClassVar['ELTAG'] = ...
    FT4: _py_ClassVar['ELTAG'] = ...
    FTSP1: _py_ClassVar['ELTAG'] = ...
    FTSP2: _py_ClassVar['ELTAG'] = ...
    FTSP3: _py_ClassVar['ELTAG'] = ...
    FT2A: _py_ClassVar['ELTAG'] = ...
    FT2B: _py_ClassVar['ELTAG'] = ...
    FT3A: _py_ClassVar['ELTAG'] = ...
    FT3B: _py_ClassVar['ELTAG'] = ...
    FT3C: _py_ClassVar['ELTAG'] = ...
    FT3D: _py_ClassVar['ELTAG'] = ...
    FT4A: _py_ClassVar['ELTAG'] = ...
    FT4B: _py_ClassVar['ELTAG'] = ...
    FT4C: _py_ClassVar['ELTAG'] = ...
    RMP: _py_ClassVar['ELTAG'] = ...
    @classmethod
    @overload
    def valueOf(cls, string: str) -> 'ELTAG': ...
    _valueOf_1__T = _py_TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @classmethod
    @overload
    def valueOf(cls, class_: _py_Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
    @classmethod
    def values(cls) -> _py_List['ELTAG']: ...

class ElenaCycleSegment(cern.accsoft.commons.util.Named):
    def addTimingProcess(self, timingProcess: cern.lsa.domain.cern.timing.TimingProcess, duration: java.time.Duration, timingProcessAnchor: cern.lsa.domain.cern.timing.TimingProcessAnchor) -> None: ...
    def getAttribute(self, string: str) -> str: ...
    def getAttributeNames(self) -> java.util.Set[str]: ...
    def getEndMomentum(self) -> int: ...
    def getHarmonicNumber(self) -> int: ...
    def getLength(self) -> java.time.Duration: ...
    def getScheduledTimingProcesses(self) -> java.util.Set[cern.lsa.domain.cern.timing.TimingProcessScheduling]: ...
    def getStartMomentum(self) -> int: ...
    def getStartTime(self) -> java.time.Duration: ...
    def getType(self) -> 'SegmentType': ...
    def isFirstSegmentInCycle(self) -> bool: ...
    def nextSegment(self) -> 'ElenaCycleSegment': ...
    def previousSegment(self) -> 'ElenaCycleSegment': ...
    def removeAttribute(self, string: str) -> None: ...
    def removeTimingProcess(self, timingProcess: cern.lsa.domain.cern.timing.TimingProcess) -> None: ...
    def setAttribute(self, string: str, string2: str) -> None: ...
    def setHarmonicNumber(self, int: int) -> None: ...
    def setLength(self, duration: java.time.Duration) -> None: ...
    def setName(self, string: str) -> None: ...

class ElenaCycleSettings:
    @classmethod
    def builder(cls) -> 'DefaultElenaCycleSettings.Builder': ...
    def getElenaCycleStructure(self) -> 'ElenaCycleStructure': ...
    def getParameterToCorrectionFunction(self) -> java.util.Map[cern.lsa.domain.settings.Parameter, cern.accsoft.commons.value.ImmutableDiscreteFunction]: ...
    def getParameterToTargetFunction(self) -> java.util.Map[cern.lsa.domain.settings.Parameter, cern.accsoft.commons.value.ImmutableDiscreteFunction]: ...

class ElenaCycleStructure(cern.lsa.domain.commons.IdentifiedEntity):
    def getId(self) -> int: ...
    def getInjectionMode(self) -> 'InjectionMode': ...
    def getInjectionSegment(self) -> 'FlatSegment': ...
    def getLength(self) -> java.time.Duration: ...
    def getParticleType(self) -> cern.accsoft.commons.domain.ParticleType: ...
    def getSegments(self) -> java.util.List[ElenaCycleSegment]: ...
    def getSegmentsCount(self) -> int: ...
    def getVersion(self) -> int: ...
    def insertFlatSegment(self, rampSegment: 'RampSegment', int: int) -> 'FlatSegment': ...
    def removeFlatSegment(self, flatSegment: 'FlatSegment') -> None: ...
    def setInjectionMode(self, injectionMode: 'InjectionMode') -> None: ...
    def setParticleType(self, particleType: cern.accsoft.commons.domain.ParticleType) -> None: ...

class InjectionMode(java.lang.Enum['InjectionMode']):
    AD: _py_ClassVar['InjectionMode'] = ...
    LOCAL_SOURCE: _py_ClassVar['InjectionMode'] = ...
    STANDALONE: _py_ClassVar['InjectionMode'] = ...
    def getTimingValue(self) -> str: ...
    @classmethod
    @overload
    def valueOf(cls, string: str) -> 'InjectionMode': ...
    _valueOf_1__T = _py_TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @classmethod
    @overload
    def valueOf(cls, class_: _py_Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
    @classmethod
    def values(cls) -> _py_List['InjectionMode']: ...

class PauseLocation(java.lang.Enum['PauseLocation']):
    NONE: _py_ClassVar['PauseLocation'] = ...
    BEFORE_START: _py_ClassVar['PauseLocation'] = ...
    BEFORE_END: _py_ClassVar['PauseLocation'] = ...
    AFTER_END: _py_ClassVar['PauseLocation'] = ...
    @classmethod
    @overload
    def valueOf(cls, string: str) -> 'PauseLocation': ...
    _valueOf_1__T = _py_TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @classmethod
    @overload
    def valueOf(cls, class_: _py_Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
    @classmethod
    def values(cls) -> _py_List['PauseLocation']: ...

class SegmentAttribute(java.lang.Enum['SegmentAttribute']):
    ELTAG: _py_ClassVar['SegmentAttribute'] = ...
    @classmethod
    @overload
    def valueOf(cls, string: str) -> 'SegmentAttribute': ...
    _valueOf_1__T = _py_TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @classmethod
    @overload
    def valueOf(cls, class_: _py_Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
    @classmethod
    def values(cls) -> _py_List['SegmentAttribute']: ...

class SegmentType(java.lang.Enum['SegmentType']):
    RAMP: _py_ClassVar['SegmentType'] = ...
    FLAT: _py_ClassVar['SegmentType'] = ...
    @classmethod
    @overload
    def valueOf(cls, string: str) -> 'SegmentType': ...
    _valueOf_1__T = _py_TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @classmethod
    @overload
    def valueOf(cls, class_: _py_Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
    @classmethod
    def values(cls) -> _py_List['SegmentType']: ...

class DefaultElenaCycleSettings(ElenaCycleSettings, java.io.Serializable):
    @classmethod
    def builder(cls) -> 'DefaultElenaCycleSettings.Builder': ...
    @classmethod
    def copyOf(cls, elenaCycleSettings: ElenaCycleSettings) -> 'DefaultElenaCycleSettings': ...
    def equals(self, object: _py_Any) -> bool: ...
    def getElenaCycleStructure(self) -> ElenaCycleStructure: ...
    @overload
    def getParameterToCorrectionFunction(self) -> com.google.common.collect.ImmutableMap[cern.lsa.domain.settings.Parameter, cern.accsoft.commons.value.ImmutableDiscreteFunction]: ...
    @overload
    def getParameterToCorrectionFunction(self) -> java.util.Map: ...
    @overload
    def getParameterToTargetFunction(self) -> com.google.common.collect.ImmutableMap[cern.lsa.domain.settings.Parameter, cern.accsoft.commons.value.ImmutableDiscreteFunction]: ...
    @overload
    def getParameterToTargetFunction(self) -> java.util.Map: ...
    def hashCode(self) -> int: ...
    def toString(self) -> str: ...
    def withElenaCycleStructure(self, elenaCycleStructure: ElenaCycleStructure) -> 'DefaultElenaCycleSettings': ...
    def withParameterToCorrectionFunction(self, map: java.util.Map[cern.lsa.domain.settings.Parameter, cern.accsoft.commons.value.ImmutableDiscreteFunction]) -> 'DefaultElenaCycleSettings': ...
    def withParameterToTargetFunction(self, map: java.util.Map[cern.lsa.domain.settings.Parameter, cern.accsoft.commons.value.ImmutableDiscreteFunction]) -> 'DefaultElenaCycleSettings': ...
    class Builder:
        def build(self) -> 'DefaultElenaCycleSettings': ...
        def elenaCycleStructure(self, elenaCycleStructure: ElenaCycleStructure) -> 'DefaultElenaCycleSettings.Builder': ...
        def parameterToCorrectionFunction(self, map: java.util.Map[cern.lsa.domain.settings.Parameter, cern.accsoft.commons.value.ImmutableDiscreteFunction]) -> 'DefaultElenaCycleSettings.Builder': ...
        def parameterToTargetFunction(self, map: java.util.Map[cern.lsa.domain.settings.Parameter, cern.accsoft.commons.value.ImmutableDiscreteFunction]) -> 'DefaultElenaCycleSettings.Builder': ...
        def putAllParameterToCorrectionFunction(self, map: java.util.Map[cern.lsa.domain.settings.Parameter, cern.accsoft.commons.value.ImmutableDiscreteFunction]) -> 'DefaultElenaCycleSettings.Builder': ...
        def putAllParameterToTargetFunction(self, map: java.util.Map[cern.lsa.domain.settings.Parameter, cern.accsoft.commons.value.ImmutableDiscreteFunction]) -> 'DefaultElenaCycleSettings.Builder': ...
        @overload
        def putParameterToCorrectionFunction(self, parameter: cern.lsa.domain.settings.Parameter, immutableDiscreteFunction: cern.accsoft.commons.value.ImmutableDiscreteFunction) -> 'DefaultElenaCycleSettings.Builder': ...
        @overload
        def putParameterToCorrectionFunction(self, entry: java.util.Map.Entry[cern.lsa.domain.settings.Parameter, cern.accsoft.commons.value.ImmutableDiscreteFunction]) -> 'DefaultElenaCycleSettings.Builder': ...
        @overload
        def putParameterToTargetFunction(self, parameter: cern.lsa.domain.settings.Parameter, immutableDiscreteFunction: cern.accsoft.commons.value.ImmutableDiscreteFunction) -> 'DefaultElenaCycleSettings.Builder': ...
        @overload
        def putParameterToTargetFunction(self, entry: java.util.Map.Entry[cern.lsa.domain.settings.Parameter, cern.accsoft.commons.value.ImmutableDiscreteFunction]) -> 'DefaultElenaCycleSettings.Builder': ...

class FlatSegment(ElenaCycleSegment):
    def getNumberOfExtractions(self) -> int: ...
    def getNumberOfInjections(self) -> int: ...
    def getPauseLocation(self) -> PauseLocation: ...
    def setNumberOfExtractions(self, int: int) -> None: ...
    def setNumberOfInjections(self, int: int) -> None: ...
    def setPauseLocation(self, pauseLocation: PauseLocation) -> None: ...

class RampSegment(ElenaCycleSegment):
    def getFlatPartLength(self) -> java.time.Duration: ...
    def getRoundPartLength(self) -> java.time.Duration: ...
    def setEndMomentum(self, int: int) -> None: ...
    def setFlatPartLength(self, duration: java.time.Duration) -> None: ...
    def setRoundPartLength(self, duration: java.time.Duration) -> None: ...
