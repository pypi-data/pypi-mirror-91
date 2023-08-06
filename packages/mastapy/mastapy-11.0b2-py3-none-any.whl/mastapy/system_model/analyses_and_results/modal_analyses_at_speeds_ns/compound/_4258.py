﻿'''_4258.py

ZerolBevelGearMeshCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1934
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4136
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _4154
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MESH_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'ZerolBevelGearMeshCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearMeshCompoundModalAnalysesAtSpeeds',)


class ZerolBevelGearMeshCompoundModalAnalysesAtSpeeds(_4154.BevelGearMeshCompoundModalAnalysesAtSpeeds):
    '''ZerolBevelGearMeshCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_MESH_COMPOUND_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearMeshCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1934.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1934.ZerolBevelGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1934.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1934.ZerolBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4136.ZerolBevelGearMeshModalAnalysesAtSpeeds]':
        '''List[ZerolBevelGearMeshModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4136.ZerolBevelGearMeshModalAnalysesAtSpeeds))
        return value

    @property
    def connection_modal_analyses_at_speeds_load_cases(self) -> 'List[_4136.ZerolBevelGearMeshModalAnalysesAtSpeeds]':
        '''List[ZerolBevelGearMeshModalAnalysesAtSpeeds]: 'ConnectionModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysesAtSpeedsLoadCases, constructor.new(_4136.ZerolBevelGearMeshModalAnalysesAtSpeeds))
        return value
