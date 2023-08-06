'''enum_with_selected_value.py

Implementations of 'EnumWithSelectedValue' in Python.
As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
'''


from enum import Enum
from typing import List

from mastapy._internal import (
    mixins, enum_with_selected_value_runtime, constructor, conversion
)
from mastapy.shafts import _33, _42
from mastapy._internal.python_net import python_net_import
from mastapy.nodal_analysis import (
    _64, _82, _70, _78,
    _48
)
from mastapy.nodal_analysis.varying_input_components import _89
from mastapy.fe_tools.enums import _1149
from mastapy.materials import _226, _230, _216
from mastapy.gears import _297, _295, _298
from mastapy.math_utility import (
    _1510, _1492, _1491, _1506,
    _1494, _1505, _1503
)
from mastapy.gears.rating.cylindrical import _436, _437
from mastapy.gears.micro_geometry import (
    _522, _521, _520, _519
)
from mastapy.gears.manufacturing.cylindrical import (
    _570, _569, _573, _555
)
from mastapy.gears.manufacturing.cylindrical.plunge_shaving import _592, _591, _589
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import _604
from mastapy.geometry.two_d.curves import _273
from mastapy.gears.gear_designs.cylindrical import _1004, _976, _996
from mastapy.gears.gear_designs.conical import _1068, _1067, _1079
from mastapy.gears.gear_set_pareto_optimiser import _835
from mastapy.utility.model_validation import _1437, _1440
from mastapy.gears.ltca import _771
from mastapy.gears.gear_designs.creation_options import _1056
from mastapy.gears.gear_designs.bevel import _1100, _1089
from mastapy.fe_tools.vfx_tools.vfx_enums import _1147, _1146
from mastapy.bearings.tolerances import (
    _1608, _1620, _1601, _1602,
    _1600
)
from mastapy.detailed_rigid_connectors.splines import (
    _1157, _1180, _1166, _1167,
    _1175, _1181, _1158
)
from mastapy.detailed_rigid_connectors.interference_fits import _1211
from mastapy.utility import _1253
from mastapy.utility.report import _1396
from mastapy.bearings import (
    _1591, _1584, _1592, _1595,
    _1572, _1573, _1597, _1579
)
from mastapy.bearings.bearing_results import (
    _1657, _1656, _1659, _1658
)
from mastapy.system_model.part_model import _2123
from mastapy.system_model.fe import (
    _2018, _2037, _2060, _2047,
    _2015
)
from mastapy.system_model import (
    _1882, _1893, _1889, _1891
)
from mastapy.nodal_analysis.fe_export_utility import _148, _147
from mastapy.utility.enums import _1463
from mastapy.system_model.part_model.couplings import _2241, _2237, _2240
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3978
from mastapy.system_model.analyses_and_results.static_loads import (
    _6416, _6575, _6501, _6494,
    _6534, _6576
)
from mastapy.system_model.analyses_and_results.mbd_analyses import (
    _5010, _5062, _5107, _5132
)
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5641
from mastapy.bearings.bearing_results.rolling.iso_rating_results import _1795
from mastapy.math_utility.hertzian_contact import _1569
from mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition import _6590

_ARRAY = python_net_import('System', 'Array')
_ENUM_WITH_SELECTED_VALUE = python_net_import('SMT.MastaAPI.Utility.Property', 'EnumWithSelectedValue')


__docformat__ = 'restructuredtext en'
__all__ = (
    'EnumWithSelectedValue_ShaftRatingMethod', 'EnumWithSelectedValue_SurfaceFinishes',
    'EnumWithSelectedValue_IntegrationMethod', 'EnumWithSelectedValue_ValueInputOption',
    'EnumWithSelectedValue_SinglePointSelectionMethod', 'EnumWithSelectedValue_ModeInputType',
    'EnumWithSelectedValue_MaterialPropertyClass', 'EnumWithSelectedValue_LubricantDefinition',
    'EnumWithSelectedValue_LubricantViscosityClassISO', 'EnumWithSelectedValue_MicroGeometryModel',
    'EnumWithSelectedValue_ExtrapolationOptions', 'EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod',
    'EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod', 'EnumWithSelectedValue_CylindricalGearRatingMethods',
    'EnumWithSelectedValue_LocationOfTipReliefEvaluation', 'EnumWithSelectedValue_LocationOfRootReliefEvaluation',
    'EnumWithSelectedValue_LocationOfEvaluationUpperLimit', 'EnumWithSelectedValue_LocationOfEvaluationLowerLimit',
    'EnumWithSelectedValue_CylindricalMftRoughingMethods', 'EnumWithSelectedValue_CylindricalMftFinishingMethods',
    'EnumWithSelectedValue_MicroGeometryDefinitionType', 'EnumWithSelectedValue_MicroGeometryDefinitionMethod',
    'EnumWithSelectedValue_ChartType', 'EnumWithSelectedValue_Flank',
    'EnumWithSelectedValue_ActiveProcessMethod', 'EnumWithSelectedValue_CutterFlankSections',
    'EnumWithSelectedValue_BasicCurveTypes', 'EnumWithSelectedValue_ThicknessType',
    'EnumWithSelectedValue_ConicalManufactureMethods', 'EnumWithSelectedValue_ConicalMachineSettingCalculationMethods',
    'EnumWithSelectedValue_CandidateDisplayChoice', 'EnumWithSelectedValue_Severity',
    'EnumWithSelectedValue_GeometrySpecificationType', 'EnumWithSelectedValue_StatusItemSeverity',
    'EnumWithSelectedValue_LubricationMethods', 'EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod',
    'EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods', 'EnumWithSelectedValue_ContactResultType',
    'EnumWithSelectedValue_StressResultsType', 'EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption',
    'EnumWithSelectedValue_ToothThicknessSpecificationMethod', 'EnumWithSelectedValue_LoadDistributionFactorMethods',
    'EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods', 'EnumWithSelectedValue_ProSolveSolverType',
    'EnumWithSelectedValue_ProSolveMpcType', 'EnumWithSelectedValue_ITDesignation',
    'EnumWithSelectedValue_DudleyEffectiveLengthApproximationOption', 'EnumWithSelectedValue_SplineRatingTypes',
    'EnumWithSelectedValue_Modules', 'EnumWithSelectedValue_PressureAngleTypes',
    'EnumWithSelectedValue_SplineFitClassType', 'EnumWithSelectedValue_SplineToleranceClassTypes',
    'EnumWithSelectedValue_Table4JointInterfaceTypes', 'EnumWithSelectedValue_ExecutableDirectoryCopier_Option',
    'EnumWithSelectedValue_CadPageOrientation', 'EnumWithSelectedValue_RollerBearingProfileTypes',
    'EnumWithSelectedValue_FluidFilmTemperatureOptions', 'EnumWithSelectedValue_SupportToleranceLocationDesignation',
    'EnumWithSelectedValue_LoadedBallElementPropertyType', 'EnumWithSelectedValue_RollingBearingArrangement',
    'EnumWithSelectedValue_RollingBearingRaceType', 'EnumWithSelectedValue_BasicDynamicLoadRatingCalculationMethod',
    'EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod', 'EnumWithSelectedValue_RotationalDirections',
    'EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing', 'EnumWithSelectedValue_ComponentOrientationOption',
    'EnumWithSelectedValue_Axis', 'EnumWithSelectedValue_AlignmentAxis',
    'EnumWithSelectedValue_DesignEntityId', 'EnumWithSelectedValue_FESubstructureType',
    'EnumWithSelectedValue_ThermalExpansionOption', 'EnumWithSelectedValue_FEExportFormat',
    'EnumWithSelectedValue_ThreeDViewContourOption', 'EnumWithSelectedValue_BoundaryConditionType',
    'EnumWithSelectedValue_LinkNodeSource', 'EnumWithSelectedValue_BearingNodeOption',
    'EnumWithSelectedValue_BearingToleranceClass', 'EnumWithSelectedValue_BearingModel',
    'EnumWithSelectedValue_PreloadType', 'EnumWithSelectedValue_RaceRadialMountingType',
    'EnumWithSelectedValue_RaceAxialMountingType', 'EnumWithSelectedValue_BearingToleranceDefinitionOptions',
    'EnumWithSelectedValue_InternalClearanceClass', 'EnumWithSelectedValue_PowerLoadType',
    'EnumWithSelectedValue_RigidConnectorTypes', 'EnumWithSelectedValue_RigidConnectorStiffnessType',
    'EnumWithSelectedValue_FitTypes', 'EnumWithSelectedValue_RigidConnectorToothSpacingType',
    'EnumWithSelectedValue_DoeValueSpecificationOption', 'EnumWithSelectedValue_AnalysisType',
    'EnumWithSelectedValue_BarModelExportType', 'EnumWithSelectedValue_DynamicsResponseType',
    'EnumWithSelectedValue_ComplexPartDisplayOption', 'EnumWithSelectedValue_DynamicsResponseScaling',
    'EnumWithSelectedValue_BearingStiffnessModel', 'EnumWithSelectedValue_GearMeshStiffnessModel',
    'EnumWithSelectedValue_ShaftAndHousingFlexibilityOption', 'EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ExportOutputType',
    'EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput', 'EnumWithSelectedValue_StressConcentrationMethod',
    'EnumWithSelectedValue_MeshStiffnessModel', 'EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod',
    'EnumWithSelectedValue_TorqueRippleInputType', 'EnumWithSelectedValue_HarmonicLoadDataType',
    'EnumWithSelectedValue_HarmonicExcitationType', 'EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification',
    'EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod', 'EnumWithSelectedValue_TorqueSpecificationForSystemDeflection',
    'EnumWithSelectedValue_TorqueConverterLockupRule', 'EnumWithSelectedValue_DegreesOfFreedom',
    'EnumWithSelectedValue_DestinationDesignState'
)


