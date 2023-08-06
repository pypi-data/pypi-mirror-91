﻿'''_3889.py

ZerolBevelGearModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model.gears import _2135
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6262
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3782
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'ZerolBevelGearModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearModalAnalysesAtStiffnesses',)


class ZerolBevelGearModalAnalysesAtStiffnesses(_3782.BevelGearModalAnalysesAtStiffnesses):
    '''ZerolBevelGearModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2135.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2135.ZerolBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6262.ZerolBevelGearLoadCase':
        '''ZerolBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6262.ZerolBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
