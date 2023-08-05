from typing import Any as _py_Any
import cern.accsoft.commons.domain.particletransfers
import cern.lsa.domain.settings
import java.io


class ParameterTypeRelation:
    @classmethod
    def builder(cls) -> 'DefaultParameterTypeRelation.Builder': ...
    def getDependentParameterType(self) -> cern.lsa.domain.settings.ParameterType: ...
    def getParticleTransfer(self) -> cern.accsoft.commons.domain.particletransfers.ParticleTransfer: ...
    def getSourceParameterType(self) -> cern.lsa.domain.settings.ParameterType: ...

class ParameterTypeRelationInfo:
    @classmethod
    def builder(cls) -> 'DefaultParameterTypeRelationInfo.Builder': ...
    def getMakeRuleName(self) -> str: ...
    def getParameterTypeRelation(self) -> ParameterTypeRelation: ...

class ParameterTypeRelationInfosRequest:
    @classmethod
    def all(cls) -> 'ParameterTypeRelationInfosRequest': ...
    @classmethod
    def builder(cls) -> 'DefaultParameterTypeRelationInfosRequest.Builder': ...
    @classmethod
    def byMakeRuleName(cls, string: str) -> 'ParameterTypeRelationInfosRequest': ...
    @classmethod
    def byParticleTransfer(cls, particleTransfer: cern.accsoft.commons.domain.particletransfers.ParticleTransfer) -> 'ParameterTypeRelationInfosRequest': ...
    def getMakeRuleName(self) -> str: ...
    def getParticleTransfer(self) -> cern.accsoft.commons.domain.particletransfers.ParticleTransfer: ...

class DefaultParameterTypeRelation(ParameterTypeRelation, java.io.Serializable):
    @classmethod
    def builder(cls) -> 'DefaultParameterTypeRelation.Builder': ...
    @classmethod
    def copyOf(cls, parameterTypeRelation: ParameterTypeRelation) -> 'DefaultParameterTypeRelation': ...
    def equals(self, object: _py_Any) -> bool: ...
    def getDependentParameterType(self) -> cern.lsa.domain.settings.ParameterType: ...
    def getParticleTransfer(self) -> cern.accsoft.commons.domain.particletransfers.ParticleTransfer: ...
    def getSourceParameterType(self) -> cern.lsa.domain.settings.ParameterType: ...
    def hashCode(self) -> int: ...
    def toString(self) -> str: ...
    def withDependentParameterType(self, parameterType: cern.lsa.domain.settings.ParameterType) -> 'DefaultParameterTypeRelation': ...
    def withParticleTransfer(self, particleTransfer: cern.accsoft.commons.domain.particletransfers.ParticleTransfer) -> 'DefaultParameterTypeRelation': ...
    def withSourceParameterType(self, parameterType: cern.lsa.domain.settings.ParameterType) -> 'DefaultParameterTypeRelation': ...
    class Builder:
        def build(self) -> 'DefaultParameterTypeRelation': ...
        def dependentParameterType(self, parameterType: cern.lsa.domain.settings.ParameterType) -> 'DefaultParameterTypeRelation.Builder': ...
        def particleTransfer(self, particleTransfer: cern.accsoft.commons.domain.particletransfers.ParticleTransfer) -> 'DefaultParameterTypeRelation.Builder': ...
        def sourceParameterType(self, parameterType: cern.lsa.domain.settings.ParameterType) -> 'DefaultParameterTypeRelation.Builder': ...

class DefaultParameterTypeRelationInfo(ParameterTypeRelationInfo, java.io.Serializable):
    @classmethod
    def builder(cls) -> 'DefaultParameterTypeRelationInfo.Builder': ...
    @classmethod
    def copyOf(cls, parameterTypeRelationInfo: ParameterTypeRelationInfo) -> 'DefaultParameterTypeRelationInfo': ...
    def equals(self, object: _py_Any) -> bool: ...
    def getMakeRuleName(self) -> str: ...
    def getParameterTypeRelation(self) -> ParameterTypeRelation: ...
    def hashCode(self) -> int: ...
    def toString(self) -> str: ...
    def withMakeRuleName(self, string: str) -> 'DefaultParameterTypeRelationInfo': ...
    def withParameterTypeRelation(self, parameterTypeRelation: ParameterTypeRelation) -> 'DefaultParameterTypeRelationInfo': ...
    class Builder:
        def build(self) -> 'DefaultParameterTypeRelationInfo': ...
        def makeRuleName(self, string: str) -> 'DefaultParameterTypeRelationInfo.Builder': ...
        def parameterTypeRelation(self, parameterTypeRelation: ParameterTypeRelation) -> 'DefaultParameterTypeRelationInfo.Builder': ...

class DefaultParameterTypeRelationInfosRequest(ParameterTypeRelationInfosRequest, java.io.Serializable):
    @classmethod
    def builder(cls) -> 'DefaultParameterTypeRelationInfosRequest.Builder': ...
    @classmethod
    def copyOf(cls, parameterTypeRelationInfosRequest: ParameterTypeRelationInfosRequest) -> 'DefaultParameterTypeRelationInfosRequest': ...
    def equals(self, object: _py_Any) -> bool: ...
    def getMakeRuleName(self) -> str: ...
    def getParticleTransfer(self) -> cern.accsoft.commons.domain.particletransfers.ParticleTransfer: ...
    def hashCode(self) -> int: ...
    def toString(self) -> str: ...
    def withMakeRuleName(self, string: str) -> 'DefaultParameterTypeRelationInfosRequest': ...
    def withParticleTransfer(self, particleTransfer: cern.accsoft.commons.domain.particletransfers.ParticleTransfer) -> 'DefaultParameterTypeRelationInfosRequest': ...
    class Builder:
        def build(self) -> 'DefaultParameterTypeRelationInfosRequest': ...
        def makeRuleName(self, string: str) -> 'DefaultParameterTypeRelationInfosRequest.Builder': ...
        def particleTransfer(self, particleTransfer: cern.accsoft.commons.domain.particletransfers.ParticleTransfer) -> 'DefaultParameterTypeRelationInfosRequest.Builder': ...
