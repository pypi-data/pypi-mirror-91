﻿'''_4353.py

SpiralBevelGearSetModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.gears import _2126
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6230
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4352, _4351, _4274
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'SpiralBevelGearSetModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetModalAnalysisAtAStiffness',)


class SpiralBevelGearSetModalAnalysisAtAStiffness(_4274.BevelGearSetModalAnalysisAtAStiffness):
    '''SpiralBevelGearSetModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2126.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2126.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6230.SpiralBevelGearSetLoadCase':
        '''SpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6230.SpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def spiral_bevel_gears_modal_analysis_at_a_stiffness(self) -> 'List[_4352.SpiralBevelGearModalAnalysisAtAStiffness]':
        '''List[SpiralBevelGearModalAnalysisAtAStiffness]: 'SpiralBevelGearsModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsModalAnalysisAtAStiffness, constructor.new(_4352.SpiralBevelGearModalAnalysisAtAStiffness))
        return value

    @property
    def spiral_bevel_meshes_modal_analysis_at_a_stiffness(self) -> 'List[_4351.SpiralBevelGearMeshModalAnalysisAtAStiffness]':
        '''List[SpiralBevelGearMeshModalAnalysisAtAStiffness]: 'SpiralBevelMeshesModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesModalAnalysisAtAStiffness, constructor.new(_4351.SpiralBevelGearMeshModalAnalysisAtAStiffness))
        return value
