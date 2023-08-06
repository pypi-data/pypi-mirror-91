﻿'''_5802.py

ShaftCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.shaft_model import _2065
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5409
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5716
from mastapy._internal.python_net import python_net_import

_SHAFT_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'ShaftCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftCompoundGearWhineAnalysis',)


class ShaftCompoundGearWhineAnalysis(_5716.AbstractShaftOrHousingCompoundGearWhineAnalysis):
    '''ShaftCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SHAFT_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2065.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2065.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5409.ShaftGearWhineAnalysis]':
        '''List[ShaftGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5409.ShaftGearWhineAnalysis))
        return value

    @property
    def component_gear_whine_analysis_load_cases(self) -> 'List[_5409.ShaftGearWhineAnalysis]':
        '''List[ShaftGearWhineAnalysis]: 'ComponentGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentGearWhineAnalysisLoadCases, constructor.new(_5409.ShaftGearWhineAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[ShaftCompoundGearWhineAnalysis]':
        '''List[ShaftCompoundGearWhineAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftCompoundGearWhineAnalysis))
        return value
