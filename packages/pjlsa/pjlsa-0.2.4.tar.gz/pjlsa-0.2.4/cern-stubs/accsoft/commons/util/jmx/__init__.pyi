from typing import Any as _py_Any
from typing import overload
import java.util
import javax.management
import org.slf4j


class MBeanRegistry:
    @overload
    def createObjectName(self, string: str) -> javax.management.ObjectName: ...
    @classmethod
    @overload
    def createObjectName(cls, string: str, string2: str) -> javax.management.ObjectName: ...
    @classmethod
    def get(cls) -> 'MBeanRegistry': ...
    def registerMBean(self, string: str, object: _py_Any, logger: org.slf4j.Logger) -> javax.management.ObjectInstance: ...
    def setJmxAppName(self, string: str) -> None: ...
    def unregisterAll(self, logger: org.slf4j.Logger) -> None: ...
    def unregisterMBean(self, string: str, logger: org.slf4j.Logger) -> None: ...

class NameParser:
    def __init__(self): ...
    @classmethod
    def parseName(cls, string: str) -> 'NameParser.Name': ...
    class Name:
        def __init__(self, string: str, map: java.util.Map[str, str], boolean: bool): ...
        def getDomainName(self) -> str: ...
        def getProperties(self) -> java.util.Map[str, str]: ...
        def isPropertyListPattern(self) -> bool: ...
        def toString(self) -> str: ...
