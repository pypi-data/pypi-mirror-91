from typing import Any as _py_Any
from typing import List as _py_List
from typing import Type as _py_Type
from typing import ClassVar as _py_ClassVar
from typing import overload
import java.io
import java.lang
import java.util


class Clipboard:
    def __init__(self, string: str): ...
    def addFlavorListener(self, flavorListener: 'FlavorListener') -> None: ...
    def getAvailableDataFlavors(self) -> _py_List['DataFlavor']: ...
    def getContents(self, object: _py_Any) -> 'Transferable': ...
    def getData(self, dataFlavor: 'DataFlavor') -> _py_Any: ...
    def getFlavorListeners(self) -> _py_List['FlavorListener']: ...
    def getName(self) -> str: ...
    def isDataFlavorAvailable(self, dataFlavor: 'DataFlavor') -> bool: ...
    def removeFlavorListener(self, flavorListener: 'FlavorListener') -> None: ...
    def setContents(self, transferable: 'Transferable', clipboardOwner: 'ClipboardOwner') -> None: ...

class ClipboardOwner:
    def lostOwnership(self, clipboard: Clipboard, transferable: 'Transferable') -> None: ...

class DataFlavor(java.io.Externalizable, java.lang.Cloneable):
    stringFlavor: _py_ClassVar['DataFlavor'] = ...
    imageFlavor: _py_ClassVar['DataFlavor'] = ...
    plainTextFlavor: _py_ClassVar['DataFlavor'] = ...
    javaSerializedObjectMimeType: _py_ClassVar[str] = ...
    javaFileListFlavor: _py_ClassVar['DataFlavor'] = ...
    javaJVMLocalObjectMimeType: _py_ClassVar[str] = ...
    javaRemoteObjectMimeType: _py_ClassVar[str] = ...
    selectionHtmlFlavor: _py_ClassVar['DataFlavor'] = ...
    fragmentHtmlFlavor: _py_ClassVar['DataFlavor'] = ...
    allHtmlFlavor: _py_ClassVar['DataFlavor'] = ...
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, class_: _py_Type[_py_Any], string: str): ...
    @overload
    def __init__(self, string: str): ...
    @overload
    def __init__(self, string: str, string2: str): ...
    @overload
    def __init__(self, string: str, string2: str, classLoader: java.lang.ClassLoader): ...
    def clone(self) -> _py_Any: ...
    @overload
    def equals(self, dataFlavor: 'DataFlavor') -> bool: ...
    @overload
    def equals(self, object: _py_Any) -> bool: ...
    @overload
    def equals(self, string: str) -> bool: ...
    def getDefaultRepresentationClass(self) -> _py_Type[_py_Any]: ...
    def getDefaultRepresentationClassAsString(self) -> str: ...
    def getHumanPresentableName(self) -> str: ...
    def getMimeType(self) -> str: ...
    def getParameter(self, string: str) -> str: ...
    def getPrimaryType(self) -> str: ...
    def getReaderForText(self, transferable: 'Transferable') -> java.io.Reader: ...
    def getRepresentationClass(self) -> _py_Type[_py_Any]: ...
    def getSubType(self) -> str: ...
    @classmethod
    def getTextPlainUnicodeFlavor(cls) -> 'DataFlavor': ...
    def hashCode(self) -> int: ...
    def isFlavorJavaFileListType(self) -> bool: ...
    def isFlavorRemoteObjectType(self) -> bool: ...
    def isFlavorSerializedObjectType(self) -> bool: ...
    def isFlavorTextType(self) -> bool: ...
    @overload
    def isMimeTypeEqual(self, string: str) -> bool: ...
    @overload
    def isMimeTypeEqual(self, dataFlavor: 'DataFlavor') -> bool: ...
    def isMimeTypeSerializedObject(self) -> bool: ...
    def isRepresentationClassByteBuffer(self) -> bool: ...
    def isRepresentationClassCharBuffer(self) -> bool: ...
    def isRepresentationClassInputStream(self) -> bool: ...
    def isRepresentationClassReader(self) -> bool: ...
    def isRepresentationClassRemote(self) -> bool: ...
    def isRepresentationClassSerializable(self) -> bool: ...
    def match(self, dataFlavor: 'DataFlavor') -> bool: ...
    def readExternal(self, objectInput: java.io.ObjectInput) -> None: ...
    @classmethod
    def selectBestTextFlavor(cls, dataFlavorArray: _py_List['DataFlavor']) -> 'DataFlavor': ...
    def setHumanPresentableName(self, string: str) -> None: ...
    def toString(self) -> str: ...
    def writeExternal(self, objectOutput: java.io.ObjectOutput) -> None: ...

class FlavorEvent(java.util.EventObject):
    def __init__(self, clipboard: Clipboard): ...

