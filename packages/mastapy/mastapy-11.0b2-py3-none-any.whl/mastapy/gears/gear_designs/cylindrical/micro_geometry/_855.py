﻿'''_855.py

CylindricalGearSetMicroGeometryDutyCycle
'''


from typing import List

from mastapy.gears.rating.cylindrical import _261
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _848
from mastapy.gears.analysis import _964
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_MICRO_GEOMETRY_DUTY_CYCLE = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'CylindricalGearSetMicroGeometryDutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetMicroGeometryDutyCycle',)


class CylindricalGearSetMicroGeometryDutyCycle(_964.GearSetImplementationAnalysisDutyCycle):
    '''CylindricalGearSetMicroGeometryDutyCycle

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_MICRO_GEOMETRY_DUTY_CYCLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetMicroGeometryDutyCycle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def rating(self) -> '_261.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_261.CylindricalGearSetDutyCycleRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def meshes(self) -> 'List[_848.CylindricalGearMeshMicroGeometryDutyCycle]':
        '''List[CylindricalGearMeshMicroGeometryDutyCycle]: 'Meshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Meshes, constructor.new(_848.CylindricalGearMeshMicroGeometryDutyCycle))
        return value
