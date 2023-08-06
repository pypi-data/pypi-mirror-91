﻿'''_3972.py

PowerLoadCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model import _2056
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3851
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _4005
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'PowerLoadCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadCompoundModalAnalysesAtStiffnesses',)


class PowerLoadCompoundModalAnalysesAtStiffnesses(_4005.VirtualComponentCompoundModalAnalysesAtStiffnesses):
    '''PowerLoadCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2056.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2056.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3851.PowerLoadModalAnalysesAtStiffnesses]':
        '''List[PowerLoadModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3851.PowerLoadModalAnalysesAtStiffnesses))
        return value

    @property
    def component_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_3851.PowerLoadModalAnalysesAtStiffnesses]':
        '''List[PowerLoadModalAnalysesAtStiffnesses]: 'ComponentModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysesAtStiffnessesLoadCases, constructor.new(_3851.PowerLoadModalAnalysesAtStiffnesses))
        return value
