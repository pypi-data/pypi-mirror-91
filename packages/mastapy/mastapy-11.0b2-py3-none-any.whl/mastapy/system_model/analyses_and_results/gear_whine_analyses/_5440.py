﻿'''_5440.py

WormGearGearWhineAnalysis
'''


from mastapy.system_model.part_model.gears import _2133
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6259
from mastapy.system_model.analyses_and_results.system_deflections import _2387
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5364
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'WormGearGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearGearWhineAnalysis',)


class WormGearGearWhineAnalysis(_5364.GearGearWhineAnalysis):
    '''WormGearGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2133.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2133.WormGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6259.WormGearLoadCase':
        '''WormGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6259.WormGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2387.WormGearSystemDeflection':
        '''WormGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2387.WormGearSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
