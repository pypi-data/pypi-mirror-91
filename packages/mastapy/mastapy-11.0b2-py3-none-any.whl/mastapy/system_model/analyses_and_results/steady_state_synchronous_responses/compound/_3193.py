﻿'''_3193.py

ImportedFEComponentCompoundSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model import _2042
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3069
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3136
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_COMPONENT_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'ImportedFEComponentCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEComponentCompoundSteadyStateSynchronousResponse',)


class ImportedFEComponentCompoundSteadyStateSynchronousResponse(_3136.AbstractShaftOrHousingCompoundSteadyStateSynchronousResponse):
    '''ImportedFEComponentCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_COMPONENT_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEComponentCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2042.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2042.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3069.ImportedFEComponentSteadyStateSynchronousResponse]':
        '''List[ImportedFEComponentSteadyStateSynchronousResponse]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3069.ImportedFEComponentSteadyStateSynchronousResponse))
        return value

    @property
    def component_steady_state_synchronous_response_load_cases(self) -> 'List[_3069.ImportedFEComponentSteadyStateSynchronousResponse]':
        '''List[ImportedFEComponentSteadyStateSynchronousResponse]: 'ComponentSteadyStateSynchronousResponseLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSteadyStateSynchronousResponseLoadCases, constructor.new(_3069.ImportedFEComponentSteadyStateSynchronousResponse))
        return value

    @property
    def planetaries(self) -> 'List[ImportedFEComponentCompoundSteadyStateSynchronousResponse]':
        '''List[ImportedFEComponentCompoundSteadyStateSynchronousResponse]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ImportedFEComponentCompoundSteadyStateSynchronousResponse))
        return value
