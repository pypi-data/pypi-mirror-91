﻿'''_3855.py

RollingRingModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2173
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6221
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3803
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'RollingRingModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingModalAnalysesAtStiffnesses',)


class RollingRingModalAnalysesAtStiffnesses(_3803.CouplingHalfModalAnalysesAtStiffnesses):
    '''RollingRingModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2173.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2173.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6221.RollingRingLoadCase':
        '''RollingRingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6221.RollingRingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[RollingRingModalAnalysesAtStiffnesses]':
        '''List[RollingRingModalAnalysesAtStiffnesses]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingModalAnalysesAtStiffnesses))
        return value
