﻿'''_5401.py

PlanetCarrierGearWhineAnalysis
'''


from mastapy.system_model.part_model import _2053
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6212
from mastapy.system_model.analyses_and_results.system_deflections import _2342
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5392
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'PlanetCarrierGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierGearWhineAnalysis',)


class PlanetCarrierGearWhineAnalysis(_5392.MountableComponentGearWhineAnalysis):
    '''PlanetCarrierGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2053.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2053.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6212.PlanetCarrierLoadCase':
        '''PlanetCarrierLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6212.PlanetCarrierLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2342.PlanetCarrierSystemDeflection':
        '''PlanetCarrierSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2342.PlanetCarrierSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
