﻿'''_3805.py

CriticalSpeedAnalysis
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3839
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.analysis_cases import _6547
from mastapy._internal.python_net import python_net_import

_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'CriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CriticalSpeedAnalysis',)


class CriticalSpeedAnalysis(_6547.StaticLoadAnalysisCase):
    '''CriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def modal_analyses_at_stiffnesses_options(self) -> '_3839.ModalAnalysesAtStiffnessesOptions':
        '''ModalAnalysesAtStiffnessesOptions: 'ModalAnalysesAtStiffnessesOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3839.ModalAnalysesAtStiffnessesOptions)(self.wrapped.ModalAnalysesAtStiffnessesOptions) if self.wrapped.ModalAnalysesAtStiffnessesOptions else None
