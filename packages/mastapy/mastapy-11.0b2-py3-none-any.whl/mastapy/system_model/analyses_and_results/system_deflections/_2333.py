﻿'''_2333.py

BearingSystemDeflection
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2089, _2090
from mastapy.system_model.analyses_and_results.static_loads import _6418
from mastapy.system_model.analyses_and_results.power_flows import _3671
from mastapy.bearings.bearing_results import (
    _1638, _1644, _1646, _1647,
    _1648, _1649, _1650, _1652
)
from mastapy._internal.cast_exception import CastException
from mastapy.bearings.bearing_results.rolling import (
    _1672, _1675, _1678, _1683,
    _1686, _1691, _1694, _1698,
    _1701, _1706, _1710, _1713,
    _1718, _1722, _1725, _1729,
    _1732, _1738, _1741, _1744,
    _1747
)
from mastapy.bearings.bearing_results.fluid_film import (
    _1804, _1805, _1806, _1807,
    _1809, _1812, _1813
)
from mastapy.math_utility.measured_vectors import _1560
from mastapy.system_model.analyses_and_results.system_deflections import _2363
from mastapy._internal.python_net import python_net_import

_BEARING_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'BearingSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingSystemDeflection',)


class BearingSystemDeflection(_2363.ConnectorSystemDeflection):
    '''BearingSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BEARING_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def element_radial_displacements(self) -> 'List[float]':
        '''List[float]: 'ElementRadialDisplacements' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.ElementRadialDisplacements)
        return value

    @property
    def element_axial_displacements(self) -> 'List[float]':
        '''List[float]: 'ElementAxialDisplacements' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.ElementAxialDisplacements)
        return value

    @property
    def element_tilts(self) -> 'List[float]':
        '''List[float]: 'ElementTilts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.ElementTilts)
        return value

    @property
    def maximum_radial_stiffness(self) -> 'float':
        '''float: 'MaximumRadialStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumRadialStiffness

    @property
    def maximum_tilt_stiffness(self) -> 'float':
        '''float: 'MaximumTiltStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumTiltStiffness

    @property
    def axial_stiffness(self) -> 'float':
        '''float: 'AxialStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AxialStiffness

    @property
    def inner_left_mounting_axial_stiffness(self) -> 'float':
        '''float: 'InnerLeftMountingAxialStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InnerLeftMountingAxialStiffness

    @property
    def inner_right_mounting_axial_stiffness(self) -> 'float':
        '''float: 'InnerRightMountingAxialStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InnerRightMountingAxialStiffness

    @property
    def outer_left_mounting_axial_stiffness(self) -> 'float':
        '''float: 'OuterLeftMountingAxialStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OuterLeftMountingAxialStiffness

    @property
    def outer_right_mounting_axial_stiffness(self) -> 'float':
        '''float: 'OuterRightMountingAxialStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OuterRightMountingAxialStiffness

    @property
    def inner_left_mounting_maximum_tilt_stiffness(self) -> 'float':
        '''float: 'InnerLeftMountingMaximumTiltStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InnerLeftMountingMaximumTiltStiffness

    @property
    def inner_right_mounting_maximum_tilt_stiffness(self) -> 'float':
        '''float: 'InnerRightMountingMaximumTiltStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InnerRightMountingMaximumTiltStiffness

    @property
    def outer_left_mounting_maximum_tilt_stiffness(self) -> 'float':
        '''float: 'OuterLeftMountingMaximumTiltStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OuterLeftMountingMaximumTiltStiffness

    @property
    def outer_right_mounting_maximum_tilt_stiffness(self) -> 'float':
        '''float: 'OuterRightMountingMaximumTiltStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OuterRightMountingMaximumTiltStiffness

    @property
    def outer_radial_mounting_maximum_tilt_stiffness(self) -> 'float':
        '''float: 'OuterRadialMountingMaximumTiltStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OuterRadialMountingMaximumTiltStiffness

    @property
    def inner_radial_mounting_maximum_tilt_stiffness(self) -> 'float':
        '''float: 'InnerRadialMountingMaximumTiltStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InnerRadialMountingMaximumTiltStiffness

    @property
    def elements_in_contact(self) -> 'int':
        '''int: 'ElementsInContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ElementsInContact

    @property
    def is_loaded(self) -> 'bool':
        '''bool: 'IsLoaded' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsLoaded

    @property
    def component_axial_displacements(self) -> 'List[float]':
        '''List[float]: 'ComponentAxialDisplacements' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.wrapped.ComponentAxialDisplacements)
        return value

    @property
    def percentage_preload_spring_compression(self) -> 'float':
        '''float: 'PercentagePreloadSpringCompression' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PercentagePreloadSpringCompression

    @property
    def preload_spring_compression(self) -> 'float':
        '''float: 'PreloadSpringCompression' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PreloadSpringCompression

    @property
    def component_design(self) -> '_2089.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2089.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6418.BearingLoadCase':
        '''BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6418.BearingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3671.BearingPowerFlow':
        '''BearingPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3671.BearingPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def stiffness_between_rings(self) -> '_1638.BearingStiffnessMatrixReporter':
        '''BearingStiffnessMatrixReporter: 'StiffnessBetweenRings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1638.BearingStiffnessMatrixReporter)(self.wrapped.StiffnessBetweenRings) if self.wrapped.StiffnessBetweenRings else None

    @property
    def stiffness_matrix(self) -> '_1638.BearingStiffnessMatrixReporter':
        '''BearingStiffnessMatrixReporter: 'StiffnessMatrix' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1638.BearingStiffnessMatrixReporter)(self.wrapped.StiffnessMatrix) if self.wrapped.StiffnessMatrix else None

    @property
    def outer_left_mounting_stiffness(self) -> '_1638.BearingStiffnessMatrixReporter':
        '''BearingStiffnessMatrixReporter: 'OuterLeftMountingStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1638.BearingStiffnessMatrixReporter)(self.wrapped.OuterLeftMountingStiffness) if self.wrapped.OuterLeftMountingStiffness else None

    @property
    def outer_right_mounting_stiffness(self) -> '_1638.BearingStiffnessMatrixReporter':
        '''BearingStiffnessMatrixReporter: 'OuterRightMountingStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1638.BearingStiffnessMatrixReporter)(self.wrapped.OuterRightMountingStiffness) if self.wrapped.OuterRightMountingStiffness else None

    @property
    def inner_left_mounting_stiffness(self) -> '_1638.BearingStiffnessMatrixReporter':
        '''BearingStiffnessMatrixReporter: 'InnerLeftMountingStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1638.BearingStiffnessMatrixReporter)(self.wrapped.InnerLeftMountingStiffness) if self.wrapped.InnerLeftMountingStiffness else None

    @property
    def inner_right_mounting_stiffness(self) -> '_1638.BearingStiffnessMatrixReporter':
        '''BearingStiffnessMatrixReporter: 'InnerRightMountingStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1638.BearingStiffnessMatrixReporter)(self.wrapped.InnerRightMountingStiffness) if self.wrapped.InnerRightMountingStiffness else None

    @property
    def inner_radial_mounting_stiffness(self) -> '_1638.BearingStiffnessMatrixReporter':
        '''BearingStiffnessMatrixReporter: 'InnerRadialMountingStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1638.BearingStiffnessMatrixReporter)(self.wrapped.InnerRadialMountingStiffness) if self.wrapped.InnerRadialMountingStiffness else None

    @property
    def outer_radial_mounting_stiffness(self) -> '_1638.BearingStiffnessMatrixReporter':
        '''BearingStiffnessMatrixReporter: 'OuterRadialMountingStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1638.BearingStiffnessMatrixReporter)(self.wrapped.OuterRadialMountingStiffness) if self.wrapped.OuterRadialMountingStiffness else None

    @property
    def preload_spring_stiffness(self) -> '_1638.BearingStiffnessMatrixReporter':
        '''BearingStiffnessMatrixReporter: 'PreloadSpringStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1638.BearingStiffnessMatrixReporter)(self.wrapped.PreloadSpringStiffness) if self.wrapped.PreloadSpringStiffness else None

    @property
    def component_detailed_analysis(self) -> '_1644.LoadedBearingResults':
        '''LoadedBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1644.LoadedBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_concept_axial_clearance_bearing_results(self) -> '_1646.LoadedConceptAxialClearanceBearingResults':
        '''LoadedConceptAxialClearanceBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1646.LoadedConceptAxialClearanceBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedConceptAxialClearanceBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_concept_clearance_bearing_results(self) -> '_1647.LoadedConceptClearanceBearingResults':
        '''LoadedConceptClearanceBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1647.LoadedConceptClearanceBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedConceptClearanceBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_concept_radial_clearance_bearing_results(self) -> '_1648.LoadedConceptRadialClearanceBearingResults':
        '''LoadedConceptRadialClearanceBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1648.LoadedConceptRadialClearanceBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedConceptRadialClearanceBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_detailed_bearing_results(self) -> '_1649.LoadedDetailedBearingResults':
        '''LoadedDetailedBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1649.LoadedDetailedBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedDetailedBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_linear_bearing_results(self) -> '_1650.LoadedLinearBearingResults':
        '''LoadedLinearBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1650.LoadedLinearBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedLinearBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_non_linear_bearing_results(self) -> '_1652.LoadedNonLinearBearingResults':
        '''LoadedNonLinearBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1652.LoadedNonLinearBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedNonLinearBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_angular_contact_ball_bearing_results(self) -> '_1672.LoadedAngularContactBallBearingResults':
        '''LoadedAngularContactBallBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1672.LoadedAngularContactBallBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedAngularContactBallBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_angular_contact_thrust_ball_bearing_results(self) -> '_1675.LoadedAngularContactThrustBallBearingResults':
        '''LoadedAngularContactThrustBallBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1675.LoadedAngularContactThrustBallBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedAngularContactThrustBallBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_asymmetric_spherical_roller_bearing_results(self) -> '_1678.LoadedAsymmetricSphericalRollerBearingResults':
        '''LoadedAsymmetricSphericalRollerBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1678.LoadedAsymmetricSphericalRollerBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedAsymmetricSphericalRollerBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_axial_thrust_cylindrical_roller_bearing_results(self) -> '_1683.LoadedAxialThrustCylindricalRollerBearingResults':
        '''LoadedAxialThrustCylindricalRollerBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1683.LoadedAxialThrustCylindricalRollerBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedAxialThrustCylindricalRollerBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_axial_thrust_needle_roller_bearing_results(self) -> '_1686.LoadedAxialThrustNeedleRollerBearingResults':
        '''LoadedAxialThrustNeedleRollerBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1686.LoadedAxialThrustNeedleRollerBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedAxialThrustNeedleRollerBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_ball_bearing_results(self) -> '_1691.LoadedBallBearingResults':
        '''LoadedBallBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1691.LoadedBallBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedBallBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_crossed_roller_bearing_results(self) -> '_1694.LoadedCrossedRollerBearingResults':
        '''LoadedCrossedRollerBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1694.LoadedCrossedRollerBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedCrossedRollerBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_cylindrical_roller_bearing_results(self) -> '_1698.LoadedCylindricalRollerBearingResults':
        '''LoadedCylindricalRollerBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1698.LoadedCylindricalRollerBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedCylindricalRollerBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_deep_groove_ball_bearing_results(self) -> '_1701.LoadedDeepGrooveBallBearingResults':
        '''LoadedDeepGrooveBallBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1701.LoadedDeepGrooveBallBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedDeepGrooveBallBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_four_point_contact_ball_bearing_results(self) -> '_1706.LoadedFourPointContactBallBearingResults':
        '''LoadedFourPointContactBallBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1706.LoadedFourPointContactBallBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedFourPointContactBallBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_needle_roller_bearing_results(self) -> '_1710.LoadedNeedleRollerBearingResults':
        '''LoadedNeedleRollerBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1710.LoadedNeedleRollerBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedNeedleRollerBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_non_barrel_roller_bearing_results(self) -> '_1713.LoadedNonBarrelRollerBearingResults':
        '''LoadedNonBarrelRollerBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1713.LoadedNonBarrelRollerBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedNonBarrelRollerBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_roller_bearing_results(self) -> '_1718.LoadedRollerBearingResults':
        '''LoadedRollerBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1718.LoadedRollerBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedRollerBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_rolling_bearing_results(self) -> '_1722.LoadedRollingBearingResults':
        '''LoadedRollingBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1722.LoadedRollingBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedRollingBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_self_aligning_ball_bearing_results(self) -> '_1725.LoadedSelfAligningBallBearingResults':
        '''LoadedSelfAligningBallBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1725.LoadedSelfAligningBallBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedSelfAligningBallBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_spherical_roller_radial_bearing_results(self) -> '_1729.LoadedSphericalRollerRadialBearingResults':
        '''LoadedSphericalRollerRadialBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1729.LoadedSphericalRollerRadialBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedSphericalRollerRadialBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_spherical_roller_thrust_bearing_results(self) -> '_1732.LoadedSphericalRollerThrustBearingResults':
        '''LoadedSphericalRollerThrustBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1732.LoadedSphericalRollerThrustBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedSphericalRollerThrustBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_taper_roller_bearing_results(self) -> '_1738.LoadedTaperRollerBearingResults':
        '''LoadedTaperRollerBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1738.LoadedTaperRollerBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedTaperRollerBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_three_point_contact_ball_bearing_results(self) -> '_1741.LoadedThreePointContactBallBearingResults':
        '''LoadedThreePointContactBallBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1741.LoadedThreePointContactBallBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedThreePointContactBallBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_thrust_ball_bearing_results(self) -> '_1744.LoadedThrustBallBearingResults':
        '''LoadedThrustBallBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1744.LoadedThrustBallBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedThrustBallBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_toroidal_roller_bearing_results(self) -> '_1747.LoadedToroidalRollerBearingResults':
        '''LoadedToroidalRollerBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1747.LoadedToroidalRollerBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedToroidalRollerBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_fluid_film_bearing_results(self) -> '_1804.LoadedFluidFilmBearingResults':
        '''LoadedFluidFilmBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1804.LoadedFluidFilmBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedFluidFilmBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_grease_filled_journal_bearing_results(self) -> '_1805.LoadedGreaseFilledJournalBearingResults':
        '''LoadedGreaseFilledJournalBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1805.LoadedGreaseFilledJournalBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedGreaseFilledJournalBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_pad_fluid_film_bearing_results(self) -> '_1806.LoadedPadFluidFilmBearingResults':
        '''LoadedPadFluidFilmBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1806.LoadedPadFluidFilmBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedPadFluidFilmBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_plain_journal_bearing_results(self) -> '_1807.LoadedPlainJournalBearingResults':
        '''LoadedPlainJournalBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1807.LoadedPlainJournalBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedPlainJournalBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_plain_oil_fed_journal_bearing(self) -> '_1809.LoadedPlainOilFedJournalBearing':
        '''LoadedPlainOilFedJournalBearing: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1809.LoadedPlainOilFedJournalBearing.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedPlainOilFedJournalBearing. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_tilting_pad_journal_bearing_results(self) -> '_1812.LoadedTiltingPadJournalBearingResults':
        '''LoadedTiltingPadJournalBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1812.LoadedTiltingPadJournalBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedTiltingPadJournalBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_detailed_analysis_of_type_loaded_tilting_pad_thrust_bearing_results(self) -> '_1813.LoadedTiltingPadThrustBearingResults':
        '''LoadedTiltingPadThrustBearingResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1813.LoadedTiltingPadThrustBearingResults.TYPE not in self.wrapped.ComponentDetailedAnalysis.__class__.__mro__:
            raise CastException('Failed to cast component_detailed_analysis to LoadedTiltingPadThrustBearingResults. Expected: {}.'.format(self.wrapped.ComponentDetailedAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDetailedAnalysis.__class__)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def planetaries(self) -> 'List[BearingSystemDeflection]':
        '''List[BearingSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingSystemDeflection))
        return value

    @property
    def stiffness_between_each_ring(self) -> 'List[_1638.BearingStiffnessMatrixReporter]':
        '''List[BearingStiffnessMatrixReporter]: 'StiffnessBetweenEachRing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StiffnessBetweenEachRing, constructor.new(_1638.BearingStiffnessMatrixReporter))
        return value

    @property
    def forces_at_zero_displacement_for_inner_and_outer_nodes(self) -> 'List[_1560.ForceResults]':
        '''List[ForceResults]: 'ForcesAtZeroDisplacementForInnerAndOuterNodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ForcesAtZeroDisplacementForInnerAndOuterNodes, constructor.new(_1560.ForceResults))
        return value

    @property
    def race_mounting_options_for_analysis(self) -> 'List[_2090.BearingRaceMountingOptions]':
        '''List[BearingRaceMountingOptions]: 'RaceMountingOptionsForAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RaceMountingOptionsForAnalysis, constructor.new(_2090.BearingRaceMountingOptions))
        return value
