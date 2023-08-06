﻿'''_4236.py

StraightBevelDiffGearSetCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.gears import _2128
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _4234, _4235, _4153
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4115
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'StraightBevelDiffGearSetCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetCompoundModalAnalysesAtSpeeds',)


class StraightBevelDiffGearSetCompoundModalAnalysesAtSpeeds(_4153.BevelGearSetCompoundModalAnalysesAtSpeeds):
    '''StraightBevelDiffGearSetCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetCompoundModalAnalysesAtSpeeds.TYPE'):
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
    def straight_bevel_diff_gears_compound_modal_analyses_at_speeds(self) -> 'List[_4234.StraightBevelDiffGearCompoundModalAnalysesAtSpeeds]':
        '''List[StraightBevelDiffGearCompoundModalAnalysesAtSpeeds]: 'StraightBevelDiffGearsCompoundModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsCompoundModalAnalysesAtSpeeds, constructor.new(_4234.StraightBevelDiffGearCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def straight_bevel_diff_meshes_compound_modal_analyses_at_speeds(self) -> 'List[_4235.StraightBevelDiffGearMeshCompoundModalAnalysesAtSpeeds]':
        '''List[StraightBevelDiffGearMeshCompoundModalAnalysesAtSpeeds]: 'StraightBevelDiffMeshesCompoundModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesCompoundModalAnalysesAtSpeeds, constructor.new(_4235.StraightBevelDiffGearMeshCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4115.StraightBevelDiffGearSetModalAnalysesAtSpeeds]':
        '''List[StraightBevelDiffGearSetModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4115.StraightBevelDiffGearSetModalAnalysesAtSpeeds))
        return value

    @property
    def assembly_modal_analyses_at_speeds_load_cases(self) -> 'List[_4115.StraightBevelDiffGearSetModalAnalysesAtSpeeds]':
        '''List[StraightBevelDiffGearSetModalAnalysesAtSpeeds]: 'AssemblyModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysesAtSpeedsLoadCases, constructor.new(_4115.StraightBevelDiffGearSetModalAnalysesAtSpeeds))
        return value
