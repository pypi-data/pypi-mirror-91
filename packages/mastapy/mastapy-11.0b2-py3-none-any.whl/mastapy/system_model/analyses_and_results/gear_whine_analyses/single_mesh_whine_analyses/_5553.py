﻿'''_5553.py

SpiralBevelGearSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model.gears import _2125
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6228
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5474
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'SpiralBevelGearSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSingleMeshWhineAnalysis',)


class SpiralBevelGearSingleMeshWhineAnalysis(_5474.BevelGearSingleMeshWhineAnalysis):
    '''SpiralBevelGearSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2125.SpiralBevelGear':
        '''SpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2125.SpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6228.SpiralBevelGearLoadCase':
        '''SpiralBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6228.SpiralBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
