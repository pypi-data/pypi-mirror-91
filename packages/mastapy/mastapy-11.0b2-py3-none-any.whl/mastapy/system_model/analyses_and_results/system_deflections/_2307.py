﻿'''_2307.py

FaceGearMeshSystemDeflection
'''


from mastapy._internal import constructor
from mastapy.gears.gear_designs.conical import _897
from mastapy.system_model.connections_and_sockets.gears import _1912
from mastapy.system_model.analyses_and_results.static_loads import _6164
from mastapy.system_model.analyses_and_results.power_flows import _3310
from mastapy.gears.rating.face import _247
from mastapy.system_model.analyses_and_results.system_deflections import _2311
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MESH_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'FaceGearMeshSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMeshSystemDeflection',)


class FaceGearMeshSystemDeflection(_2311.GearMeshSystemDeflection):
    '''FaceGearMeshSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MESH_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearMeshSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def linear_misalignment_in_surface_of_action(self) -> 'float':
        '''float: 'LinearMisalignmentInSurfaceOfAction' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LinearMisalignmentInSurfaceOfAction

    @property
    def angular_misalignment_in_surface_of_action(self) -> 'float':
        '''float: 'AngularMisalignmentInSurfaceOfAction' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AngularMisalignmentInSurfaceOfAction

    @property
    def pinion_angular_misalignment_in_surface_of_action(self) -> 'float':
        '''float: 'PinionAngularMisalignmentInSurfaceOfAction' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PinionAngularMisalignmentInSurfaceOfAction

    @property
    def wheel_angular_misalignment_in_surface_of_action(self) -> 'float':
        '''float: 'WheelAngularMisalignmentInSurfaceOfAction' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WheelAngularMisalignmentInSurfaceOfAction

    @property
    def misalignments_pinion(self) -> '_897.ConicalMeshMisalignments':
        '''ConicalMeshMisalignments: 'MisalignmentsPinion' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_897.ConicalMeshMisalignments)(self.wrapped.MisalignmentsPinion) if self.wrapped.MisalignmentsPinion else None

    @property
    def misalignments_wheel(self) -> '_897.ConicalMeshMisalignments':
        '''ConicalMeshMisalignments: 'MisalignmentsWheel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_897.ConicalMeshMisalignments)(self.wrapped.MisalignmentsWheel) if self.wrapped.MisalignmentsWheel else None

    @property
    def misalignments_total(self) -> '_897.ConicalMeshMisalignments':
        '''ConicalMeshMisalignments: 'MisalignmentsTotal' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_897.ConicalMeshMisalignments)(self.wrapped.MisalignmentsTotal) if self.wrapped.MisalignmentsTotal else None

    @property
    def connection_design(self) -> '_1912.FaceGearMesh':
        '''FaceGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1912.FaceGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6164.FaceGearMeshLoadCase':
        '''FaceGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6164.FaceGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def power_flow_results(self) -> '_3310.FaceGearMeshPowerFlow':
        '''FaceGearMeshPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3310.FaceGearMeshPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def rating(self) -> '_247.FaceGearMeshRating':
        '''FaceGearMeshRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_247.FaceGearMeshRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_247.FaceGearMeshRating':
        '''FaceGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_247.FaceGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None
