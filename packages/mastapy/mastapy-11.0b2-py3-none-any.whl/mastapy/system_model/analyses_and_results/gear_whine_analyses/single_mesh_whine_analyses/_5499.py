﻿'''_5499.py

CylindricalGearMeshSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1910
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6143
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5509
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'CylindricalGearMeshSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshSingleMeshWhineAnalysis',)


class CylindricalGearMeshSingleMeshWhineAnalysis(_5509.GearMeshSingleMeshWhineAnalysis):
    '''CylindricalGearMeshSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1910.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1910.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6143.CylindricalGearMeshLoadCase':
        '''CylindricalGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6143.CylindricalGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def planetaries(self) -> 'List[CylindricalGearMeshSingleMeshWhineAnalysis]':
        '''List[CylindricalGearMeshSingleMeshWhineAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearMeshSingleMeshWhineAnalysis))
        return value
