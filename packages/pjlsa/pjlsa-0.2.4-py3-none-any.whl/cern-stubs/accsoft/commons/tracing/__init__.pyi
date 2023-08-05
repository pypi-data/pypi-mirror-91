from typing import Any as _py_Any
from typing import List as _py_List
from typing import TypeVar as _py_TypeVar
from typing import Type as _py_Type
from typing import ClassVar as _py_ClassVar
from typing import overload
import cern.accsoft.commons.tracing.aop
import cern.accsoft.commons.tracing.requests
import cern.accsoft.commons.util.userctx
import java.lang
import java.lang.annotation
import java.util
import org.springframework.beans.factory


class TracerMBean:
    def getAspectClasses(self) -> _py_List[str]: ...
    def getRunningMode(self) -> bool: ...
    def getServerProcessInfo(self) -> str: ...
    def getStatus(self) -> str: ...
    def getTimeToLiveMBeansDays(self) -> int: ...
    def getTimeToNotifyRunningRequestsMillis(self) -> int: ...
    def getTracingLevel(self) -> str: ...
    def setRunningMode(self, boolean: bool) -> None: ...
    def setTimeToLiveMBeansDays(self, int: int) -> None: ...
    def setTimeToNotifyRunningRequestsMillis(self, long: int) -> None: ...
    def setTracingLevel(self, string: str) -> None: ...

class TracingConstants:
    TRACING_VALUE_MAX_LENGTH: _py_ClassVar[int] = ...
    JMX_OBJECT_NAME_PREFIX: _py_ClassVar[str] = ...
    DEFAULT_REQUEST_MBEANS_TIME_TO_LIVE_DAYS: _py_ClassVar[int] = ...
    DEFAULT_TRACING_LEVEL: _py_ClassVar['TracingLevel'] = ...
    DEFAULT_EXCEPTION_LINES: _py_ClassVar[int] = ...

class TracingInvocationExecutor(cern.accsoft.commons.util.userctx.ContextAwareRemoteInvocationExecutor, org.springframework.beans.factory.InitializingBean):
    def __init__(self): ...
    def afterPropertiesSet(self) -> None: ...
    def getReplaceProcessInfoWithRBACInfo(self) -> bool: ...
    def getTimeToLiveMBeansDays(self) -> int: ...
    def getTracingAspects(self) -> java.util.List[cern.accsoft.commons.tracing.aop.TracingAspect]: ...
    def getTracingConverter(self) -> 'TracingValueConverter': ...
    def getTracingLevel(self) -> str: ...
    def getWriteStats(self) -> bool: ...
    def setReplaceProcessInfoWithRBACInfo(self, boolean: bool) -> None: ...
    def setTimeToLiveMBeansDays(self, int: int) -> None: ...
    def setTracingAspects(self, list: java.util.List[cern.accsoft.commons.tracing.aop.TracingAspect]) -> None: ...
    def setTracingConverter(self, tracingValueConverter: 'TracingValueConverter') -> None: ...
    def setTracingLevel(self, string: str) -> None: ...
    def setWriteStats(self, boolean: bool) -> None: ...

class TracingLevel(java.lang.Enum['TracingLevel']):
    DOMAIN: _py_ClassVar['TracingLevel'] = ...
    APPLICATION: _py_ClassVar['TracingLevel'] = ...
    USER: _py_ClassVar['TracingLevel'] = ...
    LOCATION: _py_ClassVar['TracingLevel'] = ...
    def contains(self, tracingLevel: 'TracingLevel') -> bool: ...
    @classmethod
    @overload
    def valueOf(cls, string: str) -> 'TracingLevel': ...
    _valueOf_1__T = _py_TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @classmethod
    @overload
    def valueOf(cls, class_: _py_Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
    @classmethod
    def values(cls) -> _py_List['TracingLevel']: ...

class TracingNamedParameter(java.lang.annotation.Annotation):
    def equals(self, object: _py_Any) -> bool: ...
    def hashCode(self) -> int: ...
    def toString(self) -> str: ...
    def value(self) -> str: ...

class TracingValueConverter:
    def getArgumentValue(self, object: _py_Any, string: str) -> str: ...
    def getResultValue(self, object: _py_Any, string: str) -> str: ...

class Tracer(TracerMBean, TracingConstants):
    def addRequestToClient(self, clientRequestInfo: cern.accsoft.commons.tracing.requests.ClientRequestInfo) -> None: ...
    def getAspectClasses(self) -> _py_List[str]: ...
    def getCurrentRequestInfo(self) -> cern.accsoft.commons.tracing.requests.ClientRequestInfo: ...
    @classmethod
    def getInstance(cls) -> 'Tracer': ...
    def getRunningMode(self) -> bool: ...
    def getServerProcessInfo(self) -> str: ...
    def getStatus(self) -> str: ...
    def getTimeToLiveMBeansDays(self) -> int: ...
    def getTimeToNotifyRunningRequestsMillis(self) -> int: ...
    def getTracingAspects(self) -> java.util.List[cern.accsoft.commons.tracing.aop.TracingAspect]: ...
    def getTracingLevel(self) -> str: ...
    def removeRequestFromClient(self, clientRequestInfo: cern.accsoft.commons.tracing.requests.ClientRequestInfo) -> None: ...
    def setRunningMode(self, boolean: bool) -> None: ...
    def setTimeToLiveMBeansDays(self, int: int) -> None: ...
    def setTimeToNotifyRunningRequestsMillis(self, long: int) -> None: ...
    def setTracingAspects(self, list: java.util.List[cern.accsoft.commons.tracing.aop.TracingAspect]) -> None: ...
    def setTracingLevel(self, string: str) -> None: ...
