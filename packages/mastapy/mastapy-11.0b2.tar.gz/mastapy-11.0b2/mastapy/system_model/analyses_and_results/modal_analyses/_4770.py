﻿'''_4770.py

DatumModalAnalysis
'''


from mastapy.system_model.part_model import _2097
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6467
from mastapy.system_model.analyses_and_results.system_deflections import _2384
from mastapy.system_model.analyses_and_results.modal_analyses import _4743
from mastapy._internal.python_net import python_net_import

_DATUM_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'DatumModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumModalAnalysis',)


class DatumModalAnalysis(_4743.ComponentModalAnalysis):
    '''DatumModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _DATUM_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2097.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2097.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6467.DatumLoadCase':
        '''DatumLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6467.DatumLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2384.DatumSystemDeflection':
        '''DatumSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2384.DatumSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
