﻿'''_3858.py

ShaftModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.shaft_model import _2065
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6224
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3768
from mastapy._internal.python_net import python_net_import

_SHAFT_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'ShaftModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftModalAnalysesAtStiffnesses',)


class ShaftModalAnalysesAtStiffnesses(_3768.AbstractShaftOrHousingModalAnalysesAtStiffnesses):
    '''ShaftModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _SHAFT_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftModalAnalysesAtStiffnesses.TYPE'):
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
    def component_load_case(self) -> '_6224.ShaftLoadCase':
        '''ShaftLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6224.ShaftLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[ShaftModalAnalysesAtStiffnesses]':
        '''List[ShaftModalAnalysesAtStiffnesses]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftModalAnalysesAtStiffnesses))
        return value
