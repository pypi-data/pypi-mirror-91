﻿'''_3990.py

StraightBevelDiffGearSetCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.gears import _2128
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _3988, _3989, _3907
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3869
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'StraightBevelDiffGearSetCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetCompoundModalAnalysesAtStiffnesses',)


class StraightBevelDiffGearSetCompoundModalAnalysesAtStiffnesses(_3907.BevelGearSetCompoundModalAnalysesAtStiffnesses):
    '''StraightBevelDiffGearSetCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2128.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2128.StraightBevelDiffGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2128.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2128.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def straight_bevel_diff_gears_compound_modal_analyses_at_stiffnesses(self) -> 'List[_3988.StraightBevelDiffGearCompoundModalAnalysesAtStiffnesses]':
        '''List[StraightBevelDiffGearCompoundModalAnalysesAtStiffnesses]: 'StraightBevelDiffGearsCompoundModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsCompoundModalAnalysesAtStiffnesses, constructor.new(_3988.StraightBevelDiffGearCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def straight_bevel_diff_meshes_compound_modal_analyses_at_stiffnesses(self) -> 'List[_3989.StraightBevelDiffGearMeshCompoundModalAnalysesAtStiffnesses]':
        '''List[StraightBevelDiffGearMeshCompoundModalAnalysesAtStiffnesses]: 'StraightBevelDiffMeshesCompoundModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesCompoundModalAnalysesAtStiffnesses, constructor.new(_3989.StraightBevelDiffGearMeshCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3869.StraightBevelDiffGearSetModalAnalysesAtStiffnesses]':
        '''List[StraightBevelDiffGearSetModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3869.StraightBevelDiffGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def assembly_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_3869.StraightBevelDiffGearSetModalAnalysesAtStiffnesses]':
        '''List[StraightBevelDiffGearSetModalAnalysesAtStiffnesses]: 'AssemblyModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysesAtStiffnessesLoadCases, constructor.new(_3869.StraightBevelDiffGearSetModalAnalysesAtStiffnesses))
        return value
