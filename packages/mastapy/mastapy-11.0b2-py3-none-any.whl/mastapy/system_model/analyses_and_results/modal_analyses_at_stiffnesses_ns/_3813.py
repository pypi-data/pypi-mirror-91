﻿'''_3813.py

DatumModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model import _2034
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6149
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3790
from mastapy._internal.python_net import python_net_import

_DATUM_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'DatumModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumModalAnalysesAtStiffnesses',)


class DatumModalAnalysesAtStiffnesses(_3790.ComponentModalAnalysesAtStiffnesses):
    '''DatumModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _DATUM_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2034.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2034.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6149.DatumLoadCase':
        '''DatumLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6149.DatumLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
