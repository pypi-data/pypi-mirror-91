﻿'''_4289.py

PowerLoadModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model import _2120
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6535
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4324
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'PowerLoadModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadModalAnalysisAtAStiffness',)


class PowerLoadModalAnalysisAtAStiffness(_4324.VirtualComponentModalAnalysisAtAStiffness):
    '''PowerLoadModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2120.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2120.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6535.PowerLoadLoadCase':
        '''PowerLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6535.PowerLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
