﻿'''_6513.py

StraightBevelGearSetCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2130
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _6511, _6512, _6427
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6390
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'StraightBevelGearSetCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetCompoundAdvancedSystemDeflection',)


class StraightBevelGearSetCompoundAdvancedSystemDeflection(_6427.BevelGearSetCompoundAdvancedSystemDeflection):
    '''StraightBevelGearSetCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2130.StraightBevelGearSet':
        '''StraightBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2130.StraightBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2130.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2130.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def straight_bevel_gears_compound_advanced_system_deflection(self) -> 'List[_6511.StraightBevelGearCompoundAdvancedSystemDeflection]':
        '''List[StraightBevelGearCompoundAdvancedSystemDeflection]: 'StraightBevelGearsCompoundAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsCompoundAdvancedSystemDeflection, constructor.new(_6511.StraightBevelGearCompoundAdvancedSystemDeflection))
        return value

    @property
    def straight_bevel_meshes_compound_advanced_system_deflection(self) -> 'List[_6512.StraightBevelGearMeshCompoundAdvancedSystemDeflection]':
        '''List[StraightBevelGearMeshCompoundAdvancedSystemDeflection]: 'StraightBevelMeshesCompoundAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesCompoundAdvancedSystemDeflection, constructor.new(_6512.StraightBevelGearMeshCompoundAdvancedSystemDeflection))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_6390.StraightBevelGearSetAdvancedSystemDeflection]':
        '''List[StraightBevelGearSetAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6390.StraightBevelGearSetAdvancedSystemDeflection))
        return value

    @property
    def assembly_advanced_system_deflection_load_cases(self) -> 'List[_6390.StraightBevelGearSetAdvancedSystemDeflection]':
        '''List[StraightBevelGearSetAdvancedSystemDeflection]: 'AssemblyAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAdvancedSystemDeflectionLoadCases, constructor.new(_6390.StraightBevelGearSetAdvancedSystemDeflection))
        return value
