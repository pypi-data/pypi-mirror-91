﻿'''_854.py

CylindricalGearSetMicroGeometry
'''


from typing import List

from mastapy.gears.gear_designs.cylindrical import _787, _796
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _849, _847
from mastapy.gears.analysis import _965
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_MICRO_GEOMETRY = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'CylindricalGearSetMicroGeometry')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetMicroGeometry',)


class CylindricalGearSetMicroGeometry(_965.GearSetImplementationDetail):
    '''CylindricalGearSetMicroGeometry

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_MICRO_GEOMETRY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetMicroGeometry.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cylindrical_gear_set_design(self) -> '_787.CylindricalGearSetDesign':
        '''CylindricalGearSetDesign: 'CylindricalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _787.CylindricalGearSetDesign.TYPE not in self.wrapped.CylindricalGearSetDesign.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_gear_set_design to CylindricalGearSetDesign. Expected: {}.'.format(self.wrapped.CylindricalGearSetDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.CylindricalGearSetDesign.__class__)(self.wrapped.CylindricalGearSetDesign) if self.wrapped.CylindricalGearSetDesign else None

    @property
    def cylindrical_gear_micro_geometries(self) -> 'List[_849.CylindricalGearMicroGeometry]':
        '''List[CylindricalGearMicroGeometry]: 'CylindricalGearMicroGeometries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearMicroGeometries, constructor.new(_849.CylindricalGearMicroGeometry))
        return value

    @property
    def cylindrical_mesh_micro_geometries(self) -> 'List[_847.CylindricalGearMeshMicroGeometry]':
        '''List[CylindricalGearMeshMicroGeometry]: 'CylindricalMeshMicroGeometries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshMicroGeometries, constructor.new(_847.CylindricalGearMeshMicroGeometry))
        return value
