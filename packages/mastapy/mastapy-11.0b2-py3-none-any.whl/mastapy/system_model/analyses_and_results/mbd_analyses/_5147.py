﻿'''_5147.py

WormGearSetMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2134
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6261
from mastapy.system_model.analyses_and_results.mbd_analyses import _5146, _5145, _5069
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'WormGearSetMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetMultiBodyDynamicsAnalysis',)


class WormGearSetMultiBodyDynamicsAnalysis(_5069.GearSetMultiBodyDynamicsAnalysis):
    '''WormGearSetMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2134.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2134.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6261.WormGearSetLoadCase':
        '''WormGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6261.WormGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_5146.WormGearMultiBodyDynamicsAnalysis]':
        '''List[WormGearMultiBodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5146.WormGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def worm_gears_multi_body_dynamics_analysis(self) -> 'List[_5146.WormGearMultiBodyDynamicsAnalysis]':
        '''List[WormGearMultiBodyDynamicsAnalysis]: 'WormGearsMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsMultiBodyDynamicsAnalysis, constructor.new(_5146.WormGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def worm_meshes_multi_body_dynamics_analysis(self) -> 'List[_5145.WormGearMeshMultiBodyDynamicsAnalysis]':
        '''List[WormGearMeshMultiBodyDynamicsAnalysis]: 'WormMeshesMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesMultiBodyDynamicsAnalysis, constructor.new(_5145.WormGearMeshMultiBodyDynamicsAnalysis))
        return value
