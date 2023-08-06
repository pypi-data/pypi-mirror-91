'''_2352.py

ConceptCouplingConnectionSystemDeflection
'''


from mastapy.system_model.connections_and_sockets.couplings import _1996
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6436
from mastapy.system_model.analyses_and_results.power_flows import _3689
from mastapy.system_model.analyses_and_results.system_deflections import _2364
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_CONNECTION_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ConceptCouplingConnectionSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingConnectionSystemDeflection',)


class ConceptCouplingConnectionSystemDeflection(_2364.CouplingConnectionSystemDeflection):
    '''ConceptCouplingConnectionSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_CONNECTION_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingConnectionSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1996.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1996.ConceptCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6436.ConceptCouplingConnectionLoadCase':
        '''ConceptCouplingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6436.ConceptCouplingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def power_flow_results(self) -> '_3689.ConceptCouplingConnectionPowerFlow':
        '''ConceptCouplingConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3689.ConceptCouplingConnectionPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
