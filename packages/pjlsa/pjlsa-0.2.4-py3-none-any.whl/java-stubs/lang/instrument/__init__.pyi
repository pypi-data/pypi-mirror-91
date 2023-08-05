from typing import Any as _py_Any
from typing import List as _py_List
from typing import Type as _py_Type
from typing import overload
import java.lang
import java.security
import java.util.jar


class ClassDefinition:
    def __init__(self, class_: _py_Type[_py_Any], byteArray: _py_List[int]): ...
    def getDefinitionClass(self) -> _py_Type[_py_Any]: ...
    def getDefinitionClassFile(self) -> _py_List[int]: ...

class ClassFileTransformer:
    def transform(self, classLoader: java.lang.ClassLoader, string: str, class2: _py_Type[_py_Any], protectionDomain: java.security.ProtectionDomain, byteArray: _py_List[int]) -> _py_List[int]: ...

class IllegalClassFormatException(java.lang.Exception):
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, string: str): ...

class Instrumentation:
    @overload
    def addTransformer(self, classFileTransformer: ClassFileTransformer) -> None: ...
    @overload
    def addTransformer(self, classFileTransformer: ClassFileTransformer, boolean: bool) -> None: ...
    def appendToBootstrapClassLoaderSearch(self, jarFile: java.util.jar.JarFile) -> None: ...
    def appendToSystemClassLoaderSearch(self, jarFile: java.util.jar.JarFile) -> None: ...
    def getAllLoadedClasses(self) -> _py_List[_py_Type]: ...
    def getInitiatedClasses(self, classLoader: java.lang.ClassLoader) -> _py_List[_py_Type]: ...
    def getObjectSize(self, object: _py_Any) -> int: ...
    def isModifiableClass(self, class_: _py_Type[_py_Any]) -> bool: ...
    def isNativeMethodPrefixSupported(self) -> bool: ...
    def isRedefineClassesSupported(self) -> bool: ...
    def isRetransformClassesSupported(self) -> bool: ...
    def redefineClasses(self, classDefinitionArray: _py_List[ClassDefinition]) -> None: ...
    def removeTransformer(self, classFileTransformer: ClassFileTransformer) -> bool: ...
    def retransformClasses(self, classArray: _py_List[_py_Type[_py_Any]]) -> None: ...
    def setNativeMethodPrefix(self, classFileTransformer: ClassFileTransformer, string: str) -> None: ...

class UnmodifiableClassException(java.lang.Exception):
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, string: str): ...
