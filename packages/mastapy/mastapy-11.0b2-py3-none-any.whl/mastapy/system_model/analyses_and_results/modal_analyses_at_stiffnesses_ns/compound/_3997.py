﻿'''_3997.py

SynchroniserHalfCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2180
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3875
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _3998
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'SynchroniserHalfCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfCompoundModalAnalysesAtStiffnesses',)


class SynchroniserHalfCompoundModalAnalysesAtStiffnesses(_3998.SynchroniserPartCompoundModalAnalysesAtStiffnesses):
    '''SynchroniserHalfCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2180.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2180.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3875.SynchroniserHalfModalAnalysesAtStiffnesses]':
        '''List[SynchroniserHalfModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3875.SynchroniserHalfModalAnalysesAtStiffnesses))
        return value

    @property
    def component_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_3875.SynchroniserHalfModalAnalysesAtStiffnesses]':
        '''List[SynchroniserHalfModalAnalysesAtStiffnesses]: 'ComponentModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtStiffnessesLoadCases, constructor.new(_3875.SynchroniserHalfModalAnalysesAtStiffnesses))
        return value
