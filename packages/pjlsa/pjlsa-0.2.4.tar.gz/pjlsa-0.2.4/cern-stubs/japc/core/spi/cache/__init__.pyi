from typing import List as _py_List
from typing import TypeVar as _py_TypeVar
from typing import Type as _py_Type
from typing import ClassVar as _py_ClassVar
from typing import overload
import java.lang


class JapcCache:
    def clearAll(self) -> None: ...

class JapcCacheException(java.lang.Exception):
    @overload
    def __init__(self, string: str): ...
    @overload
    def __init__(self, string: str, throwable: java.lang.Throwable): ...
    @overload
    def __init__(self, throwable: java.lang.Throwable): ...

class JapcCacheType(java.lang.Enum['JapcCacheType']):
    DEVICE_TYPE: _py_ClassVar['JapcCacheType'] = ...
    DEVICE: _py_ClassVar['JapcCacheType'] = ...
    PARAMETER: _py_ClassVar['JapcCacheType'] = ...
    DEVICE_DESCRIPTOR: _py_ClassVar['JapcCacheType'] = ...
    PARAMETER_DESCRIPTOR: _py_ClassVar['JapcCacheType'] = ...
    VALUE_DESCRIPTOR: _py_ClassVar['JapcCacheType'] = ...
    SERVICE_CONFIG: _py_ClassVar['JapcCacheType'] = ...
    ENUM: _py_ClassVar['JapcCacheType'] = ...
    @classmethod
    @overload
    def valueOf(cls, string: str) -> 'JapcCacheType': ...
    _valueOf_1__T = _py_TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @classmethod
    @overload
    def valueOf(cls, class_: _py_Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
    @classmethod
    def values(cls) -> _py_List['JapcCacheType']: ...

class JapcCacheController(JapcCache):
    def __init__(self): ...
    def clearAll(self) -> None: ...
    @classmethod
    def getInstance(cls) -> 'JapcCacheController': ...
    def registerCache(self, japcCache: JapcCache) -> None: ...
    def unregisterCache(self, japcCache: JapcCache) -> None: ...
    class JmxMBean:
        def clearAll(self) -> None: ...
        def getRegisteredCaches(self) -> str: ...
