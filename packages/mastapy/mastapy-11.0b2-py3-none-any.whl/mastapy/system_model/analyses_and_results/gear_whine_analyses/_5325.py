﻿'''_5325.py

ConceptCouplingGearWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2159
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6124
from mastapy.system_model.analyses_and_results.system_deflections import _2278
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5336
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'ConceptCouplingGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingGearWhineAnalysis',)


class ConceptCouplingGearWhineAnalysis(_5336.CouplingGearWhineAnalysis):
    '''ConceptCouplingGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingGearWhineAnalysis.TYPE'):
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
    def system_deflection_results(self) -> '_2278.ConceptCouplingSystemDeflection':
        '''ConceptCouplingSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2278.ConceptCouplingSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
