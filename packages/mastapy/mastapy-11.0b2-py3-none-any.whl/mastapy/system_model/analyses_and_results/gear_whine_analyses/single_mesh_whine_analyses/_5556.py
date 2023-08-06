﻿'''_5556.py

SpringDamperSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2176
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6233
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5495
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'SpringDamperSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperSingleMeshWhineAnalysis',)


class SpringDamperSingleMeshWhineAnalysis(_5495.CouplingSingleMeshWhineAnalysis):
    '''SpringDamperSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2176.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2176.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6233.SpringDamperLoadCase':
        '''SpringDamperLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6233.SpringDamperLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