class FlavorListener(java.util.EventListener):
    def flavorsChanged(self, flavorEvent: FlavorEvent) -> None: ...

class FlavorMap:
    def getFlavorsForNatives(self, stringArray: _py_List[str]) -> java.util.Map[str, DataFlavor]: ...
    def getNativesForFlavors(self, dataFlavorArray: _py_List[DataFlavor]) -> java.util.Map[DataFlavor, str]: ...

class MimeType(java.io.Externalizable, java.lang.Cloneable):
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, string: str): ...
    @overload
    def __init__(self, string: str, string2: str): ...
    @overload
    def __init__(self, string: str, string2: str, mimeTypeParameterList: 'MimeTypeParameterList'): ...
    def clone(self) -> _py_Any: ...
    def equals(self, object: _py_Any) -> bool: ...
    def getBaseType(self) -> str: ...
    def getParameter(self, string: str) -> str: ...
    def getParameters(self) -> 'MimeTypeParameterList': ...
    def getPrimaryType(self) -> str: ...
    def getSubType(self) -> str: ...
    def hashCode(self) -> int: ...
    @overload
    def match(self, mimeType: 'MimeType') -> bool: ...
    @overload
    def match(self, string: str) -> bool: ...
    def readExternal(self, objectInput: java.io.ObjectInput) -> None: ...
    def removeParameter(self, string: str) -> None: ...
    def setParameter(self, string: str, string2: str) -> None: ...
    def toString(self) -> str: ...
    def writeExternal(self, objectOutput: java.io.ObjectOutput) -> None: ...

class MimeTypeParameterList(java.lang.Cloneable):
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, string: str): ...
    def clone(self) -> _py_Any: ...
    def equals(self, object: _py_Any) -> bool: ...
    def get(self, string: str) -> str: ...
    def getNames(self) -> java.util.Enumeration[str]: ...
    def hashCode(self) -> int: ...
    def isEmpty(self) -> bool: ...
    def remove(self, string: str) -> None: ...
    def set(self, string: str, string2: str) -> None: ...
    def size(self) -> int: ...
    def toString(self) -> str: ...

class MimeTypeParseException(java.lang.Exception):
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, string: str): ...

class Transferable:
    def getTransferData(self, dataFlavor: DataFlavor) -> _py_Any: ...
    def getTransferDataFlavors(self) -> _py_List[DataFlavor]: ...
    def isDataFlavorSupported(self, dataFlavor: DataFlavor) -> bool: ...

class UnsupportedFlavorException(java.lang.Exception):
    def __init__(self, dataFlavor: DataFlavor): ...

class FlavorTable(FlavorMap):
    def getFlavorsForNative(self, string: str) -> java.util.List[DataFlavor]: ...
    def getNativesForFlavor(self, dataFlavor: DataFlavor) -> java.util.List[str]: ...

class StringSelection(Transferable, ClipboardOwner):
    def __init__(self, string: str): ...
    def getTransferData(self, dataFlavor: DataFlavor) -> _py_Any: ...
    def getTransferDataFlavors(self) -> _py_List[DataFlavor]: ...
    def isDataFlavorSupported(self, dataFlavor: DataFlavor) -> bool: ...
    def lostOwnership(self, clipboard: Clipboard, transferable: Transferable) -> None: ...

class SystemFlavorMap(FlavorMap, FlavorTable):
    def addFlavorForUnencodedNative(self, string: str, dataFlavor: DataFlavor) -> None: ...
    def addUnencodedNativeForFlavor(self, dataFlavor: DataFlavor, string: str) -> None: ...
    @classmethod
    def decodeDataFlavor(cls, string: str) -> DataFlavor: ...
    @classmethod
    def decodeJavaMIMEType(cls, string: str) -> str: ...
    @classmethod
    def encodeDataFlavor(cls, dataFlavor: DataFlavor) -> str: ...
    @classmethod
    def encodeJavaMIMEType(cls, string: str) -> str: ...
    @classmethod
    def getDefaultFlavorMap(cls) -> FlavorMap: ...
    def getFlavorsForNative(self, string: str) -> java.util.List[DataFlavor]: ...
    def getFlavorsForNatives(self, stringArray: _py_List[str]) -> java.util.Map[str, DataFlavor]: ...
    def getNativesForFlavor(self, dataFlavor: DataFlavor) -> java.util.List[str]: ...
    def getNativesForFlavors(self, dataFlavorArray: _py_List[DataFlavor]) -> java.util.Map[DataFlavor, str]: ...
    @classmethod
    def isJavaMIMEType(cls, string: str) -> bool: ...
    def setFlavorsForNative(self, string: str, dataFlavorArray: _py_List[DataFlavor]) -> None: ...
    def setNativesForFlavor(self, dataFlavor: DataFlavor, stringArray: _py_List[str]) -> None: ...
