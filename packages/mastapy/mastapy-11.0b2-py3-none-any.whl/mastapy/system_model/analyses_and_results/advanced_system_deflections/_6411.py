﻿'''_6411.py

ZerolBevelGearMeshAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1934
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6265
from mastapy.gears.rating.zerol_bevel import _169
from mastapy.system_model.analyses_and_results.system_deflections import _2390
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6302
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'ZerolBevelGearMeshAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearMeshAdvancedSystemDeflection',)


class ZerolBevelGearMeshAdvancedSystemDeflection(_6302.BevelGearMeshAdvancedSystemDeflection):
    '''ZerolBevelGearMeshAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearMeshAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1934.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1934.ZerolBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6265.ZerolBevelGearMeshLoadCase':
        '''ZerolBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6265.ZerolBevelGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_169.ZerolBevelGearMeshRating':
        '''ZerolBevelGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_169.ZerolBevelGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2390.ZerolBevelGearMeshSystemDeflection]':
        '''List[ZerolBevelGearMeshSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2390.ZerolBevelGearMeshSystemDeflection))
        return value
