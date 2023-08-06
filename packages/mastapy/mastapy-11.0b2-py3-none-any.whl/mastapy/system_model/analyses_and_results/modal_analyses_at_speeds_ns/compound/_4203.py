﻿'''_4203.py

KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.gears import _2122
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4080
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _4197
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysesAtSpeeds',)


class KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysesAtSpeeds(_4197.KlingelnbergCycloPalloidConicalGearCompoundModalAnalysesAtSpeeds):
    '''KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_COMPOUND_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2122.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2122.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4080.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysesAtSpeeds]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4080.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysesAtSpeeds))
        return value

    @property
    def component_modal_analyses_at_speeds_load_cases(self) -> 'List[_4080.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysesAtSpeeds]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearModalAnalysesAtSpeeds]: 'ComponentModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtSpeedsLoadCases, constructor.new(_4080.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysesAtSpeeds))
        return value
