'''_1719.py

LoadedRollerBearingRow
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.scripting import _7157
from mastapy.bearings.bearing_results.rolling import (
    _1718, _1678, _1683, _1686,
    _1694, _1698, _1710, _1713,
    _1729, _1732, _1738, _1747,
    _1664, _1723
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_LOADED_ROLLER_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedRollerBearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedRollerBearingRow',)


class LoadedRollerBearingRow(_1723.LoadedRollingBearingRow):
    '''LoadedRollerBearingRow

    This is a mastapy class.
    '''

    TYPE = _LOADED_ROLLER_BEARING_ROW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedRollerBearingRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def roller_profile_warning(self) -> 'str':
        '''str: 'RollerProfileWarning' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RollerProfileWarning

    @property
    def inner_race_profile_warning(self) -> 'str':
        '''str: 'InnerRaceProfileWarning' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InnerRaceProfileWarning

    @property
    def outer_race_profile_warning(self) -> 'str':
        '''str: 'OuterRaceProfileWarning' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OuterRaceProfileWarning

    @property
    def hertzian_contact_width_inner(self) -> 'float':
        '''float: 'HertzianContactWidthInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HertzianContactWidthInner

    @property
    def hertzian_contact_width_outer(self) -> 'float':
        '''float: 'HertzianContactWidthOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HertzianContactWidthOuter

    @property
    def maximum_shear_stress_outer(self) -> 'float':
        '''float: 'MaximumShearStressOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumShearStressOuter

    @property
    def maximum_shear_stress_inner(self) -> 'float':
        '''float: 'MaximumShearStressInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumShearStressInner

    @property
    def maximum_normal_edge_stress_inner(self) -> 'float':
        '''float: 'MaximumNormalEdgeStressInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumNormalEdgeStressInner

    @property
    def maximum_normal_edge_stress_outer(self) -> 'float':
        '''float: 'MaximumNormalEdgeStressOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumNormalEdgeStressOuter

    @property
    def shear_stress_chart_inner(self) -> '_7157.SMTBitmap':
        '''SMTBitmap: 'ShearStressChartInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_7157.SMTBitmap)(self.wrapped.ShearStressChartInner) if self.wrapped.ShearStressChartInner else None

    @property
    def shear_stress_chart_outer(self) -> '_7157.SMTBitmap':
        '''SMTBitmap: 'ShearStressChartOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_7157.SMTBitmap)(self.wrapped.ShearStressChartOuter) if self.wrapped.ShearStressChartOuter else None

    @property
    def depth_of_maximum_shear_stress_chart_inner(self) -> '_7157.SMTBitmap':
        '''SMTBitmap: 'DepthOfMaximumShearStressChartInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_7157.SMTBitmap)(self.wrapped.DepthOfMaximumShearStressChartInner) if self.wrapped.DepthOfMaximumShearStressChartInner else None

    @property
    def depth_of_maximum_shear_stress_chart_outer(self) -> '_7157.SMTBitmap':
        '''SMTBitmap: 'DepthOfMaximumShearStressChartOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_7157.SMTBitmap)(self.wrapped.DepthOfMaximumShearStressChartOuter) if self.wrapped.DepthOfMaximumShearStressChartOuter else None

    @property
    def loaded_bearing(self) -> '_1718.LoadedRollerBearingResults':
        '''LoadedRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1718.LoadedRollerBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedRollerBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None

    @property
    def loaded_bearing_of_type_loaded_asymmetric_spherical_roller_bearing_results(self) -> '_1678.LoadedAsymmetricSphericalRollerBearingResults':
        '''LoadedAsymmetricSphericalRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1678.LoadedAsymmetricSphericalRollerBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedAsymmetricSphericalRollerBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

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
    def loaded_bearing_of_type_loaded_crossed_roller_bearing_results(self) -> '_1694.LoadedCrossedRollerBearingResults':
        '''LoadedCrossedRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1694.LoadedCrossedRollerBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedCrossedRollerBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

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
    def loaded_bearing_of_type_loaded_non_barrel_roller_bearing_results(self) -> '_1713.LoadedNonBarrelRollerBearingResults':
        '''LoadedNonBarrelRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1713.LoadedNonBarrelRollerBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedNonBarrelRollerBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None

    @property
    def loaded_bearing_of_type_loaded_spherical_roller_radial_bearing_results(self) -> '_1729.LoadedSphericalRollerRadialBearingResults':
        '''LoadedSphericalRollerRadialBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1729.LoadedSphericalRollerRadialBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedSphericalRollerRadialBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None

    @property
    def loaded_bearing_of_type_loaded_spherical_roller_thrust_bearing_results(self) -> '_1732.LoadedSphericalRollerThrustBearingResults':
        '''LoadedSphericalRollerThrustBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1732.LoadedSphericalRollerThrustBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedSphericalRollerThrustBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

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

    @property
    def loaded_bearing_of_type_loaded_toroidal_roller_bearing_results(self) -> '_1747.LoadedToroidalRollerBearingResults':
        '''LoadedToroidalRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1747.LoadedToroidalRollerBearingResults.TYPE not in self.wrapped.LoadedBearing.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedToroidalRollerBearingResults. Expected: {}.'.format(self.wrapped.LoadedBearing.__class__.__qualname__))

        return constructor.new_override(self.wrapped.LoadedBearing.__class__)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None

    @property
    def lamina_dynamic_equivalent_loads(self) -> 'List[_1664.ForceAtLaminaGroupReportable]':
        '''List[ForceAtLaminaGroupReportable]: 'LaminaDynamicEquivalentLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LaminaDynamicEquivalentLoads, constructor.new(_1664.ForceAtLaminaGroupReportable))
        return value
