﻿'''_4129.py

UnbalancedMassModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model import _2061
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6257
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4130
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'UnbalancedMassModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassModalAnalysesAtSpeeds',)


class UnbalancedMassModalAnalysesAtSpeeds(_4130.VirtualComponentModalAnalysesAtSpeeds):
    '''UnbalancedMassModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2061.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2061.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6257.UnbalancedMassLoadCase':
        '''UnbalancedMassLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6257.UnbalancedMassLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
