﻿'''_5744.py

ConceptGearSetCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2104
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5742, _5743, _5768
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5329
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'ConceptGearSetCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetCompoundGearWhineAnalysis',)


class ConceptGearSetCompoundGearWhineAnalysis(_5768.GearSetCompoundGearWhineAnalysis):
    '''ConceptGearSetCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2104.ConceptGearSet':
        '''ConceptGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2104.ConceptGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2104.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2104.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def concept_gears_compound_gear_whine_analysis(self) -> 'List[_5742.ConceptGearCompoundGearWhineAnalysis]':
        '''List[ConceptGearCompoundGearWhineAnalysis]: 'ConceptGearsCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsCompoundGearWhineAnalysis, constructor.new(_5742.ConceptGearCompoundGearWhineAnalysis))
        return value

    @property
    def concept_meshes_compound_gear_whine_analysis(self) -> 'List[_5743.ConceptGearMeshCompoundGearWhineAnalysis]':
        '''List[ConceptGearMeshCompoundGearWhineAnalysis]: 'ConceptMeshesCompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesCompoundGearWhineAnalysis, constructor.new(_5743.ConceptGearMeshCompoundGearWhineAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5329.ConceptGearSetGearWhineAnalysis]':
        '''List[ConceptGearSetGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5329.ConceptGearSetGearWhineAnalysis))
        return value

    @property
    def assembly_gear_whine_analysis_load_cases(self) -> 'List[_5329.ConceptGearSetGearWhineAnalysis]':
        '''List[ConceptGearSetGearWhineAnalysis]: 'AssemblyGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyGearWhineAnalysisLoadCases, constructor.new(_5329.ConceptGearSetGearWhineAnalysis))
        return value
