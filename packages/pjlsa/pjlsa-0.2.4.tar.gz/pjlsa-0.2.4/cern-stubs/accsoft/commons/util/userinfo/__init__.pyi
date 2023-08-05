from typing import Any as _py_Any
from typing import ClassVar as _py_ClassVar


class Constants:
    OUT_ENCODING: _py_ClassVar[str] = ...
    TRUST_PASSWD: _py_ClassVar[str] = ...
    TRUSTSTORE_TYPE: _py_ClassVar[str] = ...
    IS_WINDOWS: _py_ClassVar[bool] = ...
    DATA_PATH: _py_ClassVar[str] = ...
    DATA_URL: _py_ClassVar[str] = ...
    CONNECT_TIMEOUT: _py_ClassVar[int] = ...

class NiceUser:
    def __init__(self, int: int, int2: int, string: str, string2: str, string3: str, string4: str, string5: str, string6: str, string7: str, string8: str): ...
    def equals(self, object: _py_Any) -> bool: ...
    def getCCID(self) -> int: ...
    def getCompany(self) -> str: ...
    def getDepartment(self) -> str: ...
    def getEmail(self) -> str: ...
    def getFirstName(self) -> str: ...
    def getFullName(self) -> str: ...
    def getLastName(self) -> str: ...
    def getLogin(self) -> str: ...
    def getPhone(self) -> str: ...
    def getRespCCID(self) -> int: ...
    def hashCode(self) -> int: ...
    def toString(self) -> str: ...
