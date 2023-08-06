﻿'''_847.py

CylindricalGearMeshMicroGeometry
'''


from typing import List

from mastapy.gears.gear_designs.cylindrical import _785, _782
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _854, _849
from mastapy.gears.analysis import _959
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_MICRO_GEOMETRY = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'CylindricalGearMeshMicroGeometry')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshMicroGeometry',)


class CylindricalGearMeshMicroGeometry(_959.GearMeshImplementationDetail):
    '''CylindricalGearMeshMicroGeometry

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_MICRO_GEOMETRY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshMicroGeometry.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def profile_measured_as(self) -> '_785.CylindricalGearProfileMeasurementType':
        '''CylindricalGearProfileMeasurementType: 'ProfileMeasuredAs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.ProfileMeasuredAs)
        return constructor.new(_785.CylindricalGearProfileMeasurementType)(value) if value else None

    @property
    def cylindrical_mesh(self) -> '_782.CylindricalGearMeshDesign':
        '''CylindricalGearMeshDesign: 'CylindricalMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_782.CylindricalGearMeshDesign)(self.wrapped.CylindricalMesh) if self.wrapped.CylindricalMesh else None

    @property
    def cylindrical_gear_set_micro_geometry(self) -> '_854.CylindricalGearSetMicroGeometry':
        '''CylindricalGearSetMicroGeometry: 'CylindricalGearSetMicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_854.CylindricalGearSetMicroGeometry)(self.wrapped.CylindricalGearSetMicroGeometry) if self.wrapped.CylindricalGearSetMicroGeometry else None

    @property
    def cylindrical_gear_micro_geometries(self) -> 'List[_849.CylindricalGearMicroGeometry]':
        '''List[CylindricalGearMicroGeometry]: 'CylindricalGearMicroGeometries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearMicroGeometries, constructor.new(_849.CylindricalGearMicroGeometry))
        return value

    @property
    def gear_a(self) -> '_849.CylindricalGearMicroGeometry':
        '''CylindricalGearMicroGeometry: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_849.CylindricalGearMicroGeometry)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_b(self) -> '_849.CylindricalGearMicroGeometry':
        '''CylindricalGearMicroGeometry: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_849.CylindricalGearMicroGeometry)(self.wrapped.GearB) if self.wrapped.GearB else None
