﻿'''_4225.py

ShaftHubConnectionCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2175
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4102
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _4171
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'ShaftHubConnectionCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionCompoundModalAnalysesAtSpeeds',)


class ShaftHubConnectionCompoundModalAnalysesAtSpeeds(_4171.ConnectorCompoundModalAnalysesAtSpeeds):
    '''ShaftHubConnectionCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _SHAFT_HUB_CONNECTION_COMPOUND_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2175.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2175.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4102.ShaftHubConnectionModalAnalysesAtSpeeds]':
        '''List[ShaftHubConnectionModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4102.ShaftHubConnectionModalAnalysesAtSpeeds))
        return value

    @property
    def component_modal_analyses_at_speeds_load_cases(self) -> 'List[_4102.ShaftHubConnectionModalAnalysesAtSpeeds]':
        '''List[ShaftHubConnectionModalAnalysesAtSpeeds]: 'ComponentModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtSpeedsLoadCases, constructor.new(_4102.ShaftHubConnectionModalAnalysesAtSpeeds))
        return value

    @property
    def planetaries(self) -> 'List[ShaftHubConnectionCompoundModalAnalysesAtSpeeds]':
        '''List[ShaftHubConnectionCompoundModalAnalysesAtSpeeds]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftHubConnectionCompoundModalAnalysesAtSpeeds))
        return value