class EnumWithSelectedValue_ShaftRatingMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ShaftRatingMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ShaftRatingMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'ShaftRatingMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_33.ShaftRatingMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _33.ShaftRatingMethod

    @classmethod
    def implicit_type(cls) -> '_33.ShaftRatingMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _33.ShaftRatingMethod.type_()

    @property
    def selected_value(self) -> '_33.ShaftRatingMethod':
        '''ShaftRatingMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_33.ShaftRatingMethod]':
        '''List[ShaftRatingMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_SurfaceFinishes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_SurfaceFinishes

    A specific implementation of 'EnumWithSelectedValue' for 'SurfaceFinishes' types.
    '''

    __hash__ = None
    __qualname__ = 'SurfaceFinishes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_42.SurfaceFinishes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _42.SurfaceFinishes

    @classmethod
    def implicit_type(cls) -> '_42.SurfaceFinishes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _42.SurfaceFinishes.type_()

    @property
    def selected_value(self) -> '_42.SurfaceFinishes':
        '''SurfaceFinishes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_42.SurfaceFinishes]':
        '''List[SurfaceFinishes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_IntegrationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_IntegrationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'IntegrationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'IntegrationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_64.IntegrationMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _64.IntegrationMethod

    @classmethod
    def implicit_type(cls) -> '_64.IntegrationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _64.IntegrationMethod.type_()

    @property
    def selected_value(self) -> '_64.IntegrationMethod':
        '''IntegrationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_64.IntegrationMethod]':
        '''List[IntegrationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ValueInputOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ValueInputOption

    A specific implementation of 'EnumWithSelectedValue' for 'ValueInputOption' types.
    '''

    __hash__ = None
    __qualname__ = 'ValueInputOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_82.ValueInputOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _82.ValueInputOption

    @classmethod
    def implicit_type(cls) -> '_82.ValueInputOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _82.ValueInputOption.type_()

    @property
    def selected_value(self) -> '_82.ValueInputOption':
        '''ValueInputOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_82.ValueInputOption]':
        '''List[ValueInputOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_SinglePointSelectionMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_SinglePointSelectionMethod

    A specific implementation of 'EnumWithSelectedValue' for 'SinglePointSelectionMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'SinglePointSelectionMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_89.SinglePointSelectionMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _89.SinglePointSelectionMethod

    @classmethod
    def implicit_type(cls) -> '_89.SinglePointSelectionMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _89.SinglePointSelectionMethod.type_()

    @property
    def selected_value(self) -> '_89.SinglePointSelectionMethod':
        '''SinglePointSelectionMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_89.SinglePointSelectionMethod]':
        '''List[SinglePointSelectionMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ModeInputType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ModeInputType

    A specific implementation of 'EnumWithSelectedValue' for 'ModeInputType' types.
    '''

    __hash__ = None
    __qualname__ = 'ModeInputType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_70.ModeInputType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _70.ModeInputType

    @classmethod
    def implicit_type(cls) -> '_70.ModeInputType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _70.ModeInputType.type_()

    @property
    def selected_value(self) -> '_70.ModeInputType':
        '''ModeInputType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_70.ModeInputType]':
        '''List[ModeInputType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_MaterialPropertyClass(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_MaterialPropertyClass

    A specific implementation of 'EnumWithSelectedValue' for 'MaterialPropertyClass' types.
    '''

    __hash__ = None
    __qualname__ = 'MaterialPropertyClass'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1149.MaterialPropertyClass':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1149.MaterialPropertyClass

    @classmethod
    def implicit_type(cls) -> '_1149.MaterialPropertyClass.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1149.MaterialPropertyClass.type_()

    @property
    def selected_value(self) -> '_1149.MaterialPropertyClass':
        '''MaterialPropertyClass: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1149.MaterialPropertyClass]':
        '''List[MaterialPropertyClass]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LubricantDefinition(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LubricantDefinition

    A specific implementation of 'EnumWithSelectedValue' for 'LubricantDefinition' types.
    '''

    __hash__ = None
    __qualname__ = 'LubricantDefinition'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_226.LubricantDefinition':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _226.LubricantDefinition

    @classmethod
    def implicit_type(cls) -> '_226.LubricantDefinition.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _226.LubricantDefinition.type_()

    @property
    def selected_value(self) -> '_226.LubricantDefinition':
        '''LubricantDefinition: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_226.LubricantDefinition]':
        '''List[LubricantDefinition]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LubricantViscosityClassISO(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LubricantViscosityClassISO

    A specific implementation of 'EnumWithSelectedValue' for 'LubricantViscosityClassISO' types.
    '''

    __hash__ = None
    __qualname__ = 'LubricantViscosityClassISO'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_230.LubricantViscosityClassISO':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _230.LubricantViscosityClassISO

    @classmethod
    def implicit_type(cls) -> '_230.LubricantViscosityClassISO.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _230.LubricantViscosityClassISO.type_()

    @property
    def selected_value(self) -> '_230.LubricantViscosityClassISO':
        '''LubricantViscosityClassISO: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_230.LubricantViscosityClassISO]':
        '''List[LubricantViscosityClassISO]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_MicroGeometryModel(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_MicroGeometryModel

    A specific implementation of 'EnumWithSelectedValue' for 'MicroGeometryModel' types.
    '''

    __hash__ = None
    __qualname__ = 'MicroGeometryModel'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_297.MicroGeometryModel':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _297.MicroGeometryModel

    @classmethod
    def implicit_type(cls) -> '_297.MicroGeometryModel.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _297.MicroGeometryModel.type_()

    @property
    def selected_value(self) -> '_297.MicroGeometryModel':
        '''MicroGeometryModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_297.MicroGeometryModel]':
        '''List[MicroGeometryModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ExtrapolationOptions(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ExtrapolationOptions

    A specific implementation of 'EnumWithSelectedValue' for 'ExtrapolationOptions' types.
    '''

    __hash__ = None
    __qualname__ = 'ExtrapolationOptions'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1510.ExtrapolationOptions':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1510.ExtrapolationOptions

    @classmethod
    def implicit_type(cls) -> '_1510.ExtrapolationOptions.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1510.ExtrapolationOptions.type_()

    @property
    def selected_value(self) -> '_1510.ExtrapolationOptions':
        '''ExtrapolationOptions: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1510.ExtrapolationOptions]':
        '''List[ExtrapolationOptions]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ScuffingFlashTemperatureRatingMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'ScuffingFlashTemperatureRatingMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_436.ScuffingFlashTemperatureRatingMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _436.ScuffingFlashTemperatureRatingMethod

    @classmethod
    def implicit_type(cls) -> '_436.ScuffingFlashTemperatureRatingMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _436.ScuffingFlashTemperatureRatingMethod.type_()

    @property
    def selected_value(self) -> '_436.ScuffingFlashTemperatureRatingMethod':
        '''ScuffingFlashTemperatureRatingMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_436.ScuffingFlashTemperatureRatingMethod]':
        '''List[ScuffingFlashTemperatureRatingMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ScuffingIntegralTemperatureRatingMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ScuffingIntegralTemperatureRatingMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'ScuffingIntegralTemperatureRatingMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_437.ScuffingIntegralTemperatureRatingMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _437.ScuffingIntegralTemperatureRatingMethod

    @classmethod
    def implicit_type(cls) -> '_437.ScuffingIntegralTemperatureRatingMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _437.ScuffingIntegralTemperatureRatingMethod.type_()

    @property
    def selected_value(self) -> '_437.ScuffingIntegralTemperatureRatingMethod':
        '''ScuffingIntegralTemperatureRatingMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_437.ScuffingIntegralTemperatureRatingMethod]':
        '''List[ScuffingIntegralTemperatureRatingMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_CylindricalGearRatingMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_CylindricalGearRatingMethods

    A specific implementation of 'EnumWithSelectedValue' for 'CylindricalGearRatingMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalGearRatingMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_216.CylindricalGearRatingMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _216.CylindricalGearRatingMethods

    @classmethod
    def implicit_type(cls) -> '_216.CylindricalGearRatingMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _216.CylindricalGearRatingMethods.type_()

    @property
    def selected_value(self) -> '_216.CylindricalGearRatingMethods':
        '''CylindricalGearRatingMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_216.CylindricalGearRatingMethods]':
        '''List[CylindricalGearRatingMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LocationOfTipReliefEvaluation(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LocationOfTipReliefEvaluation

    A specific implementation of 'EnumWithSelectedValue' for 'LocationOfTipReliefEvaluation' types.
    '''

    __hash__ = None
    __qualname__ = 'LocationOfTipReliefEvaluation'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_522.LocationOfTipReliefEvaluation':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _522.LocationOfTipReliefEvaluation

    @classmethod
    def implicit_type(cls) -> '_522.LocationOfTipReliefEvaluation.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _522.LocationOfTipReliefEvaluation.type_()

    @property
    def selected_value(self) -> '_522.LocationOfTipReliefEvaluation':
        '''LocationOfTipReliefEvaluation: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_522.LocationOfTipReliefEvaluation]':
        '''List[LocationOfTipReliefEvaluation]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LocationOfRootReliefEvaluation(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LocationOfRootReliefEvaluation

    A specific implementation of 'EnumWithSelectedValue' for 'LocationOfRootReliefEvaluation' types.
    '''

    __hash__ = None
    __qualname__ = 'LocationOfRootReliefEvaluation'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_521.LocationOfRootReliefEvaluation':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _521.LocationOfRootReliefEvaluation

    @classmethod
    def implicit_type(cls) -> '_521.LocationOfRootReliefEvaluation.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _521.LocationOfRootReliefEvaluation.type_()

    @property
    def selected_value(self) -> '_521.LocationOfRootReliefEvaluation':
        '''LocationOfRootReliefEvaluation: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_521.LocationOfRootReliefEvaluation]':
        '''List[LocationOfRootReliefEvaluation]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LocationOfEvaluationUpperLimit(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LocationOfEvaluationUpperLimit

    A specific implementation of 'EnumWithSelectedValue' for 'LocationOfEvaluationUpperLimit' types.
    '''

    __hash__ = None
    __qualname__ = 'LocationOfEvaluationUpperLimit'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_520.LocationOfEvaluationUpperLimit':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _520.LocationOfEvaluationUpperLimit

    @classmethod
    def implicit_type(cls) -> '_520.LocationOfEvaluationUpperLimit.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _520.LocationOfEvaluationUpperLimit.type_()

    @property
    def selected_value(self) -> '_520.LocationOfEvaluationUpperLimit':
        '''LocationOfEvaluationUpperLimit: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_520.LocationOfEvaluationUpperLimit]':
        '''List[LocationOfEvaluationUpperLimit]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LocationOfEvaluationLowerLimit(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LocationOfEvaluationLowerLimit

    A specific implementation of 'EnumWithSelectedValue' for 'LocationOfEvaluationLowerLimit' types.
    '''

    __hash__ = None
    __qualname__ = 'LocationOfEvaluationLowerLimit'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_519.LocationOfEvaluationLowerLimit':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _519.LocationOfEvaluationLowerLimit

    @classmethod
    def implicit_type(cls) -> '_519.LocationOfEvaluationLowerLimit.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _519.LocationOfEvaluationLowerLimit.type_()

    @property
    def selected_value(self) -> '_519.LocationOfEvaluationLowerLimit':
        '''LocationOfEvaluationLowerLimit: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_519.LocationOfEvaluationLowerLimit]':
        '''List[LocationOfEvaluationLowerLimit]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_CylindricalMftRoughingMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_CylindricalMftRoughingMethods

    A specific implementation of 'EnumWithSelectedValue' for 'CylindricalMftRoughingMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalMftRoughingMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_570.CylindricalMftRoughingMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _570.CylindricalMftRoughingMethods

    @classmethod
    def implicit_type(cls) -> '_570.CylindricalMftRoughingMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _570.CylindricalMftRoughingMethods.type_()

    @property
    def selected_value(self) -> '_570.CylindricalMftRoughingMethods':
        '''CylindricalMftRoughingMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_570.CylindricalMftRoughingMethods]':
        '''List[CylindricalMftRoughingMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_CylindricalMftFinishingMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_CylindricalMftFinishingMethods

    A specific implementation of 'EnumWithSelectedValue' for 'CylindricalMftFinishingMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalMftFinishingMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_569.CylindricalMftFinishingMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _569.CylindricalMftFinishingMethods

    @classmethod
    def implicit_type(cls) -> '_569.CylindricalMftFinishingMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _569.CylindricalMftFinishingMethods.type_()

    @property
    def selected_value(self) -> '_569.CylindricalMftFinishingMethods':
        '''CylindricalMftFinishingMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_569.CylindricalMftFinishingMethods]':
        '''List[CylindricalMftFinishingMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_MicroGeometryDefinitionType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_MicroGeometryDefinitionType

    A specific implementation of 'EnumWithSelectedValue' for 'MicroGeometryDefinitionType' types.
    '''

    __hash__ = None
    __qualname__ = 'MicroGeometryDefinitionType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_592.MicroGeometryDefinitionType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _592.MicroGeometryDefinitionType

    @classmethod
    def implicit_type(cls) -> '_592.MicroGeometryDefinitionType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _592.MicroGeometryDefinitionType.type_()

    @property
    def selected_value(self) -> '_592.MicroGeometryDefinitionType':
        '''MicroGeometryDefinitionType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_592.MicroGeometryDefinitionType]':
        '''List[MicroGeometryDefinitionType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_MicroGeometryDefinitionMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_MicroGeometryDefinitionMethod

    A specific implementation of 'EnumWithSelectedValue' for 'MicroGeometryDefinitionMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'MicroGeometryDefinitionMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_591.MicroGeometryDefinitionMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _591.MicroGeometryDefinitionMethod

    @classmethod
    def implicit_type(cls) -> '_591.MicroGeometryDefinitionMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _591.MicroGeometryDefinitionMethod.type_()

    @property
    def selected_value(self) -> '_591.MicroGeometryDefinitionMethod':
        '''MicroGeometryDefinitionMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_591.MicroGeometryDefinitionMethod]':
        '''List[MicroGeometryDefinitionMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ChartType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ChartType

    A specific implementation of 'EnumWithSelectedValue' for 'ChartType' types.
    '''

    __hash__ = None
    __qualname__ = 'ChartType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_589.ChartType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _589.ChartType

    @classmethod
    def implicit_type(cls) -> '_589.ChartType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _589.ChartType.type_()

    @property
    def selected_value(self) -> '_589.ChartType':
        '''ChartType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_589.ChartType]':
        '''List[ChartType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_Flank(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_Flank

    A specific implementation of 'EnumWithSelectedValue' for 'Flank' types.
    '''

    __hash__ = None
    __qualname__ = 'Flank'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_573.Flank':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _573.Flank

    @classmethod
    def implicit_type(cls) -> '_573.Flank.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _573.Flank.type_()

    @property
    def selected_value(self) -> '_573.Flank':
        '''Flank: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_573.Flank]':
        '''List[Flank]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ActiveProcessMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ActiveProcessMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ActiveProcessMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'ActiveProcessMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_604.ActiveProcessMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _604.ActiveProcessMethod

    @classmethod
    def implicit_type(cls) -> '_604.ActiveProcessMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _604.ActiveProcessMethod.type_()

    @property
    def selected_value(self) -> '_604.ActiveProcessMethod':
        '''ActiveProcessMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_604.ActiveProcessMethod]':
        '''List[ActiveProcessMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_CutterFlankSections(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_CutterFlankSections

    A specific implementation of 'EnumWithSelectedValue' for 'CutterFlankSections' types.
    '''

    __hash__ = None
    __qualname__ = 'CutterFlankSections'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_555.CutterFlankSections':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _555.CutterFlankSections

    @classmethod
    def implicit_type(cls) -> '_555.CutterFlankSections.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _555.CutterFlankSections.type_()

    @property
    def selected_value(self) -> '_555.CutterFlankSections':
        '''CutterFlankSections: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_555.CutterFlankSections]':
        '''List[CutterFlankSections]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BasicCurveTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BasicCurveTypes

    A specific implementation of 'EnumWithSelectedValue' for 'BasicCurveTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'BasicCurveTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_273.BasicCurveTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _273.BasicCurveTypes

    @classmethod
    def implicit_type(cls) -> '_273.BasicCurveTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _273.BasicCurveTypes.type_()

    @property
    def selected_value(self) -> '_273.BasicCurveTypes':
        '''BasicCurveTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_273.BasicCurveTypes]':
        '''List[BasicCurveTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ThicknessType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ThicknessType

    A specific implementation of 'EnumWithSelectedValue' for 'ThicknessType' types.
    '''

    __hash__ = None
    __qualname__ = 'ThicknessType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1004.ThicknessType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1004.ThicknessType

    @classmethod
    def implicit_type(cls) -> '_1004.ThicknessType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1004.ThicknessType.type_()

    @property
    def selected_value(self) -> '_1004.ThicknessType':
        '''ThicknessType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1004.ThicknessType]':
        '''List[ThicknessType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ConicalManufactureMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ConicalManufactureMethods

    A specific implementation of 'EnumWithSelectedValue' for 'ConicalManufactureMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'ConicalManufactureMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1068.ConicalManufactureMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1068.ConicalManufactureMethods

    @classmethod
    def implicit_type(cls) -> '_1068.ConicalManufactureMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1068.ConicalManufactureMethods.type_()

    @property
    def selected_value(self) -> '_1068.ConicalManufactureMethods':
        '''ConicalManufactureMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1068.ConicalManufactureMethods]':
        '''List[ConicalManufactureMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ConicalMachineSettingCalculationMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ConicalMachineSettingCalculationMethods

    A specific implementation of 'EnumWithSelectedValue' for 'ConicalMachineSettingCalculationMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'ConicalMachineSettingCalculationMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1067.ConicalMachineSettingCalculationMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1067.ConicalMachineSettingCalculationMethods

    @classmethod
    def implicit_type(cls) -> '_1067.ConicalMachineSettingCalculationMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1067.ConicalMachineSettingCalculationMethods.type_()

    @property
    def selected_value(self) -> '_1067.ConicalMachineSettingCalculationMethods':
        '''ConicalMachineSettingCalculationMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1067.ConicalMachineSettingCalculationMethods]':
        '''List[ConicalMachineSettingCalculationMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_CandidateDisplayChoice(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_CandidateDisplayChoice

    A specific implementation of 'EnumWithSelectedValue' for 'CandidateDisplayChoice' types.
    '''

    __hash__ = None
    __qualname__ = 'CandidateDisplayChoice'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_835.CandidateDisplayChoice':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _835.CandidateDisplayChoice

    @classmethod
    def implicit_type(cls) -> '_835.CandidateDisplayChoice.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _835.CandidateDisplayChoice.type_()

    @property
    def selected_value(self) -> '_835.CandidateDisplayChoice':
        '''CandidateDisplayChoice: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_835.CandidateDisplayChoice]':
        '''List[CandidateDisplayChoice]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_Severity(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_Severity

    A specific implementation of 'EnumWithSelectedValue' for 'Severity' types.
    '''

    __hash__ = None
    __qualname__ = 'Severity'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1437.Severity':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1437.Severity

    @classmethod
    def implicit_type(cls) -> '_1437.Severity.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1437.Severity.type_()

    @property
    def selected_value(self) -> '_1437.Severity':
        '''Severity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1437.Severity]':
        '''List[Severity]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_GeometrySpecificationType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_GeometrySpecificationType

    A specific implementation of 'EnumWithSelectedValue' for 'GeometrySpecificationType' types.
    '''

    __hash__ = None
    __qualname__ = 'GeometrySpecificationType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_976.GeometrySpecificationType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _976.GeometrySpecificationType

    @classmethod
    def implicit_type(cls) -> '_976.GeometrySpecificationType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _976.GeometrySpecificationType.type_()

    @property
    def selected_value(self) -> '_976.GeometrySpecificationType':
        '''GeometrySpecificationType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_976.GeometrySpecificationType]':
        '''List[GeometrySpecificationType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_StatusItemSeverity(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_StatusItemSeverity

    A specific implementation of 'EnumWithSelectedValue' for 'StatusItemSeverity' types.
    '''

    __hash__ = None
    __qualname__ = 'StatusItemSeverity'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1440.StatusItemSeverity':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1440.StatusItemSeverity

    @classmethod
    def implicit_type(cls) -> '_1440.StatusItemSeverity.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1440.StatusItemSeverity.type_()

    @property
    def selected_value(self) -> '_1440.StatusItemSeverity':
        '''StatusItemSeverity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1440.StatusItemSeverity]':
        '''List[StatusItemSeverity]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LubricationMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LubricationMethods

    A specific implementation of 'EnumWithSelectedValue' for 'LubricationMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'LubricationMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_295.LubricationMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _295.LubricationMethods

    @classmethod
    def implicit_type(cls) -> '_295.LubricationMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _295.LubricationMethods.type_()

    @property
    def selected_value(self) -> '_295.LubricationMethods':
        '''LubricationMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_295.LubricationMethods]':
        '''List[LubricationMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'MicropittingCoefficientOfFrictionCalculationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'MicropittingCoefficientOfFrictionCalculationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_298.MicropittingCoefficientOfFrictionCalculationMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _298.MicropittingCoefficientOfFrictionCalculationMethod

    @classmethod
    def implicit_type(cls) -> '_298.MicropittingCoefficientOfFrictionCalculationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _298.MicropittingCoefficientOfFrictionCalculationMethod.type_()

    @property
    def selected_value(self) -> '_298.MicropittingCoefficientOfFrictionCalculationMethod':
        '''MicropittingCoefficientOfFrictionCalculationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_298.MicropittingCoefficientOfFrictionCalculationMethod]':
        '''List[MicropittingCoefficientOfFrictionCalculationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods

    A specific implementation of 'EnumWithSelectedValue' for 'ScuffingCoefficientOfFrictionMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'ScuffingCoefficientOfFrictionMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_996.ScuffingCoefficientOfFrictionMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _996.ScuffingCoefficientOfFrictionMethods

    @classmethod
    def implicit_type(cls) -> '_996.ScuffingCoefficientOfFrictionMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _996.ScuffingCoefficientOfFrictionMethods.type_()

    @property
    def selected_value(self) -> '_996.ScuffingCoefficientOfFrictionMethods':
        '''ScuffingCoefficientOfFrictionMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_996.ScuffingCoefficientOfFrictionMethods]':
        '''List[ScuffingCoefficientOfFrictionMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ContactResultType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ContactResultType

    A specific implementation of 'EnumWithSelectedValue' for 'ContactResultType' types.
    '''

    __hash__ = None
    __qualname__ = 'ContactResultType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_771.ContactResultType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _771.ContactResultType

    @classmethod
    def implicit_type(cls) -> '_771.ContactResultType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _771.ContactResultType.type_()

    @property
    def selected_value(self) -> '_771.ContactResultType':
        '''ContactResultType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_771.ContactResultType]':
        '''List[ContactResultType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_StressResultsType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_StressResultsType

    A specific implementation of 'EnumWithSelectedValue' for 'StressResultsType' types.
    '''

    __hash__ = None
    __qualname__ = 'StressResultsType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_78.StressResultsType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _78.StressResultsType

    @classmethod
    def implicit_type(cls) -> '_78.StressResultsType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _78.StressResultsType.type_()

    @property
    def selected_value(self) -> '_78.StressResultsType':
        '''StressResultsType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_78.StressResultsType]':
        '''List[StressResultsType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption

    A specific implementation of 'EnumWithSelectedValue' for 'CylindricalGearPairCreationOptions.DerivedParameterOption' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalGearPairCreationOptions.DerivedParameterOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1056.CylindricalGearPairCreationOptions.DerivedParameterOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1056.CylindricalGearPairCreationOptions.DerivedParameterOption

    @classmethod
    def implicit_type(cls) -> '_1056.CylindricalGearPairCreationOptions.DerivedParameterOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1056.CylindricalGearPairCreationOptions.DerivedParameterOption.type_()

    @property
    def selected_value(self) -> '_1056.CylindricalGearPairCreationOptions.DerivedParameterOption':
        '''CylindricalGearPairCreationOptions.DerivedParameterOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1056.CylindricalGearPairCreationOptions.DerivedParameterOption]':
        '''List[CylindricalGearPairCreationOptions.DerivedParameterOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ToothThicknessSpecificationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ToothThicknessSpecificationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ToothThicknessSpecificationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'ToothThicknessSpecificationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1100.ToothThicknessSpecificationMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1100.ToothThicknessSpecificationMethod

    @classmethod
    def implicit_type(cls) -> '_1100.ToothThicknessSpecificationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1100.ToothThicknessSpecificationMethod.type_()

    @property
    def selected_value(self) -> '_1100.ToothThicknessSpecificationMethod':
        '''ToothThicknessSpecificationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1100.ToothThicknessSpecificationMethod]':
        '''List[ToothThicknessSpecificationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LoadDistributionFactorMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LoadDistributionFactorMethods

    A specific implementation of 'EnumWithSelectedValue' for 'LoadDistributionFactorMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'LoadDistributionFactorMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1079.LoadDistributionFactorMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1079.LoadDistributionFactorMethods

    @classmethod
    def implicit_type(cls) -> '_1079.LoadDistributionFactorMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1079.LoadDistributionFactorMethods.type_()

    @property
    def selected_value(self) -> '_1079.LoadDistributionFactorMethods':
        '''LoadDistributionFactorMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1079.LoadDistributionFactorMethods]':
        '''List[LoadDistributionFactorMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods

    A specific implementation of 'EnumWithSelectedValue' for 'AGMAGleasonConicalGearGeometryMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'AGMAGleasonConicalGearGeometryMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1089.AGMAGleasonConicalGearGeometryMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1089.AGMAGleasonConicalGearGeometryMethods

    @classmethod
    def implicit_type(cls) -> '_1089.AGMAGleasonConicalGearGeometryMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1089.AGMAGleasonConicalGearGeometryMethods.type_()

    @property
    def selected_value(self) -> '_1089.AGMAGleasonConicalGearGeometryMethods':
        '''AGMAGleasonConicalGearGeometryMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1089.AGMAGleasonConicalGearGeometryMethods]':
        '''List[AGMAGleasonConicalGearGeometryMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ProSolveSolverType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ProSolveSolverType

    A specific implementation of 'EnumWithSelectedValue' for 'ProSolveSolverType' types.
    '''

    __hash__ = None
    __qualname__ = 'ProSolveSolverType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1147.ProSolveSolverType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1147.ProSolveSolverType

    @classmethod
    def implicit_type(cls) -> '_1147.ProSolveSolverType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1147.ProSolveSolverType.type_()

    @property
    def selected_value(self) -> '_1147.ProSolveSolverType':
        '''ProSolveSolverType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1147.ProSolveSolverType]':
        '''List[ProSolveSolverType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ProSolveMpcType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ProSolveMpcType

    A specific implementation of 'EnumWithSelectedValue' for 'ProSolveMpcType' types.
    '''

    __hash__ = None
    __qualname__ = 'ProSolveMpcType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1146.ProSolveMpcType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1146.ProSolveMpcType

    @classmethod
    def implicit_type(cls) -> '_1146.ProSolveMpcType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1146.ProSolveMpcType.type_()

    @property
    def selected_value(self) -> '_1146.ProSolveMpcType':
        '''ProSolveMpcType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1146.ProSolveMpcType]':
        '''List[ProSolveMpcType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ITDesignation(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ITDesignation

    A specific implementation of 'EnumWithSelectedValue' for 'ITDesignation' types.
    '''

    __hash__ = None
    __qualname__ = 'ITDesignation'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1608.ITDesignation':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1608.ITDesignation

    @classmethod
    def implicit_type(cls) -> '_1608.ITDesignation.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1608.ITDesignation.type_()

    @property
    def selected_value(self) -> '_1608.ITDesignation':
        '''ITDesignation: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1608.ITDesignation]':
        '''List[ITDesignation]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_DudleyEffectiveLengthApproximationOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_DudleyEffectiveLengthApproximationOption

    A specific implementation of 'EnumWithSelectedValue' for 'DudleyEffectiveLengthApproximationOption' types.
    '''

    __hash__ = None
    __qualname__ = 'DudleyEffectiveLengthApproximationOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1157.DudleyEffectiveLengthApproximationOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1157.DudleyEffectiveLengthApproximationOption

    @classmethod
    def implicit_type(cls) -> '_1157.DudleyEffectiveLengthApproximationOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1157.DudleyEffectiveLengthApproximationOption.type_()

    @property
    def selected_value(self) -> '_1157.DudleyEffectiveLengthApproximationOption':
        '''DudleyEffectiveLengthApproximationOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1157.DudleyEffectiveLengthApproximationOption]':
        '''List[DudleyEffectiveLengthApproximationOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_SplineRatingTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_SplineRatingTypes

    A specific implementation of 'EnumWithSelectedValue' for 'SplineRatingTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'SplineRatingTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1180.SplineRatingTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1180.SplineRatingTypes

    @classmethod
    def implicit_type(cls) -> '_1180.SplineRatingTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1180.SplineRatingTypes.type_()

    @property
    def selected_value(self) -> '_1180.SplineRatingTypes':
        '''SplineRatingTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1180.SplineRatingTypes]':
        '''List[SplineRatingTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_Modules(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_Modules

    A specific implementation of 'EnumWithSelectedValue' for 'Modules' types.
    '''

    __hash__ = None
    __qualname__ = 'Modules'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1166.Modules':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1166.Modules

    @classmethod
    def implicit_type(cls) -> '_1166.Modules.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1166.Modules.type_()

    @property
    def selected_value(self) -> '_1166.Modules':
        '''Modules: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1166.Modules]':
        '''List[Modules]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_PressureAngleTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_PressureAngleTypes

    A specific implementation of 'EnumWithSelectedValue' for 'PressureAngleTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'PressureAngleTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1167.PressureAngleTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1167.PressureAngleTypes

    @classmethod
    def implicit_type(cls) -> '_1167.PressureAngleTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1167.PressureAngleTypes.type_()

    @property
    def selected_value(self) -> '_1167.PressureAngleTypes':
        '''PressureAngleTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1167.PressureAngleTypes]':
        '''List[PressureAngleTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_SplineFitClassType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_SplineFitClassType

    A specific implementation of 'EnumWithSelectedValue' for 'SplineFitClassType' types.
    '''

    __hash__ = None
    __qualname__ = 'SplineFitClassType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1175.SplineFitClassType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1175.SplineFitClassType

    @classmethod
    def implicit_type(cls) -> '_1175.SplineFitClassType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1175.SplineFitClassType.type_()

    @property
    def selected_value(self) -> '_1175.SplineFitClassType':
        '''SplineFitClassType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1175.SplineFitClassType]':
        '''List[SplineFitClassType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_SplineToleranceClassTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_SplineToleranceClassTypes

    A specific implementation of 'EnumWithSelectedValue' for 'SplineToleranceClassTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'SplineToleranceClassTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1181.SplineToleranceClassTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1181.SplineToleranceClassTypes

    @classmethod
    def implicit_type(cls) -> '_1181.SplineToleranceClassTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1181.SplineToleranceClassTypes.type_()

    @property
    def selected_value(self) -> '_1181.SplineToleranceClassTypes':
        '''SplineToleranceClassTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1181.SplineToleranceClassTypes]':
        '''List[SplineToleranceClassTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_Table4JointInterfaceTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_Table4JointInterfaceTypes

    A specific implementation of 'EnumWithSelectedValue' for 'Table4JointInterfaceTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'Table4JointInterfaceTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1211.Table4JointInterfaceTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1211.Table4JointInterfaceTypes

    @classmethod
    def implicit_type(cls) -> '_1211.Table4JointInterfaceTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1211.Table4JointInterfaceTypes.type_()

    @property
    def selected_value(self) -> '_1211.Table4JointInterfaceTypes':
        '''Table4JointInterfaceTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1211.Table4JointInterfaceTypes]':
        '''List[Table4JointInterfaceTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ExecutableDirectoryCopier_Option(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ExecutableDirectoryCopier_Option

    A specific implementation of 'EnumWithSelectedValue' for 'ExecutableDirectoryCopier.Option' types.
    '''

    __hash__ = None
    __qualname__ = 'ExecutableDirectoryCopier.Option'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1253.ExecutableDirectoryCopier.Option':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1253.ExecutableDirectoryCopier.Option

    @classmethod
    def implicit_type(cls) -> '_1253.ExecutableDirectoryCopier.Option.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1253.ExecutableDirectoryCopier.Option.type_()

    @property
    def selected_value(self) -> '_1253.ExecutableDirectoryCopier.Option':
        '''ExecutableDirectoryCopier.Option: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1253.ExecutableDirectoryCopier.Option]':
        '''List[ExecutableDirectoryCopier.Option]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_CadPageOrientation(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_CadPageOrientation

    A specific implementation of 'EnumWithSelectedValue' for 'CadPageOrientation' types.
    '''

    __hash__ = None
    __qualname__ = 'CadPageOrientation'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1396.CadPageOrientation':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1396.CadPageOrientation

    @classmethod
    def implicit_type(cls) -> '_1396.CadPageOrientation.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1396.CadPageOrientation.type_()

    @property
    def selected_value(self) -> '_1396.CadPageOrientation':
        '''CadPageOrientation: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1396.CadPageOrientation]':
        '''List[CadPageOrientation]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RollerBearingProfileTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RollerBearingProfileTypes

    A specific implementation of 'EnumWithSelectedValue' for 'RollerBearingProfileTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'RollerBearingProfileTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1591.RollerBearingProfileTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1591.RollerBearingProfileTypes

    @classmethod
    def implicit_type(cls) -> '_1591.RollerBearingProfileTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1591.RollerBearingProfileTypes.type_()

    @property
    def selected_value(self) -> '_1591.RollerBearingProfileTypes':
        '''RollerBearingProfileTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1591.RollerBearingProfileTypes]':
        '''List[RollerBearingProfileTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_FluidFilmTemperatureOptions(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_FluidFilmTemperatureOptions

    A specific implementation of 'EnumWithSelectedValue' for 'FluidFilmTemperatureOptions' types.
    '''

    __hash__ = None
    __qualname__ = 'FluidFilmTemperatureOptions'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1584.FluidFilmTemperatureOptions':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1584.FluidFilmTemperatureOptions

    @classmethod
    def implicit_type(cls) -> '_1584.FluidFilmTemperatureOptions.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1584.FluidFilmTemperatureOptions.type_()

    @property
    def selected_value(self) -> '_1584.FluidFilmTemperatureOptions':
        '''FluidFilmTemperatureOptions: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1584.FluidFilmTemperatureOptions]':
        '''List[FluidFilmTemperatureOptions]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_SupportToleranceLocationDesignation(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_SupportToleranceLocationDesignation

    A specific implementation of 'EnumWithSelectedValue' for 'SupportToleranceLocationDesignation' types.
    '''

    __hash__ = None
    __qualname__ = 'SupportToleranceLocationDesignation'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1620.SupportToleranceLocationDesignation':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1620.SupportToleranceLocationDesignation

    @classmethod
    def implicit_type(cls) -> '_1620.SupportToleranceLocationDesignation.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1620.SupportToleranceLocationDesignation.type_()

    @property
    def selected_value(self) -> '_1620.SupportToleranceLocationDesignation':
        '''SupportToleranceLocationDesignation: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1620.SupportToleranceLocationDesignation]':
        '''List[SupportToleranceLocationDesignation]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LoadedBallElementPropertyType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LoadedBallElementPropertyType

    A specific implementation of 'EnumWithSelectedValue' for 'LoadedBallElementPropertyType' types.
    '''

    __hash__ = None
    __qualname__ = 'LoadedBallElementPropertyType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1657.LoadedBallElementPropertyType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1657.LoadedBallElementPropertyType

    @classmethod
    def implicit_type(cls) -> '_1657.LoadedBallElementPropertyType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1657.LoadedBallElementPropertyType.type_()

    @property
    def selected_value(self) -> '_1657.LoadedBallElementPropertyType':
        '''LoadedBallElementPropertyType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1657.LoadedBallElementPropertyType]':
        '''List[LoadedBallElementPropertyType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RollingBearingArrangement(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RollingBearingArrangement

    A specific implementation of 'EnumWithSelectedValue' for 'RollingBearingArrangement' types.
    '''

    __hash__ = None
    __qualname__ = 'RollingBearingArrangement'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1592.RollingBearingArrangement':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1592.RollingBearingArrangement

    @classmethod
    def implicit_type(cls) -> '_1592.RollingBearingArrangement.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1592.RollingBearingArrangement.type_()

    @property
    def selected_value(self) -> '_1592.RollingBearingArrangement':
        '''RollingBearingArrangement: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1592.RollingBearingArrangement]':
        '''List[RollingBearingArrangement]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RollingBearingRaceType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RollingBearingRaceType

    A specific implementation of 'EnumWithSelectedValue' for 'RollingBearingRaceType' types.
    '''

    __hash__ = None
    __qualname__ = 'RollingBearingRaceType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1595.RollingBearingRaceType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1595.RollingBearingRaceType

    @classmethod
    def implicit_type(cls) -> '_1595.RollingBearingRaceType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1595.RollingBearingRaceType.type_()

    @property
    def selected_value(self) -> '_1595.RollingBearingRaceType':
        '''RollingBearingRaceType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1595.RollingBearingRaceType]':
        '''List[RollingBearingRaceType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BasicDynamicLoadRatingCalculationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BasicDynamicLoadRatingCalculationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'BasicDynamicLoadRatingCalculationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'BasicDynamicLoadRatingCalculationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1572.BasicDynamicLoadRatingCalculationMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1572.BasicDynamicLoadRatingCalculationMethod

    @classmethod
    def implicit_type(cls) -> '_1572.BasicDynamicLoadRatingCalculationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1572.BasicDynamicLoadRatingCalculationMethod.type_()

    @property
    def selected_value(self) -> '_1572.BasicDynamicLoadRatingCalculationMethod':
        '''BasicDynamicLoadRatingCalculationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1572.BasicDynamicLoadRatingCalculationMethod]':
        '''List[BasicDynamicLoadRatingCalculationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'BasicStaticLoadRatingCalculationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'BasicStaticLoadRatingCalculationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1573.BasicStaticLoadRatingCalculationMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1573.BasicStaticLoadRatingCalculationMethod

    @classmethod
    def implicit_type(cls) -> '_1573.BasicStaticLoadRatingCalculationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1573.BasicStaticLoadRatingCalculationMethod.type_()

    @property
    def selected_value(self) -> '_1573.BasicStaticLoadRatingCalculationMethod':
        '''BasicStaticLoadRatingCalculationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1573.BasicStaticLoadRatingCalculationMethod]':
        '''List[BasicStaticLoadRatingCalculationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RotationalDirections(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RotationalDirections

    A specific implementation of 'EnumWithSelectedValue' for 'RotationalDirections' types.
    '''

    __hash__ = None
    __qualname__ = 'RotationalDirections'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1597.RotationalDirections':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1597.RotationalDirections

    @classmethod
    def implicit_type(cls) -> '_1597.RotationalDirections.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1597.RotationalDirections.type_()

    @property
    def selected_value(self) -> '_1597.RotationalDirections':
        '''RotationalDirections: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1597.RotationalDirections]':
        '''List[RotationalDirections]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing

    A specific implementation of 'EnumWithSelectedValue' for 'ShaftDiameterModificationDueToRollingBearingRing' types.
    '''

    __hash__ = None
    __qualname__ = 'ShaftDiameterModificationDueToRollingBearingRing'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2123.ShaftDiameterModificationDueToRollingBearingRing':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _2123.ShaftDiameterModificationDueToRollingBearingRing

    @classmethod
    def implicit_type(cls) -> '_2123.ShaftDiameterModificationDueToRollingBearingRing.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2123.ShaftDiameterModificationDueToRollingBearingRing.type_()

    @property
    def selected_value(self) -> '_2123.ShaftDiameterModificationDueToRollingBearingRing':
        '''ShaftDiameterModificationDueToRollingBearingRing: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_2123.ShaftDiameterModificationDueToRollingBearingRing]':
        '''List[ShaftDiameterModificationDueToRollingBearingRing]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ComponentOrientationOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ComponentOrientationOption

    A specific implementation of 'EnumWithSelectedValue' for 'ComponentOrientationOption' types.
    '''

    __hash__ = None
    __qualname__ = 'ComponentOrientationOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2018.ComponentOrientationOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _2018.ComponentOrientationOption

    @classmethod
    def implicit_type(cls) -> '_2018.ComponentOrientationOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2018.ComponentOrientationOption.type_()

    @property
    def selected_value(self) -> '_2018.ComponentOrientationOption':
        '''ComponentOrientationOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_2018.ComponentOrientationOption]':
        '''List[ComponentOrientationOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_Axis(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_Axis

    A specific implementation of 'EnumWithSelectedValue' for 'Axis' types.
    '''

    __hash__ = None
    __qualname__ = 'Axis'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1492.Axis':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1492.Axis

    @classmethod
    def implicit_type(cls) -> '_1492.Axis.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1492.Axis.type_()

    @property
    def selected_value(self) -> '_1492.Axis':
        '''Axis: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1492.Axis]':
        '''List[Axis]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_AlignmentAxis(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_AlignmentAxis

    A specific implementation of 'EnumWithSelectedValue' for 'AlignmentAxis' types.
    '''

    __hash__ = None
    __qualname__ = 'AlignmentAxis'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1491.AlignmentAxis':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1491.AlignmentAxis

    @classmethod
    def implicit_type(cls) -> '_1491.AlignmentAxis.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1491.AlignmentAxis.type_()

    @property
    def selected_value(self) -> '_1491.AlignmentAxis':
        '''AlignmentAxis: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1491.AlignmentAxis]':
        '''List[AlignmentAxis]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_DesignEntityId(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_DesignEntityId

    A specific implementation of 'EnumWithSelectedValue' for 'DesignEntityId' types.
    '''

    __hash__ = None
    __qualname__ = 'DesignEntityId'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1882.DesignEntityId':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1882.DesignEntityId

    @classmethod
    def implicit_type(cls) -> '_1882.DesignEntityId.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1882.DesignEntityId.type_()

    @property
    def selected_value(self) -> '_1882.DesignEntityId':
        '''DesignEntityId: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1882.DesignEntityId]':
        '''List[DesignEntityId]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_FESubstructureType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_FESubstructureType

    A specific implementation of 'EnumWithSelectedValue' for 'FESubstructureType' types.
    '''

    __hash__ = None
    __qualname__ = 'FESubstructureType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2037.FESubstructureType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _2037.FESubstructureType

    @classmethod
    def implicit_type(cls) -> '_2037.FESubstructureType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2037.FESubstructureType.type_()

    @property
    def selected_value(self) -> '_2037.FESubstructureType':
        '''FESubstructureType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_2037.FESubstructureType]':
        '''List[FESubstructureType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ThermalExpansionOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ThermalExpansionOption

    A specific implementation of 'EnumWithSelectedValue' for 'ThermalExpansionOption' types.
    '''

    __hash__ = None
    __qualname__ = 'ThermalExpansionOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2060.ThermalExpansionOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _2060.ThermalExpansionOption

    @classmethod
    def implicit_type(cls) -> '_2060.ThermalExpansionOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2060.ThermalExpansionOption.type_()

    @property
    def selected_value(self) -> '_2060.ThermalExpansionOption':
        '''ThermalExpansionOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_2060.ThermalExpansionOption]':
        '''List[ThermalExpansionOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_FEExportFormat(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_FEExportFormat

    A specific implementation of 'EnumWithSelectedValue' for 'FEExportFormat' types.
    '''

    __hash__ = None
    __qualname__ = 'FEExportFormat'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_148.FEExportFormat':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _148.FEExportFormat

    @classmethod
    def implicit_type(cls) -> '_148.FEExportFormat.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _148.FEExportFormat.type_()

    @property
    def selected_value(self) -> '_148.FEExportFormat':
        '''FEExportFormat: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_148.FEExportFormat]':
        '''List[FEExportFormat]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ThreeDViewContourOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ThreeDViewContourOption

    A specific implementation of 'EnumWithSelectedValue' for 'ThreeDViewContourOption' types.
    '''

    __hash__ = None
    __qualname__ = 'ThreeDViewContourOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1463.ThreeDViewContourOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1463.ThreeDViewContourOption

    @classmethod
    def implicit_type(cls) -> '_1463.ThreeDViewContourOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1463.ThreeDViewContourOption.type_()

    @property
    def selected_value(self) -> '_1463.ThreeDViewContourOption':
        '''ThreeDViewContourOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1463.ThreeDViewContourOption]':
        '''List[ThreeDViewContourOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BoundaryConditionType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BoundaryConditionType

    A specific implementation of 'EnumWithSelectedValue' for 'BoundaryConditionType' types.
    '''

    __hash__ = None
    __qualname__ = 'BoundaryConditionType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_147.BoundaryConditionType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _147.BoundaryConditionType

    @classmethod
    def implicit_type(cls) -> '_147.BoundaryConditionType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _147.BoundaryConditionType.type_()

    @property
    def selected_value(self) -> '_147.BoundaryConditionType':
        '''BoundaryConditionType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_147.BoundaryConditionType]':
        '''List[BoundaryConditionType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LinkNodeSource(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LinkNodeSource

    A specific implementation of 'EnumWithSelectedValue' for 'LinkNodeSource' types.
    '''

    __hash__ = None
    __qualname__ = 'LinkNodeSource'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2047.LinkNodeSource':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _2047.LinkNodeSource

    @classmethod
    def implicit_type(cls) -> '_2047.LinkNodeSource.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2047.LinkNodeSource.type_()

    @property
    def selected_value(self) -> '_2047.LinkNodeSource':
        '''LinkNodeSource: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_2047.LinkNodeSource]':
        '''List[LinkNodeSource]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BearingNodeOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BearingNodeOption

    A specific implementation of 'EnumWithSelectedValue' for 'BearingNodeOption' types.
    '''

    __hash__ = None
    __qualname__ = 'BearingNodeOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2015.BearingNodeOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _2015.BearingNodeOption

    @classmethod
    def implicit_type(cls) -> '_2015.BearingNodeOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2015.BearingNodeOption.type_()

    @property
    def selected_value(self) -> '_2015.BearingNodeOption':
        '''BearingNodeOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_2015.BearingNodeOption]':
        '''List[BearingNodeOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BearingToleranceClass(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BearingToleranceClass

    A specific implementation of 'EnumWithSelectedValue' for 'BearingToleranceClass' types.
    '''

    __hash__ = None
    __qualname__ = 'BearingToleranceClass'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1601.BearingToleranceClass':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1601.BearingToleranceClass

    @classmethod
    def implicit_type(cls) -> '_1601.BearingToleranceClass.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1601.BearingToleranceClass.type_()

    @property
    def selected_value(self) -> '_1601.BearingToleranceClass':
        '''BearingToleranceClass: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1601.BearingToleranceClass]':
        '''List[BearingToleranceClass]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BearingModel(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BearingModel

    A specific implementation of 'EnumWithSelectedValue' for 'BearingModel' types.
    '''

    __hash__ = None
    __qualname__ = 'BearingModel'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1579.BearingModel':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1579.BearingModel

    @classmethod
    def implicit_type(cls) -> '_1579.BearingModel.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1579.BearingModel.type_()

    @property
    def selected_value(self) -> '_1579.BearingModel':
        '''BearingModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1579.BearingModel]':
        '''List[BearingModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_PreloadType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_PreloadType

    A specific implementation of 'EnumWithSelectedValue' for 'PreloadType' types.
    '''

    __hash__ = None
    __qualname__ = 'PreloadType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1656.PreloadType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1656.PreloadType

    @classmethod
    def implicit_type(cls) -> '_1656.PreloadType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1656.PreloadType.type_()

    @property
    def selected_value(self) -> '_1656.PreloadType':
        '''PreloadType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1656.PreloadType]':
        '''List[PreloadType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RaceRadialMountingType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RaceRadialMountingType

    A specific implementation of 'EnumWithSelectedValue' for 'RaceRadialMountingType' types.
    '''

    __hash__ = None
    __qualname__ = 'RaceRadialMountingType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1659.RaceRadialMountingType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1659.RaceRadialMountingType

    @classmethod
    def implicit_type(cls) -> '_1659.RaceRadialMountingType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1659.RaceRadialMountingType.type_()

    @property
    def selected_value(self) -> '_1659.RaceRadialMountingType':
        '''RaceRadialMountingType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1659.RaceRadialMountingType]':
        '''List[RaceRadialMountingType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RaceAxialMountingType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RaceAxialMountingType

    A specific implementation of 'EnumWithSelectedValue' for 'RaceAxialMountingType' types.
    '''

    __hash__ = None
    __qualname__ = 'RaceAxialMountingType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1658.RaceAxialMountingType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1658.RaceAxialMountingType

    @classmethod
    def implicit_type(cls) -> '_1658.RaceAxialMountingType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1658.RaceAxialMountingType.type_()

    @property
    def selected_value(self) -> '_1658.RaceAxialMountingType':
        '''RaceAxialMountingType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1658.RaceAxialMountingType]':
        '''List[RaceAxialMountingType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BearingToleranceDefinitionOptions(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BearingToleranceDefinitionOptions

    A specific implementation of 'EnumWithSelectedValue' for 'BearingToleranceDefinitionOptions' types.
    '''

    __hash__ = None
    __qualname__ = 'BearingToleranceDefinitionOptions'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1602.BearingToleranceDefinitionOptions':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1602.BearingToleranceDefinitionOptions

    @classmethod
    def implicit_type(cls) -> '_1602.BearingToleranceDefinitionOptions.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1602.BearingToleranceDefinitionOptions.type_()

    @property
    def selected_value(self) -> '_1602.BearingToleranceDefinitionOptions':
        '''BearingToleranceDefinitionOptions: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1602.BearingToleranceDefinitionOptions]':
        '''List[BearingToleranceDefinitionOptions]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_InternalClearanceClass(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_InternalClearanceClass

    A specific implementation of 'EnumWithSelectedValue' for 'InternalClearanceClass' types.
    '''

    __hash__ = None
    __qualname__ = 'InternalClearanceClass'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1600.InternalClearanceClass':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1600.InternalClearanceClass

    @classmethod
    def implicit_type(cls) -> '_1600.InternalClearanceClass.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1600.InternalClearanceClass.type_()

    @property
    def selected_value(self) -> '_1600.InternalClearanceClass':
        '''InternalClearanceClass: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1600.InternalClearanceClass]':
        '''List[InternalClearanceClass]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_PowerLoadType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_PowerLoadType

    A specific implementation of 'EnumWithSelectedValue' for 'PowerLoadType' types.
    '''

    __hash__ = None
    __qualname__ = 'PowerLoadType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1893.PowerLoadType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1893.PowerLoadType

    @classmethod
    def implicit_type(cls) -> '_1893.PowerLoadType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1893.PowerLoadType.type_()

    @property
    def selected_value(self) -> '_1893.PowerLoadType':
        '''PowerLoadType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1893.PowerLoadType]':
        '''List[PowerLoadType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RigidConnectorTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RigidConnectorTypes

    A specific implementation of 'EnumWithSelectedValue' for 'RigidConnectorTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'RigidConnectorTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2241.RigidConnectorTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _2241.RigidConnectorTypes

    @classmethod
    def implicit_type(cls) -> '_2241.RigidConnectorTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2241.RigidConnectorTypes.type_()

    @property
    def selected_value(self) -> '_2241.RigidConnectorTypes':
        '''RigidConnectorTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_2241.RigidConnectorTypes]':
        '''List[RigidConnectorTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RigidConnectorStiffnessType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RigidConnectorStiffnessType

    A specific implementation of 'EnumWithSelectedValue' for 'RigidConnectorStiffnessType' types.
    '''

    __hash__ = None
    __qualname__ = 'RigidConnectorStiffnessType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2237.RigidConnectorStiffnessType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _2237.RigidConnectorStiffnessType

    @classmethod
    def implicit_type(cls) -> '_2237.RigidConnectorStiffnessType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2237.RigidConnectorStiffnessType.type_()

    @property
    def selected_value(self) -> '_2237.RigidConnectorStiffnessType':
        '''RigidConnectorStiffnessType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_2237.RigidConnectorStiffnessType]':
        '''List[RigidConnectorStiffnessType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_FitTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_FitTypes

    A specific implementation of 'EnumWithSelectedValue' for 'FitTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'FitTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1158.FitTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1158.FitTypes

    @classmethod
    def implicit_type(cls) -> '_1158.FitTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1158.FitTypes.type_()

    @property
    def selected_value(self) -> '_1158.FitTypes':
        '''FitTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1158.FitTypes]':
        '''List[FitTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RigidConnectorToothSpacingType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RigidConnectorToothSpacingType

    A specific implementation of 'EnumWithSelectedValue' for 'RigidConnectorToothSpacingType' types.
    '''

    __hash__ = None
    __qualname__ = 'RigidConnectorToothSpacingType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2240.RigidConnectorToothSpacingType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _2240.RigidConnectorToothSpacingType

    @classmethod
    def implicit_type(cls) -> '_2240.RigidConnectorToothSpacingType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2240.RigidConnectorToothSpacingType.type_()

    @property
    def selected_value(self) -> '_2240.RigidConnectorToothSpacingType':
        '''RigidConnectorToothSpacingType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_2240.RigidConnectorToothSpacingType]':
        '''List[RigidConnectorToothSpacingType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_DoeValueSpecificationOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_DoeValueSpecificationOption

    A specific implementation of 'EnumWithSelectedValue' for 'DoeValueSpecificationOption' types.
    '''

    __hash__ = None
    __qualname__ = 'DoeValueSpecificationOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_3978.DoeValueSpecificationOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _3978.DoeValueSpecificationOption

    @classmethod
    def implicit_type(cls) -> '_3978.DoeValueSpecificationOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _3978.DoeValueSpecificationOption.type_()

    @property
    def selected_value(self) -> '_3978.DoeValueSpecificationOption':
        '''DoeValueSpecificationOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_3978.DoeValueSpecificationOption]':
        '''List[DoeValueSpecificationOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_AnalysisType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_AnalysisType

    A specific implementation of 'EnumWithSelectedValue' for 'AnalysisType' types.
    '''

    __hash__ = None
    __qualname__ = 'AnalysisType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6416.AnalysisType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _6416.AnalysisType

    @classmethod
    def implicit_type(cls) -> '_6416.AnalysisType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6416.AnalysisType.type_()

    @property
    def selected_value(self) -> '_6416.AnalysisType':
        '''AnalysisType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_6416.AnalysisType]':
        '''List[AnalysisType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BarModelExportType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BarModelExportType

    A specific implementation of 'EnumWithSelectedValue' for 'BarModelExportType' types.
    '''

    __hash__ = None
    __qualname__ = 'BarModelExportType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_48.BarModelExportType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _48.BarModelExportType

    @classmethod
    def implicit_type(cls) -> '_48.BarModelExportType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _48.BarModelExportType.type_()

    @property
    def selected_value(self) -> '_48.BarModelExportType':
        '''BarModelExportType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_48.BarModelExportType]':
        '''List[BarModelExportType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_DynamicsResponseType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_DynamicsResponseType

    A specific implementation of 'EnumWithSelectedValue' for 'DynamicsResponseType' types.
    '''

    __hash__ = None
    __qualname__ = 'DynamicsResponseType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1506.DynamicsResponseType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1506.DynamicsResponseType

    @classmethod
    def implicit_type(cls) -> '_1506.DynamicsResponseType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1506.DynamicsResponseType.type_()

    @property
    def selected_value(self) -> '_1506.DynamicsResponseType':
        '''DynamicsResponseType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1506.DynamicsResponseType]':
        '''List[DynamicsResponseType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ComplexPartDisplayOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ComplexPartDisplayOption

    A specific implementation of 'EnumWithSelectedValue' for 'ComplexPartDisplayOption' types.
    '''

    __hash__ = None
    __qualname__ = 'ComplexPartDisplayOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1494.ComplexPartDisplayOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1494.ComplexPartDisplayOption

    @classmethod
    def implicit_type(cls) -> '_1494.ComplexPartDisplayOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1494.ComplexPartDisplayOption.type_()

    @property
    def selected_value(self) -> '_1494.ComplexPartDisplayOption':
        '''ComplexPartDisplayOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1494.ComplexPartDisplayOption]':
        '''List[ComplexPartDisplayOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_DynamicsResponseScaling(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_DynamicsResponseScaling

    A specific implementation of 'EnumWithSelectedValue' for 'DynamicsResponseScaling' types.
    '''

    __hash__ = None
    __qualname__ = 'DynamicsResponseScaling'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1505.DynamicsResponseScaling':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1505.DynamicsResponseScaling

    @classmethod
    def implicit_type(cls) -> '_1505.DynamicsResponseScaling.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1505.DynamicsResponseScaling.type_()

    @property
    def selected_value(self) -> '_1505.DynamicsResponseScaling':
        '''DynamicsResponseScaling: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1505.DynamicsResponseScaling]':
        '''List[DynamicsResponseScaling]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BearingStiffnessModel(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BearingStiffnessModel

    A specific implementation of 'EnumWithSelectedValue' for 'BearingStiffnessModel' types.
    '''

    __hash__ = None
    __qualname__ = 'BearingStiffnessModel'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_5010.BearingStiffnessModel':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _5010.BearingStiffnessModel

    @classmethod
    def implicit_type(cls) -> '_5010.BearingStiffnessModel.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5010.BearingStiffnessModel.type_()

    @property
    def selected_value(self) -> '_5010.BearingStiffnessModel':
        '''BearingStiffnessModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_5010.BearingStiffnessModel]':
        '''List[BearingStiffnessModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_GearMeshStiffnessModel(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_GearMeshStiffnessModel

    A specific implementation of 'EnumWithSelectedValue' for 'GearMeshStiffnessModel' types.
    '''

    __hash__ = None
    __qualname__ = 'GearMeshStiffnessModel'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_5062.GearMeshStiffnessModel':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _5062.GearMeshStiffnessModel

    @classmethod
    def implicit_type(cls) -> '_5062.GearMeshStiffnessModel.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5062.GearMeshStiffnessModel.type_()

    @property
    def selected_value(self) -> '_5062.GearMeshStiffnessModel':
        '''GearMeshStiffnessModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_5062.GearMeshStiffnessModel]':
        '''List[GearMeshStiffnessModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ShaftAndHousingFlexibilityOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ShaftAndHousingFlexibilityOption

    A specific implementation of 'EnumWithSelectedValue' for 'ShaftAndHousingFlexibilityOption' types.
    '''

    __hash__ = None
    __qualname__ = 'ShaftAndHousingFlexibilityOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_5107.ShaftAndHousingFlexibilityOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _5107.ShaftAndHousingFlexibilityOption

    @classmethod
    def implicit_type(cls) -> '_5107.ShaftAndHousingFlexibilityOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5107.ShaftAndHousingFlexibilityOption.type_()

    @property
    def selected_value(self) -> '_5107.ShaftAndHousingFlexibilityOption':
        '''ShaftAndHousingFlexibilityOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_5107.ShaftAndHousingFlexibilityOption]':
        '''List[ShaftAndHousingFlexibilityOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ExportOutputType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ExportOutputType

    A specific implementation of 'EnumWithSelectedValue' for 'HarmonicAnalysisFEExportOptions.ExportOutputType' types.
    '''

    __hash__ = None
    __qualname__ = 'HarmonicAnalysisFEExportOptions.ExportOutputType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_5641.HarmonicAnalysisFEExportOptions.ExportOutputType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _5641.HarmonicAnalysisFEExportOptions.ExportOutputType

    @classmethod
    def implicit_type(cls) -> '_5641.HarmonicAnalysisFEExportOptions.ExportOutputType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5641.HarmonicAnalysisFEExportOptions.ExportOutputType.type_()

    @property
    def selected_value(self) -> '_5641.HarmonicAnalysisFEExportOptions.ExportOutputType':
        '''HarmonicAnalysisFEExportOptions.ExportOutputType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_5641.HarmonicAnalysisFEExportOptions.ExportOutputType]':
        '''List[HarmonicAnalysisFEExportOptions.ExportOutputType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_HarmonicAnalysisFEExportOptions_ComplexNumberOutput

    A specific implementation of 'EnumWithSelectedValue' for 'HarmonicAnalysisFEExportOptions.ComplexNumberOutput' types.
    '''

    __hash__ = None
    __qualname__ = 'HarmonicAnalysisFEExportOptions.ComplexNumberOutput'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_5641.HarmonicAnalysisFEExportOptions.ComplexNumberOutput':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _5641.HarmonicAnalysisFEExportOptions.ComplexNumberOutput

    @classmethod
    def implicit_type(cls) -> '_5641.HarmonicAnalysisFEExportOptions.ComplexNumberOutput.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5641.HarmonicAnalysisFEExportOptions.ComplexNumberOutput.type_()

    @property
    def selected_value(self) -> '_5641.HarmonicAnalysisFEExportOptions.ComplexNumberOutput':
        '''HarmonicAnalysisFEExportOptions.ComplexNumberOutput: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_5641.HarmonicAnalysisFEExportOptions.ComplexNumberOutput]':
        '''List[HarmonicAnalysisFEExportOptions.ComplexNumberOutput]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_StressConcentrationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_StressConcentrationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'StressConcentrationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'StressConcentrationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1795.StressConcentrationMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1795.StressConcentrationMethod

    @classmethod
    def implicit_type(cls) -> '_1795.StressConcentrationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1795.StressConcentrationMethod.type_()

    @property
    def selected_value(self) -> '_1795.StressConcentrationMethod':
        '''StressConcentrationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1795.StressConcentrationMethod]':
        '''List[StressConcentrationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_MeshStiffnessModel(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_MeshStiffnessModel

    A specific implementation of 'EnumWithSelectedValue' for 'MeshStiffnessModel' types.
    '''

    __hash__ = None
    __qualname__ = 'MeshStiffnessModel'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1889.MeshStiffnessModel':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1889.MeshStiffnessModel

    @classmethod
    def implicit_type(cls) -> '_1889.MeshStiffnessModel.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1889.MeshStiffnessModel.type_()

    @property
    def selected_value(self) -> '_1889.MeshStiffnessModel':
        '''MeshStiffnessModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1889.MeshStiffnessModel]':
        '''List[MeshStiffnessModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'HertzianContactDeflectionCalculationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'HertzianContactDeflectionCalculationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1569.HertzianContactDeflectionCalculationMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1569.HertzianContactDeflectionCalculationMethod

    @classmethod
    def implicit_type(cls) -> '_1569.HertzianContactDeflectionCalculationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1569.HertzianContactDeflectionCalculationMethod.type_()

    @property
    def selected_value(self) -> '_1569.HertzianContactDeflectionCalculationMethod':
        '''HertzianContactDeflectionCalculationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1569.HertzianContactDeflectionCalculationMethod]':
        '''List[HertzianContactDeflectionCalculationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_TorqueRippleInputType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_TorqueRippleInputType

    A specific implementation of 'EnumWithSelectedValue' for 'TorqueRippleInputType' types.
    '''

    __hash__ = None
    __qualname__ = 'TorqueRippleInputType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6575.TorqueRippleInputType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _6575.TorqueRippleInputType

    @classmethod
    def implicit_type(cls) -> '_6575.TorqueRippleInputType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6575.TorqueRippleInputType.type_()

    @property
    def selected_value(self) -> '_6575.TorqueRippleInputType':
        '''TorqueRippleInputType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_6575.TorqueRippleInputType]':
        '''List[TorqueRippleInputType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_HarmonicLoadDataType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_HarmonicLoadDataType

    A specific implementation of 'EnumWithSelectedValue' for 'HarmonicLoadDataType' types.
    '''

    __hash__ = None
    __qualname__ = 'HarmonicLoadDataType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6501.HarmonicLoadDataType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _6501.HarmonicLoadDataType

    @classmethod
    def implicit_type(cls) -> '_6501.HarmonicLoadDataType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6501.HarmonicLoadDataType.type_()

    @property
    def selected_value(self) -> '_6501.HarmonicLoadDataType':
        '''HarmonicLoadDataType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_6501.HarmonicLoadDataType]':
        '''List[HarmonicLoadDataType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_HarmonicExcitationType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_HarmonicExcitationType

    A specific implementation of 'EnumWithSelectedValue' for 'HarmonicExcitationType' types.
    '''

    __hash__ = None
    __qualname__ = 'HarmonicExcitationType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6494.HarmonicExcitationType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _6494.HarmonicExcitationType

    @classmethod
    def implicit_type(cls) -> '_6494.HarmonicExcitationType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6494.HarmonicExcitationType.type_()

    @property
    def selected_value(self) -> '_6494.HarmonicExcitationType':
        '''HarmonicExcitationType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_6494.HarmonicExcitationType]':
        '''List[HarmonicExcitationType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification

    A specific implementation of 'EnumWithSelectedValue' for 'PointLoadLoadCase.ForceSpecification' types.
    '''

    __hash__ = None
    __qualname__ = 'PointLoadLoadCase.ForceSpecification'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6534.PointLoadLoadCase.ForceSpecification':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _6534.PointLoadLoadCase.ForceSpecification

    @classmethod
    def implicit_type(cls) -> '_6534.PointLoadLoadCase.ForceSpecification.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6534.PointLoadLoadCase.ForceSpecification.type_()

    @property
    def selected_value(self) -> '_6534.PointLoadLoadCase.ForceSpecification':
        '''PointLoadLoadCase.ForceSpecification: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_6534.PointLoadLoadCase.ForceSpecification]':
        '''List[PointLoadLoadCase.ForceSpecification]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'PowerLoadInputTorqueSpecificationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'PowerLoadInputTorqueSpecificationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1891.PowerLoadInputTorqueSpecificationMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1891.PowerLoadInputTorqueSpecificationMethod

    @classmethod
    def implicit_type(cls) -> '_1891.PowerLoadInputTorqueSpecificationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1891.PowerLoadInputTorqueSpecificationMethod.type_()

    @property
    def selected_value(self) -> '_1891.PowerLoadInputTorqueSpecificationMethod':
        '''PowerLoadInputTorqueSpecificationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1891.PowerLoadInputTorqueSpecificationMethod]':
        '''List[PowerLoadInputTorqueSpecificationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_TorqueSpecificationForSystemDeflection(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_TorqueSpecificationForSystemDeflection

    A specific implementation of 'EnumWithSelectedValue' for 'TorqueSpecificationForSystemDeflection' types.
    '''

    __hash__ = None
    __qualname__ = 'TorqueSpecificationForSystemDeflection'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6576.TorqueSpecificationForSystemDeflection':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _6576.TorqueSpecificationForSystemDeflection

    @classmethod
    def implicit_type(cls) -> '_6576.TorqueSpecificationForSystemDeflection.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6576.TorqueSpecificationForSystemDeflection.type_()

    @property
    def selected_value(self) -> '_6576.TorqueSpecificationForSystemDeflection':
        '''TorqueSpecificationForSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_6576.TorqueSpecificationForSystemDeflection]':
        '''List[TorqueSpecificationForSystemDeflection]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_TorqueConverterLockupRule(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_TorqueConverterLockupRule

    A specific implementation of 'EnumWithSelectedValue' for 'TorqueConverterLockupRule' types.
    '''

    __hash__ = None
    __qualname__ = 'TorqueConverterLockupRule'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_5132.TorqueConverterLockupRule':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _5132.TorqueConverterLockupRule

    @classmethod
    def implicit_type(cls) -> '_5132.TorqueConverterLockupRule.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5132.TorqueConverterLockupRule.type_()

    @property
    def selected_value(self) -> '_5132.TorqueConverterLockupRule':
        '''TorqueConverterLockupRule: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_5132.TorqueConverterLockupRule]':
        '''List[TorqueConverterLockupRule]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_DegreesOfFreedom(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_DegreesOfFreedom

    A specific implementation of 'EnumWithSelectedValue' for 'DegreesOfFreedom' types.
    '''

    __hash__ = None
    __qualname__ = 'DegreesOfFreedom'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1503.DegreesOfFreedom':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1503.DegreesOfFreedom

    @classmethod
    def implicit_type(cls) -> '_1503.DegreesOfFreedom.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1503.DegreesOfFreedom.type_()

    @property
    def selected_value(self) -> '_1503.DegreesOfFreedom':
        '''DegreesOfFreedom: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1503.DegreesOfFreedom]':
        '''List[DegreesOfFreedom]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_DestinationDesignState(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_DestinationDesignState

    A specific implementation of 'EnumWithSelectedValue' for 'DestinationDesignState' types.
    '''

    __hash__ = None
    __qualname__ = 'DestinationDesignState'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6590.DestinationDesignState':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _6590.DestinationDesignState

    @classmethod
    def implicit_type(cls) -> '_6590.DestinationDesignState.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6590.DestinationDesignState.type_()

    @property
    def selected_value(self) -> '_6590.DestinationDesignState':
        '''DestinationDesignState: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_6590.DestinationDesignState]':
        '''List[DestinationDesignState]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None
