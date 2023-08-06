﻿'''_5082.py

KlingelnbergCycloPalloidSpiralBevelGearSetMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2187
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6516
from mastapy.system_model.analyses_and_results.mbd_analyses import _5081, _5080, _5076
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'KlingelnbergCycloPalloidSpiralBevelGearSetMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetMultibodyDynamicsAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearSetMultibodyDynamicsAnalysis(_5076.KlingelnbergCycloPalloidConicalGearSetMultibodyDynamicsAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2187.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2187.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6516.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6516.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_5081.KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5081.KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_multibody_dynamics_analysis(self) -> 'List[_5081.KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearsMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsMultibodyDynamicsAnalysis, constructor.new(_5081.KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_multibody_dynamics_analysis(self) -> 'List[_5080.KlingelnbergCycloPalloidSpiralBevelGearMeshMultibodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshMultibodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelMeshesMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesMultibodyDynamicsAnalysis, constructor.new(_5080.KlingelnbergCycloPalloidSpiralBevelGearMeshMultibodyDynamicsAnalysis))
        return value
