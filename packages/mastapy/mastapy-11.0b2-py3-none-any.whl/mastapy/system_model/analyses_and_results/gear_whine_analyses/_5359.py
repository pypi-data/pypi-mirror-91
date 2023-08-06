﻿'''_5359.py

FaceGearGearWhineAnalysis
'''


from mastapy.system_model.part_model.gears import _2110
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6163
from mastapy.system_model.analyses_and_results.system_deflections import _2309
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5364
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'FaceGearGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearGearWhineAnalysis',)


class FaceGearGearWhineAnalysis(_5364.GearGearWhineAnalysis):
    '''FaceGearGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2110.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2110.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6163.FaceGearLoadCase':
        '''FaceGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6163.FaceGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2309.FaceGearSystemDeflection':
        '''FaceGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2309.FaceGearSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
