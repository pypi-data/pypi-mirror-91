from typing import Any as _py_Any
from typing import List as _py_List
from typing import TypeVar as _py_TypeVar
from typing import Type as _py_Type
from typing import ClassVar as _py_ClassVar
from typing import overload
import cern.lsa.domain.commons
import cern.lsa.domain.settings
import java.lang.reflect
import java.sql
import java.time
import java.util


class Attributes:
    MAX_ATTRIBUTE_VALUE_LENGTH: _py_ClassVar[int] = ...
    def __init__(self): ...
    @classmethod
    @overload
    def assertCanWriteAttributes(cls, object: _py_Any) -> cern.lsa.domain.commons.AttributeWritableAware: ...
    @classmethod
    @overload
    def assertCanWriteAttributes(cls, collection: java.util.Collection[_py_Any]) -> java.util.Collection[cern.lsa.domain.commons.AttributeWritableAware]: ...
    @classmethod
    def assertCorrectlyConstructedAttribute(cls, attribute: cern.lsa.domain.commons.Attribute) -> None: ...
    @classmethod
    def assertCorrectlyConstructedAttributes(cls, collection: java.util.Collection[cern.lsa.domain.commons.Attribute]) -> None: ...
    @classmethod
    def assertEntitiesHaveAllAttributes(cls, collection: java.util.Collection[cern.lsa.domain.commons.AttributeDefinition], collection2: java.util.Collection[cern.lsa.domain.commons.AttributeAware]) -> None: ...
    @classmethod
    def assertValidAttributeValue(cls, attributeDefinition: cern.lsa.domain.commons.AttributeDefinition, string: str) -> None: ...
    @classmethod
    def getAttributeDefinitions(cls, collection: java.util.Collection[cern.lsa.domain.commons.Attribute]) -> java.util.Set[cern.lsa.domain.commons.AttributeDefinition]: ...
    @classmethod
    def getAttributesWithDefaultValues(cls, collection: java.util.Collection[cern.lsa.domain.commons.AttributeDefinition]) -> java.util.Set[cern.lsa.domain.commons.Attribute]: ...
    _getValue__T = _py_TypeVar('_getValue__T')  # <T>
    @classmethod
    def getValue(cls, class_: _py_Type[_getValue__T], string: str) -> _getValue__T: ...
    @classmethod
    def isAttributeAware(cls, contextFamily: cern.lsa.domain.settings.ContextFamily) -> bool: ...
    @classmethod
    def overrideAttributeValues(cls, attributeWritableAware: cern.lsa.domain.commons.AttributeWritableAware, set: java.util.Set[cern.lsa.domain.commons.Attribute]) -> None: ...
    _overrideDefaultAttributeValues__T = _py_TypeVar('_overrideDefaultAttributeValues__T', bound=cern.lsa.domain.commons.AttributeWritableAware)  # <T>
    @classmethod
    def overrideDefaultAttributeValues(cls, collection: java.util.Collection[_overrideDefaultAttributeValues__T], map: java.util.Map[int, java.util.Set[cern.lsa.domain.commons.Attribute]]) -> None: ...
    @classmethod
    def validateAttributeValue(cls, attributeDefinition: cern.lsa.domain.commons.AttributeDefinition, string: str) -> 'Attributes.AttributeValidationResult': ...
    class AttributeValidationResult:
        def getErrorMessage(self) -> str: ...
        def isValid(self) -> bool: ...

class CacheUtil:
    def __init__(self): ...
    @classmethod
    def generateCacheKey(cls, object: _py_Any, method: java.lang.reflect.Method, objectArray: _py_List[_py_Any]) -> str: ...

class TimeUtils:
    @classmethod
    def convertToTimestamp(cls, instant: java.time.Instant) -> java.sql.Timestamp: ...
