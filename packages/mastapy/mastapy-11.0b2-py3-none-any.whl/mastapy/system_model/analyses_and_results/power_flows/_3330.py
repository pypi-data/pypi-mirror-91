﻿'''_3330.py

KlingelnbergCycloPalloidSpiralBevelGearPowerFlow
'''


from mastapy.system_model.part_model.gears import _2122
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6195
from mastapy.gears.rating.klingelnberg_spiral_bevel import _206
from mastapy.system_model.analyses_and_results.power_flows import _3324
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'KlingelnbergCycloPalloidSpiralBevelGearPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearPowerFlow',)


class KlingelnbergCycloPalloidSpiralBevelGearPowerFlow(_3324.KlingelnbergCycloPalloidConicalGearPowerFlow):
    '''KlingelnbergCycloPalloidSpiralBevelGearPowerFlow

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2122.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2122.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6195.KlingelnbergCycloPalloidSpiralBevelGearLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6195.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_206.KlingelnbergCycloPalloidSpiralBevelGearRating':
        '''KlingelnbergCycloPalloidSpiralBevelGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_206.KlingelnbergCycloPalloidSpiralBevelGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
