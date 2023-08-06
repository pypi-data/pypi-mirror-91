﻿'''_4696.py

StraightBevelDiffGearSetCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2192
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4694, _4695, _4607
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4567
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'StraightBevelDiffGearSetCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetCompoundModalAnalysisAtASpeed',)


class StraightBevelDiffGearSetCompoundModalAnalysisAtASpeed(_4607.BevelGearSetCompoundModalAnalysisAtASpeed):
    '''StraightBevelDiffGearSetCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2192.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2192.StraightBevelDiffGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2192.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2192.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def straight_bevel_diff_gears_compound_modal_analysis_at_a_speed(self) -> 'List[_4694.StraightBevelDiffGearCompoundModalAnalysisAtASpeed]':
        '''List[StraightBevelDiffGearCompoundModalAnalysisAtASpeed]: 'StraightBevelDiffGearsCompoundModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsCompoundModalAnalysisAtASpeed, constructor.new(_4694.StraightBevelDiffGearCompoundModalAnalysisAtASpeed))
        return value

    @property
    def straight_bevel_diff_meshes_compound_modal_analysis_at_a_speed(self) -> 'List[_4695.StraightBevelDiffGearMeshCompoundModalAnalysisAtASpeed]':
        '''List[StraightBevelDiffGearMeshCompoundModalAnalysisAtASpeed]: 'StraightBevelDiffMeshesCompoundModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesCompoundModalAnalysisAtASpeed, constructor.new(_4695.StraightBevelDiffGearMeshCompoundModalAnalysisAtASpeed))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4567.StraightBevelDiffGearSetModalAnalysisAtASpeed]':
        '''List[StraightBevelDiffGearSetModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4567.StraightBevelDiffGearSetModalAnalysisAtASpeed))
        return value

    @property
    def assembly_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4567.StraightBevelDiffGearSetModalAnalysisAtASpeed]':
        '''List[StraightBevelDiffGearSetModalAnalysisAtASpeed]: 'AssemblyModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisAtASpeedLoadCases, constructor.new(_4567.StraightBevelDiffGearSetModalAnalysisAtASpeed))
        return value
