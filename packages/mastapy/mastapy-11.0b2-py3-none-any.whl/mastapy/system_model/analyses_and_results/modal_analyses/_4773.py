﻿'''_4773.py

FaceGearModalAnalysis
'''


from mastapy.system_model.part_model.gears import _2174
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6481
from mastapy.system_model.analyses_and_results.system_deflections import _2389
from mastapy.system_model.analyses_and_results.modal_analyses import _4779
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'FaceGearModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearModalAnalysis',)


class FaceGearModalAnalysis(_4779.GearModalAnalysis):
    '''FaceGearModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2174.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2174.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6481.FaceGearLoadCase':
        '''FaceGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6481.FaceGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2389.FaceGearSystemDeflection':
        '''FaceGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2389.FaceGearSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
