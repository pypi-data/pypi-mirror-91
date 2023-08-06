﻿'''_3886.py

WormGearModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model.gears import _2133
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6259
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3820
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'WormGearModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearModalAnalysesAtStiffnesses',)


class WormGearModalAnalysesAtStiffnesses(_3820.GearModalAnalysesAtStiffnesses):
    '''WormGearModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2133.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2133.WormGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6259.WormGearLoadCase':
        '''WormGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6259.WormGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
