﻿'''_5423.py

StraightBevelDiffGearSetGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2128
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6237
from mastapy.system_model.analyses_and_results.system_deflections import _2363
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5421, _5422, _5315
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'StraightBevelDiffGearSetGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetGearWhineAnalysis',)


class StraightBevelDiffGearSetGearWhineAnalysis(_5315.BevelGearSetGearWhineAnalysis):
    '''StraightBevelDiffGearSetGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2128.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2128.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6237.StraightBevelDiffGearSetLoadCase':
        '''StraightBevelDiffGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6237.StraightBevelDiffGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2363.StraightBevelDiffGearSetSystemDeflection':
        '''StraightBevelDiffGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2363.StraightBevelDiffGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def gears_gear_whine_analysis(self) -> 'List[_5421.StraightBevelDiffGearGearWhineAnalysis]':
        '''List[StraightBevelDiffGearGearWhineAnalysis]: 'GearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsGearWhineAnalysis, constructor.new(_5421.StraightBevelDiffGearGearWhineAnalysis))
        return value

    @property
    def straight_bevel_diff_gears_gear_whine_analysis(self) -> 'List[_5421.StraightBevelDiffGearGearWhineAnalysis]':
        '''List[StraightBevelDiffGearGearWhineAnalysis]: 'StraightBevelDiffGearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsGearWhineAnalysis, constructor.new(_5421.StraightBevelDiffGearGearWhineAnalysis))
        return value

    @property
    def meshes_gear_whine_analysis(self) -> 'List[_5422.StraightBevelDiffGearMeshGearWhineAnalysis]':
        '''List[StraightBevelDiffGearMeshGearWhineAnalysis]: 'MeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesGearWhineAnalysis, constructor.new(_5422.StraightBevelDiffGearMeshGearWhineAnalysis))
        return value

    @property
    def straight_bevel_diff_meshes_gear_whine_analysis(self) -> 'List[_5422.StraightBevelDiffGearMeshGearWhineAnalysis]':
        '''List[StraightBevelDiffGearMeshGearWhineAnalysis]: 'StraightBevelDiffMeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesGearWhineAnalysis, constructor.new(_5422.StraightBevelDiffGearMeshGearWhineAnalysis))
        return value
