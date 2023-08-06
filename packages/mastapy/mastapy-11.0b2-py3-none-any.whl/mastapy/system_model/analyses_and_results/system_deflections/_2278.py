﻿'''_2278.py

ConceptCouplingSystemDeflection
'''


from mastapy.system_model.part_model.couplings import _2159
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6124
from mastapy.system_model.analyses_and_results.power_flows import _3288
from mastapy.system_model.analyses_and_results.system_deflections import _2290
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ConceptCouplingSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingSystemDeflection',)


class ConceptCouplingSystemDeflection(_2290.CouplingSystemDeflection):
    '''ConceptCouplingSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2159.ConceptCoupling':
        '''ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2159.ConceptCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6124.ConceptCouplingLoadCase':
        '''ConceptCouplingLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6124.ConceptCouplingLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def power_flow_results(self) -> '_3288.ConceptCouplingPowerFlow':
        '''ConceptCouplingPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3288.ConceptCouplingPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
