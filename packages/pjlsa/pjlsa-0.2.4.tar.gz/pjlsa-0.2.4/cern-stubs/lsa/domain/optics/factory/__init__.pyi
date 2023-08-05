from typing import overload
import cern.accsoft.commons.domain
import cern.accsoft.commons.domain.beams
import cern.accsoft.commons.domain.particletransfers
import cern.accsoft.commons.domain.zones
import cern.lsa.domain.optics
import com.google.common.collect
import java.util


class ElementsRequestBuilder:
    def __init__(self): ...
    def build(self) -> cern.lsa.domain.optics.ElementsRequest: ...
    @classmethod
    def byAcceleratorZone(cls, acceleratorZone: cern.accsoft.commons.domain.zones.AcceleratorZone) -> cern.lsa.domain.optics.ElementsRequest: ...
    @classmethod
    def byElementNames(cls, collection: java.util.Collection[str]) -> cern.lsa.domain.optics.ElementsRequest: ...
    @classmethod
    def byLogicalHwName(cls, string: str) -> cern.lsa.domain.optics.ElementsRequest: ...
    @classmethod
    def byLogicalHwNames(cls, collection: java.util.Collection[str]) -> cern.lsa.domain.optics.ElementsRequest: ...
    @classmethod
    def byParticleTransfer(cls, particleTransfer: cern.accsoft.commons.domain.particletransfers.ParticleTransfer) -> cern.lsa.domain.optics.ElementsRequest: ...
    @classmethod
    def byTypes(cls, collection: java.util.Collection[cern.lsa.domain.optics.ElementType]) -> cern.lsa.domain.optics.ElementsRequest: ...
    def excludeObsolete(self) -> 'ElementsRequestBuilder': ...
    def setAcceleratorZone(self, acceleratorZone: cern.accsoft.commons.domain.zones.AcceleratorZone) -> 'ElementsRequestBuilder': ...
    def setElementNames(self, collection: java.util.Collection[str]) -> 'ElementsRequestBuilder': ...
    def setLogicalHwNames(self, collection: java.util.Collection[str]) -> 'ElementsRequestBuilder': ...
    def setParticleTransfer(self, particleTransfer: cern.accsoft.commons.domain.particletransfers.ParticleTransfer) -> 'ElementsRequestBuilder': ...
    def setSteering(self) -> 'ElementsRequestBuilder': ...
    def setTypes(self, collection: java.util.Collection[cern.lsa.domain.optics.ElementType]) -> 'ElementsRequestBuilder': ...

class MeasuredTwissBuilder:
    def __init__(self, twiss: cern.lsa.domain.optics.Twiss, double: float, date: java.util.Date): ...
    def build(self) -> cern.lsa.domain.optics.MeasuredTwiss: ...
    def setAlfxError(self, double: float) -> 'MeasuredTwissBuilder': ...
    def setAlfxMeas(self, double: float) -> 'MeasuredTwissBuilder': ...
    def setAlfyError(self, double: float) -> 'MeasuredTwissBuilder': ...
    def setAlfyMeas(self, double: float) -> 'MeasuredTwissBuilder': ...
    def setBetxError(self, double: float) -> 'MeasuredTwissBuilder': ...
    def setBetxMeas(self, double: float) -> 'MeasuredTwissBuilder': ...
    def setBetyError(self, double: float) -> 'MeasuredTwissBuilder': ...
    def setBetyMeas(self, double: float) -> 'MeasuredTwissBuilder': ...
    def setDxError(self, double: float) -> 'MeasuredTwissBuilder': ...
    def setDxMeas(self, double: float) -> 'MeasuredTwissBuilder': ...
    def setDyError(self, double: float) -> 'MeasuredTwissBuilder': ...
    def setDyMeas(self, double: float) -> 'MeasuredTwissBuilder': ...
    def setMuxError(self, double: float) -> 'MeasuredTwissBuilder': ...
    def setMuxMeas(self, double: float) -> 'MeasuredTwissBuilder': ...
    def setMuyError(self, double: float) -> 'MeasuredTwissBuilder': ...
    def setMuyMeas(self, double: float) -> 'MeasuredTwissBuilder': ...

class OpticsRequestBuilder:
    def __init__(self): ...
    def build(self) -> cern.lsa.domain.optics.OpticsRequest: ...
    @classmethod
    def byAccelerator(cls, accelerator: cern.accsoft.commons.domain.Accelerator) -> cern.lsa.domain.optics.OpticsRequest: ...
    @classmethod
    def byBeamProcessTypeNames(cls, collection: java.util.Collection[str]) -> cern.lsa.domain.optics.OpticsRequest: ...
    @classmethod
    def byOpticIds(cls, collection: java.util.Collection[int]) -> cern.lsa.domain.optics.OpticsRequest: ...
    @classmethod
    def byParticleTransfer(cls, particleTransfer: cern.accsoft.commons.domain.particletransfers.ParticleTransfer) -> cern.lsa.domain.optics.OpticsRequest: ...
    def setAccelerator(self, accelerator: cern.accsoft.commons.domain.Accelerator) -> 'OpticsRequestBuilder': ...
    def setBeamProcessTypeNames(self, collection: java.util.Collection[str]) -> 'OpticsRequestBuilder': ...
    def setOpticIds(self, collection: java.util.Collection[int]) -> 'OpticsRequestBuilder': ...
    def setParticleTransfer(self, particleTransfer: cern.accsoft.commons.domain.particletransfers.ParticleTransfer) -> 'OpticsRequestBuilder': ...

class TwissesRequestBuilder:
    def __init__(self): ...
    def build(self) -> cern.lsa.domain.optics.TwissesRequest: ...
    @classmethod
    def byOpticName(cls, string: str) -> cern.lsa.domain.optics.TwissesRequest: ...
    def setBeam(self, beam: cern.accsoft.commons.domain.beams.Beam) -> 'TwissesRequestBuilder': ...
    def setElementNames(self, collection: java.util.Collection[str]) -> 'TwissesRequestBuilder': ...
    @overload
    def setElementPositionRange(self, range: com.google.common.collect.Range[float]) -> 'TwissesRequestBuilder': ...
    @overload
    def setElementPositionRange(self, double: float, double2: float) -> 'TwissesRequestBuilder': ...
    def setElementTypes(self, collection: java.util.Collection[cern.lsa.domain.optics.ElementType]) -> 'TwissesRequestBuilder': ...
    def setOpticName(self, string: str) -> 'TwissesRequestBuilder': ...
