from typing import Any as _py_Any
from typing import List as _py_List
from typing import TypeVar as _py_TypeVar
from typing import Type as _py_Type
from typing import ClassVar as _py_ClassVar
from typing import Generic as _py_Generic
from typing import overload
import cern.rbac.common
import cern.rbac.common.authorization
import java.lang
import java.util


class AbstractRequest(java.lang.Cloneable):
    def __init__(self): ...
    def clone(self) -> _py_Any: ...
    def getParameters(self) -> java.util.Map['RequestParameterType', _py_Any]: ...
    def getServletSuffix(self) -> str: ...
    def getVersion(self) -> str: ...
    def isVerbose(self) -> bool: ...
    def toString(self) -> str: ...

class AccessMapCommand(java.lang.Enum['AccessMapCommand']):
    MAPS_FOR_SERVER: _py_ClassVar['AccessMapCommand'] = ...
    MAPS_FOR_CLASS: _py_ClassVar['AccessMapCommand'] = ...
    MAPS_FOR_CLASS_TEST: _py_ClassVar['AccessMapCommand'] = ...
    MAPS_FOR_FRONT_END: _py_ClassVar['AccessMapCommand'] = ...
    @classmethod
    def fromString(cls, string: str) -> 'AccessMapCommand': ...
    def getBunchSize(self) -> int: ...
    def getName(self) -> str: ...
    def getScriptName(self) -> str: ...
    def toString(self) -> str: ...
    @classmethod
    @overload
    def valueOf(cls, string: str) -> 'AccessMapCommand': ...
    _valueOf_1__T = _py_TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @classmethod
    @overload
    def valueOf(cls, class_: _py_Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
    @classmethod
    def values(cls) -> _py_List['AccessMapCommand']: ...

_RequestBuilder__Request = _py_TypeVar('_RequestBuilder__Request', bound=AbstractRequest)  # <Request>
class RequestBuilder(_py_Generic[_RequestBuilder__Request]):
    def __init__(self, request: _RequestBuilder__Request): ...
    def addParameters(self, map: java.util.Map['RequestParameterType', _py_Any]) -> None: ...
    def buildRequest(self) -> _RequestBuilder__Request: ...
    def setVerbose(self, boolean: bool) -> 'RequestBuilder'[_RequestBuilder__Request]: ...
    def setVersion(self, string: str) -> 'RequestBuilder'[_RequestBuilder__Request]: ...

class RequestParameterType(java.lang.Enum['RequestParameterType']):
    SERVER_ADDR_SUFFIX: _py_ClassVar['RequestParameterType'] = ...
    APPLICATION: _py_ClassVar['RequestParameterType'] = ...
    APPLICATION_ID: _py_ClassVar['RequestParameterType'] = ...
    TOKEN_FORMAT: _py_ClassVar['RequestParameterType'] = ...
    TOKEN_TYPE: _py_ClassVar['RequestParameterType'] = ...
    LIFETIME: _py_ClassVar['RequestParameterType'] = ...
    ACCOUNT_NAME: _py_ClassVar['RequestParameterType'] = ...
    USER_NAME: _py_ClassVar['RequestParameterType'] = ...
    PASSWORD: _py_ClassVar['RequestParameterType'] = ...
    ORIGIN: _py_ClassVar['RequestParameterType'] = ...
    ROLE: _py_ClassVar['RequestParameterType'] = ...
    TOKEN: _py_ClassVar['RequestParameterType'] = ...
    SIGN_BUFFER: _py_ClassVar['RequestParameterType'] = ...
    VERBOSE: _py_ClassVar['RequestParameterType'] = ...
    BUILD: _py_ClassVar['RequestParameterType'] = ...
    PARAMETER: _py_ClassVar['RequestParameterType'] = ...
    CLASS: _py_ClassVar['RequestParameterType'] = ...
    DEVICE: _py_ClassVar['RequestParameterType'] = ...
    PROPERTY: _py_ClassVar['RequestParameterType'] = ...
    OPERATION: _py_ClassVar['RequestParameterType'] = ...
    MCS_ROLE: _py_ClassVar['RequestParameterType'] = ...
    VERSION: _py_ClassVar['RequestParameterType'] = ...
    SAML_RESPONSE: _py_ClassVar['RequestParameterType'] = ...
    KRB5_TICKET: _py_ClassVar['RequestParameterType'] = ...
    CHECKING_POLICY: _py_ClassVar['RequestParameterType'] = ...
    @classmethod
    def fromString(cls, string: str) -> 'RequestParameterType': ...
    def getName(self) -> str: ...
    @classmethod
    @overload
    def valueOf(cls, string: str) -> 'RequestParameterType': ...
    _valueOf_1__T = _py_TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @classmethod
    @overload
    def valueOf(cls, class_: _py_Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
    @classmethod
    def values(cls) -> _py_List['RequestParameterType']: ...

class ServerErrorCode(java.lang.Enum['ServerErrorCode']):
    BAD_REQUEST: _py_ClassVar['ServerErrorCode'] = ...
    AUTHENTICATION_FAILED: _py_ClassVar['ServerErrorCode'] = ...
    PROCESSING_ERROR: _py_ClassVar['ServerErrorCode'] = ...
    @classmethod
    def fromInt(cls, int: int) -> 'ServerErrorCode': ...
    def getCode(self) -> int: ...
    @classmethod
    @overload
    def valueOf(cls, string: str) -> 'ServerErrorCode': ...
    _valueOf_1__T = _py_TypeVar('_valueOf_1__T', bound=java.lang.Enum)  # <T>
    @classmethod
    @overload
    def valueOf(cls, class_: _py_Type[_valueOf_1__T], string: str) -> _valueOf_1__T: ...
    @classmethod
    def values(cls) -> _py_List['ServerErrorCode']: ...

class AccessCheckerRequest(AbstractRequest):
    def __init__(self): ...
    def getCheckingPolicy(self) -> cern.rbac.common.authorization.CheckingPolicy: ...
    def getDevice(self) -> str: ...
    def getDeviceClass(self) -> str: ...
    def getOperation(self) -> cern.rbac.common.authorization.Operation: ...
    def getProperty(self) -> str: ...
    def getToken(self) -> cern.rbac.common.RbaToken: ...

class AccessCheckerRequestBuilder(RequestBuilder[AccessCheckerRequest]):
    @overload
    def buildRequest(self) -> AbstractRequest: ...
    @overload
    def buildRequest(self) -> AccessCheckerRequest: ...
    @classmethod
    def newInstance(cls) -> 'AccessCheckerRequestBuilder': ...
    def setCheckingPolicy(self, checkingPolicy: cern.rbac.common.authorization.CheckingPolicy) -> 'AccessCheckerRequestBuilder': ...
    def setDevice(self, string: str) -> 'AccessCheckerRequestBuilder': ...
    def setDeviceClass(self, string: str) -> 'AccessCheckerRequestBuilder': ...
    def setOperation(self, operation: cern.rbac.common.authorization.Operation) -> 'AccessCheckerRequestBuilder': ...
    def setProperty(self, string: str) -> 'AccessCheckerRequestBuilder': ...
    def setToken(self, rbaToken: cern.rbac.common.RbaToken) -> 'AccessCheckerRequestBuilder': ...

class AccessMapRequest(AbstractRequest):
    def __init__(self): ...
    def getCommand(self) -> AccessMapCommand: ...
    def getParameter(self) -> str: ...
    def getToken(self) -> cern.rbac.common.RbaToken: ...

class AccessMapRequestBuilder(RequestBuilder[AccessMapRequest]):
    @overload
    def buildRequest(self) -> AbstractRequest: ...
    @overload
    def buildRequest(self) -> AccessMapRequest: ...
    @classmethod
    def newInstance(cls) -> 'AccessMapRequestBuilder': ...
    def setCommand(self, accessMapCommand: AccessMapCommand) -> 'AccessMapRequestBuilder': ...
    def setParameter(self, string: str) -> 'AccessMapRequestBuilder': ...
    def setToken(self, rbaToken: cern.rbac.common.RbaToken) -> 'AccessMapRequestBuilder': ...

class AuthenticationRequest(AbstractRequest):
    def __init__(self): ...
    def getAccountName(self) -> str: ...
    def getApplication(self) -> str: ...
    def getKerberosTicket(self) -> str: ...
    def getLifetime(self) -> int: ...
    def getOrigin(self) -> cern.rbac.common.RbaToken: ...
    def getPassword(self) -> str: ...
    def getRoles(self) -> _py_List[str]: ...
    def getSamlResponse(self) -> str: ...
    def getTokenType(self) -> cern.rbac.common.TokenType: ...
    def getUserName(self) -> str: ...

class AuthenticationRequestBuilder(RequestBuilder[AuthenticationRequest]):
    @classmethod
    def newInstance(cls) -> 'AuthenticationRequestBuilder': ...
    def setAccountName(self, string: str) -> 'AuthenticationRequestBuilder': ...
    def setApplication(self, string: str) -> 'AuthenticationRequestBuilder': ...
    def setKerberosTicket(self, byteArray: _py_List[int]) -> 'AuthenticationRequestBuilder': ...
    def setLifetime(self, int: int) -> 'AuthenticationRequestBuilder': ...
    def setOrigin(self, rbaToken: cern.rbac.common.RbaToken) -> 'AuthenticationRequestBuilder': ...
    def setPassword(self, string: str) -> 'AuthenticationRequestBuilder': ...
    def setRoles(self, stringArray: _py_List[str]) -> 'AuthenticationRequestBuilder': ...
    def setSamlResponse(self, string: str) -> 'AuthenticationRequestBuilder': ...
    def setTokenType(self, tokenType: cern.rbac.common.TokenType) -> 'AuthenticationRequestBuilder': ...
    def setUserName(self, string: str) -> 'AuthenticationRequestBuilder': ...

class McsKeyRequest(AbstractRequest):
    def __init__(self): ...
    def getDevice(self) -> str: ...
    def getDeviceClass(self) -> str: ...
    def getMCSRole(self) -> str: ...
    def getProperty(self) -> str: ...

class McsKeyRequestBuilder(RequestBuilder[McsKeyRequest]):
    @overload
    def buildRequest(self) -> AbstractRequest: ...
    @overload
    def buildRequest(self) -> McsKeyRequest: ...
    @classmethod
    def newInstance(cls) -> 'McsKeyRequestBuilder': ...
    def setDevice(self, string: str) -> 'McsKeyRequestBuilder': ...
    def setDeviceClass(self, string: str) -> 'McsKeyRequestBuilder': ...
    def setMCSRole(self, string: str) -> 'McsKeyRequestBuilder': ...
    def setProperty(self, string: str) -> 'McsKeyRequestBuilder': ...

class McsSignRequest(AbstractRequest):
    def __init__(self): ...
    def getSignBuffer(self) -> _py_List[int]: ...
    def getToken(self) -> cern.rbac.common.RbaToken: ...

class McsSignRequestBuilder(RequestBuilder[McsSignRequest]):
    @overload
    def buildRequest(self) -> AbstractRequest: ...
    @overload
    def buildRequest(self) -> McsSignRequest: ...
    @classmethod
    def newInstance(cls) -> 'McsSignRequestBuilder': ...
    def setSignBuffer(self, byteArray: _py_List[int]) -> 'McsSignRequestBuilder': ...
    def setToken(self, rbaToken: cern.rbac.common.RbaToken) -> 'McsSignRequestBuilder': ...

class AccessCheckerRequestImpl(AccessCheckerRequest):
    def __init__(self): ...

class AccessMapRequestImpl(AccessMapRequest):
    def __init__(self): ...
    def setCommand(self, accessMapCommand: AccessMapCommand) -> None: ...
    def setParameter(self, string: str) -> None: ...
    def setToken(self, rbaToken: cern.rbac.common.RbaToken) -> None: ...

class AuthenticationRequestImpl(AuthenticationRequest): ...

class McsKeyRequestImpl(McsKeyRequest):
    def __init__(self): ...

class McsSignRequestImpl(McsSignRequest):
    def __init__(self): ...
