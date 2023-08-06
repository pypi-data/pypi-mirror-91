'''_1714.py

LoadedNonBarrelRollerBearingRow
'''


from mastapy.bearings.bearing_results.rolling import (
    _1713, _1683, _1686, _1698,
    _1710, _1738, _1719
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_LOADED_NON_BARREL_ROLLER_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedNonBarrelRollerBearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedNonBarrelRollerBearingRow',)


class LoadedNonBarrelRollerBearingRow(_1719.LoadedRollerBearingRow):
    '''LoadedNonBarrelRollerBearingRow

    This is a mastapy class.
    '''

    TYPE = _LOADED_NON_BARREL_ROLLER_BEARING_ROW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedNonBarrelRollerBearingRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def loaded_bearing(self) -> '_1713.LoadedNonBarrelRollerBearingResults':
        '''LoadedNonBarrelRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1713.LoadedNonBarrelRollerBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedNonBarrelRollerBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None

    @property
    def loaded_bearing_of_type_loaded_axial_thrust_cylindrical_roller_bearing_results(self) -> '_1683.LoadedAxialThrustCylindricalRollerBearingResults':
        '''LoadedAxialThrustCylindricalRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1683.LoadedAxialThrustCylindricalRollerBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedAxialThrustCylindricalRollerBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None

    @property
    def loaded_bearing_of_type_loaded_axial_thrust_needle_roller_bearing_results(self) -> '_1686.LoadedAxialThrustNeedleRollerBearingResults':
        '''LoadedAxialThrustNeedleRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1686.LoadedAxialThrustNeedleRollerBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedAxialThrustNeedleRollerBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None

    @property
    def loaded_bearing_of_type_loaded_cylindrical_roller_bearing_results(self) -> '_1698.LoadedCylindricalRollerBearingResults':
        '''LoadedCylindricalRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1698.LoadedCylindricalRollerBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedCylindricalRollerBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None

    @property
    def loaded_bearing_of_type_loaded_needle_roller_bearing_results(self) -> '_1710.LoadedNeedleRollerBearingResults':
        '''LoadedNeedleRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1710.LoadedNeedleRollerBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedNeedleRollerBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None

    @property
    def loaded_bearing_of_type_loaded_taper_roller_bearing_results(self) -> '_1738.LoadedTaperRollerBearingResults':
        '''LoadedTaperRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1738.LoadedTaperRollerBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedTaperRollerBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None
