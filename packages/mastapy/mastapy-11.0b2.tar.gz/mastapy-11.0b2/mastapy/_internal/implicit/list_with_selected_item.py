'''list_with_selected_item.py

Implementations of 'ListWithSelectedItem' in Python.
As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
'''


from typing import List, Generic, TypeVar

from mastapy._internal import mixins, constructor, conversion
from mastapy._internal.python_net import python_net_import
from mastapy.gears.ltca.cylindrical import _792, _791
from mastapy.gears.manufacturing.cylindrical import _571
from mastapy.gears.manufacturing.bevel import _737
from mastapy.utility import _1269
from mastapy.utility.units_and_measurements import (
    _1279, _1271, _1272, _1273,
    _1277, _1278, _1280, _1274
)
from mastapy._internal.cast_exception import CastException
from mastapy.utility.units_and_measurements.measurements import (
    _1281, _1282, _1283, _1284,
    _1285, _1286, _1287, _1288,
    _1289, _1290, _1291, _1292,
    _1293, _1294, _1295, _1296,
    _1297, _1298, _1299, _1300,
    _1301, _1302, _1303, _1304,
    _1305, _1306, _1307, _1308,
    _1309, _1310, _1311, _1312,
    _1313, _1314, _1315, _1316,
    _1317, _1318, _1319, _1320,
    _1321, _1322, _1323, _1324,
    _1325, _1326, _1327, _1328,
    _1329, _1330, _1331, _1332,
    _1333, _1334, _1335, _1336,
    _1337, _1338, _1339, _1340,
    _1341, _1342, _1343, _1344,
    _1345, _1346, _1347, _1348,
    _1349, _1350, _1351, _1352,
    _1353, _1354, _1355, _1356,
    _1357, _1358, _1359, _1360,
    _1361, _1362, _1363, _1364,
    _1365, _1366, _1367, _1368,
    _1369, _1370, _1371, _1372,
    _1373, _1374, _1375, _1376,
    _1377, _1378, _1379, _1380,
    _1381, _1382, _1383, _1384,
    _1385, _1386, _1387, _1388
)
from mastapy.utility.file_access_helpers import _1460
from mastapy.system_model.part_model import (
    _2120, _2097, _2093, _2085,
    _2086, _2089, _2091, _2096,
    _2100, _2101, _2103, _2110,
    _2111, _2112, _2114, _2117,
    _2119, _2125, _2126
)
from mastapy.system_model.part_model.gears import (
    _2178, _2160, _2162, _2166,
    _2168, _2170, _2172, _2175,
    _2181, _2183, _2185, _2187,
    _2188, _2190, _2192, _2194,
    _2198, _2200, _2159, _2161,
    _2163, _2164, _2165, _2167,
    _2169, _2171, _2173, _2174,
    _2176, _2180, _2182, _2184,
    _2186, _2189, _2191, _2193,
    _2195, _2196, _2197, _2199
)
from mastapy.system_model.fe import _2036, _2034, _2025
from mastapy.system_model.part_model.shaft_model import _2129
from mastapy.system_model.part_model.cycloidal import _2215, _2216
from mastapy.system_model.part_model.couplings import (
    _2225, _2228, _2230, _2233,
    _2235, _2236, _2242, _2244,
    _2246, _2249, _2250, _2251,
    _2253, _2255
)
from mastapy.system_model.fe.links import (
    _2067, _2068, _2070, _2071,
    _2072, _2073, _2074, _2075,
    _2076, _2077, _2078, _2079,
    _2080, _2081
)
from mastapy.system_model.part_model.part_groups import _2134
from mastapy.gears.gear_designs import _879
from mastapy.gears.gear_designs.zerol_bevel import _883
from mastapy.gears.gear_designs.worm import _888
from mastapy.gears.gear_designs.straight_bevel_diff import _892
from mastapy.gears.gear_designs.straight_bevel import _896
from mastapy.gears.gear_designs.spiral_bevel import _900
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _904
from mastapy.gears.gear_designs.klingelnberg_hypoid import _908
from mastapy.gears.gear_designs.klingelnberg_conical import _912
from mastapy.gears.gear_designs.hypoid import _916
from mastapy.gears.gear_designs.face import _924
from mastapy.gears.gear_designs.cylindrical import _955, _966
from mastapy.gears.gear_designs.conical import _1066
from mastapy.gears.gear_designs.concept import _1088
from mastapy.gears.gear_designs.bevel import _1092
from mastapy.gears.gear_designs.agma_gleason_conical import _1105
from mastapy.system_model.analyses_and_results.system_deflections import (
    _2380, _2381, _2382, _2383
)
from mastapy.system_model.analyses_and_results.load_case_groups import _5286, _5287
from mastapy.system_model.analyses_and_results.harmonic_analyses.results import _5725
from mastapy.system_model.analyses_and_results.static_loads import _6556, _6410
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4016

_ARRAY = python_net_import('System', 'Array')
_LIST_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.Utility.Property', 'ListWithSelectedItem')


__docformat__ = 'restructuredtext en'
__all__ = (
    'ListWithSelectedItem_int', 'ListWithSelectedItem_str',
    'ListWithSelectedItem_T', 'ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis',
    'ListWithSelectedItem_CylindricalGearLoadDistributionAnalysis', 'ListWithSelectedItem_CylindricalSetManufacturingConfig',
    'ListWithSelectedItem_ConicalSetManufacturingConfig', 'ListWithSelectedItem_SystemDirectory',
    'ListWithSelectedItem_Unit', 'ListWithSelectedItem_MeasurementBase',
    'ListWithSelectedItem_ColumnTitle', 'ListWithSelectedItem_PowerLoad',
    'ListWithSelectedItem_GearSet', 'ListWithSelectedItem_FESubstructureNode',
    'ListWithSelectedItem_Datum', 'ListWithSelectedItem_Component',
    'ListWithSelectedItem_FELink', 'ListWithSelectedItem_FESubstructure',
    'ListWithSelectedItem_CylindricalGear', 'ListWithSelectedItem_GuideDxfModel',
    'ListWithSelectedItem_ConcentricPartGroup', 'ListWithSelectedItem_CylindricalGearSet',
    'ListWithSelectedItem_GearSetDesign', 'ListWithSelectedItem_ShaftHubConnection',
    'ListWithSelectedItem_TSelectableItem', 'ListWithSelectedItem_CylindricalGearSystemDeflection',
    'ListWithSelectedItem_DesignState', 'ListWithSelectedItem_FEPart',
    'ListWithSelectedItem_ResultLocationSelectionGroup', 'ListWithSelectedItem_StaticLoadCase',
    'ListWithSelectedItem_DutyCycle', 'ListWithSelectedItem_float',
    'ListWithSelectedItem_ElectricMachineDataSet', 'ListWithSelectedItem_PointLoad'
)


T = TypeVar('T')
TSelectableItem = TypeVar('TSelectableItem')


class ListWithSelectedItem_int(int, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_int

    A specific implementation of 'ListWithSelectedItem' for 'int' types.
    '''

    __hash__ = None
    __qualname__ = 'int'

    def __new__(cls, instance_to_wrap: 'ListWithSelectedItem_int.TYPE'):
        return int.__new__(cls, instance_to_wrap.SelectedValue) if instance_to_wrap.SelectedValue else 0

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_int.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.SelectedValue
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> 'int':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return int

    @property
    def selected_value(self) -> 'int':
        '''int: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.SelectedValue

    @property
    def available_values(self) -> 'List[int]':
        '''List[int]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, int)
        return value


class ListWithSelectedItem_str(str, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_str

    A specific implementation of 'ListWithSelectedItem' for 'str' types.
    '''

    __hash__ = None
    __qualname__ = 'str'

    def __new__(cls, instance_to_wrap: 'ListWithSelectedItem_str.TYPE'):
        return str.__new__(cls, instance_to_wrap.SelectedValue) if instance_to_wrap.SelectedValue else None

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_str.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.SelectedValue
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> 'str':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return str

    @property
    def selected_value(self) -> 'str':
        '''str: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.SelectedValue

    @property
    def available_values(self) -> 'List[str]':
        '''List[str]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, str)
        return value


class ListWithSelectedItem_T(Generic[T], mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_T

    A specific implementation of 'ListWithSelectedItem' for 'T' types.
    '''

    __hash__ = None
    __qualname__ = 'T'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_T.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.SelectedValue
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> 'T':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return T

    @property
    def selected_value(self) -> 'T':
        '''T: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(T)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[T]':
        '''List[T]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(T))
        return value


class ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis(_792.CylindricalGearMeshLoadDistributionAnalysis, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalGearMeshLoadDistributionAnalysis' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalGearMeshLoadDistributionAnalysis'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_CylindricalGearMeshLoadDistributionAnalysis.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_792.CylindricalGearMeshLoadDistributionAnalysis.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _792.CylindricalGearMeshLoadDistributionAnalysis.TYPE

    @property
    def selected_value(self) -> '_792.CylindricalGearMeshLoadDistributionAnalysis':
        '''CylindricalGearMeshLoadDistributionAnalysis: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_792.CylindricalGearMeshLoadDistributionAnalysis)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_792.CylindricalGearMeshLoadDistributionAnalysis]':
        '''List[CylindricalGearMeshLoadDistributionAnalysis]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_792.CylindricalGearMeshLoadDistributionAnalysis))
        return value


class ListWithSelectedItem_CylindricalGearLoadDistributionAnalysis(_791.CylindricalGearLoadDistributionAnalysis, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_CylindricalGearLoadDistributionAnalysis

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalGearLoadDistributionAnalysis' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalGearLoadDistributionAnalysis'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_CylindricalGearLoadDistributionAnalysis.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_791.CylindricalGearLoadDistributionAnalysis.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _791.CylindricalGearLoadDistributionAnalysis.TYPE

    @property
    def selected_value(self) -> '_791.CylindricalGearLoadDistributionAnalysis':
        '''CylindricalGearLoadDistributionAnalysis: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_791.CylindricalGearLoadDistributionAnalysis)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_791.CylindricalGearLoadDistributionAnalysis]':
        '''List[CylindricalGearLoadDistributionAnalysis]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_791.CylindricalGearLoadDistributionAnalysis))
        return value


class ListWithSelectedItem_CylindricalSetManufacturingConfig(_571.CylindricalSetManufacturingConfig, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_CylindricalSetManufacturingConfig

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalSetManufacturingConfig' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalSetManufacturingConfig'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_CylindricalSetManufacturingConfig.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_571.CylindricalSetManufacturingConfig.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _571.CylindricalSetManufacturingConfig.TYPE

    @property
    def selected_value(self) -> '_571.CylindricalSetManufacturingConfig':
        '''CylindricalSetManufacturingConfig: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_571.CylindricalSetManufacturingConfig)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_571.CylindricalSetManufacturingConfig]':
        '''List[CylindricalSetManufacturingConfig]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_571.CylindricalSetManufacturingConfig))
        return value


class ListWithSelectedItem_ConicalSetManufacturingConfig(_737.ConicalSetManufacturingConfig, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ConicalSetManufacturingConfig

    A specific implementation of 'ListWithSelectedItem' for 'ConicalSetManufacturingConfig' types.
    '''

    __hash__ = None
    __qualname__ = 'ConicalSetManufacturingConfig'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ConicalSetManufacturingConfig.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_737.ConicalSetManufacturingConfig.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _737.ConicalSetManufacturingConfig.TYPE

    @property
    def selected_value(self) -> '_737.ConicalSetManufacturingConfig':
        '''ConicalSetManufacturingConfig: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_737.ConicalSetManufacturingConfig)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_737.ConicalSetManufacturingConfig]':
        '''List[ConicalSetManufacturingConfig]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_737.ConicalSetManufacturingConfig))
        return value


class ListWithSelectedItem_SystemDirectory(_1269.SystemDirectory, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_SystemDirectory

    A specific implementation of 'ListWithSelectedItem' for 'SystemDirectory' types.
    '''

    __hash__ = None
    __qualname__ = 'SystemDirectory'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_SystemDirectory.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_1269.SystemDirectory.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1269.SystemDirectory.TYPE

    @property
    def selected_value(self) -> '_1269.SystemDirectory':
        '''SystemDirectory: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1269.SystemDirectory)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_1269.SystemDirectory]':
        '''List[SystemDirectory]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1269.SystemDirectory))
        return value


class ListWithSelectedItem_Unit(_1279.Unit, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_Unit

    A specific implementation of 'ListWithSelectedItem' for 'Unit' types.
    '''

    __hash__ = None
    __qualname__ = 'Unit'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_Unit.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_1279.Unit.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1279.Unit.TYPE

    @property
    def selected_value(self) -> '_1279.Unit':
        '''Unit: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1279.Unit.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Unit. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_1279.Unit]':
        '''List[Unit]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1279.Unit))
        return value


class ListWithSelectedItem_MeasurementBase(_1274.MeasurementBase, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_MeasurementBase

    A specific implementation of 'ListWithSelectedItem' for 'MeasurementBase' types.
    '''

    __hash__ = None
    __qualname__ = 'MeasurementBase'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_MeasurementBase.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_1274.MeasurementBase.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1274.MeasurementBase.TYPE

    @property
    def selected_value(self) -> '_1274.MeasurementBase':
        '''MeasurementBase: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1274.MeasurementBase.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MeasurementBase. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_acceleration(self) -> '_1281.Acceleration':
        '''Acceleration: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1281.Acceleration.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Acceleration. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_angle(self) -> '_1282.Angle':
        '''Angle: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1282.Angle.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Angle. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_angle_per_unit_temperature(self) -> '_1283.AnglePerUnitTemperature':
        '''AnglePerUnitTemperature: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1283.AnglePerUnitTemperature.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AnglePerUnitTemperature. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_angle_small(self) -> '_1284.AngleSmall':
        '''AngleSmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1284.AngleSmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngleSmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_angle_very_small(self) -> '_1285.AngleVerySmall':
        '''AngleVerySmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1285.AngleVerySmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngleVerySmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_angular_acceleration(self) -> '_1286.AngularAcceleration':
        '''AngularAcceleration: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1286.AngularAcceleration.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngularAcceleration. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_angular_compliance(self) -> '_1287.AngularCompliance':
        '''AngularCompliance: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1287.AngularCompliance.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngularCompliance. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_angular_jerk(self) -> '_1288.AngularJerk':
        '''AngularJerk: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1288.AngularJerk.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngularJerk. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_angular_stiffness(self) -> '_1289.AngularStiffness':
        '''AngularStiffness: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1289.AngularStiffness.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngularStiffness. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_angular_velocity(self) -> '_1290.AngularVelocity':
        '''AngularVelocity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1290.AngularVelocity.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AngularVelocity. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_area(self) -> '_1291.Area':
        '''Area: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1291.Area.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Area. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_area_small(self) -> '_1292.AreaSmall':
        '''AreaSmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1292.AreaSmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AreaSmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_cycles(self) -> '_1293.Cycles':
        '''Cycles: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1293.Cycles.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Cycles. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_damage(self) -> '_1294.Damage':
        '''Damage: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1294.Damage.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Damage. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_damage_rate(self) -> '_1295.DamageRate':
        '''DamageRate: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1295.DamageRate.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to DamageRate. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_data_size(self) -> '_1296.DataSize':
        '''DataSize: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1296.DataSize.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to DataSize. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_decibel(self) -> '_1297.Decibel':
        '''Decibel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1297.Decibel.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Decibel. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_density(self) -> '_1298.Density':
        '''Density: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1298.Density.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Density. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_energy(self) -> '_1299.Energy':
        '''Energy: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1299.Energy.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Energy. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_energy_per_unit_area(self) -> '_1300.EnergyPerUnitArea':
        '''EnergyPerUnitArea: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1300.EnergyPerUnitArea.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to EnergyPerUnitArea. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_energy_per_unit_area_small(self) -> '_1301.EnergyPerUnitAreaSmall':
        '''EnergyPerUnitAreaSmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1301.EnergyPerUnitAreaSmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to EnergyPerUnitAreaSmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_energy_small(self) -> '_1302.EnergySmall':
        '''EnergySmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1302.EnergySmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to EnergySmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_enum(self) -> '_1303.Enum':
        '''Enum: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1303.Enum.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Enum. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_flow_rate(self) -> '_1304.FlowRate':
        '''FlowRate: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1304.FlowRate.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FlowRate. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_force(self) -> '_1305.Force':
        '''Force: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1305.Force.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Force. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_force_per_unit_length(self) -> '_1306.ForcePerUnitLength':
        '''ForcePerUnitLength: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1306.ForcePerUnitLength.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ForcePerUnitLength. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_force_per_unit_pressure(self) -> '_1307.ForcePerUnitPressure':
        '''ForcePerUnitPressure: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1307.ForcePerUnitPressure.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ForcePerUnitPressure. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_force_per_unit_temperature(self) -> '_1308.ForcePerUnitTemperature':
        '''ForcePerUnitTemperature: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1308.ForcePerUnitTemperature.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ForcePerUnitTemperature. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_fraction_measurement_base(self) -> '_1309.FractionMeasurementBase':
        '''FractionMeasurementBase: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1309.FractionMeasurementBase.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FractionMeasurementBase. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_frequency(self) -> '_1310.Frequency':
        '''Frequency: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1310.Frequency.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Frequency. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_fuel_consumption_engine(self) -> '_1311.FuelConsumptionEngine':
        '''FuelConsumptionEngine: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1311.FuelConsumptionEngine.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FuelConsumptionEngine. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_fuel_efficiency_vehicle(self) -> '_1312.FuelEfficiencyVehicle':
        '''FuelEfficiencyVehicle: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1312.FuelEfficiencyVehicle.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FuelEfficiencyVehicle. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_gradient(self) -> '_1313.Gradient':
        '''Gradient: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1313.Gradient.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Gradient. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_heat_conductivity(self) -> '_1314.HeatConductivity':
        '''HeatConductivity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1314.HeatConductivity.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HeatConductivity. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_heat_transfer(self) -> '_1315.HeatTransfer':
        '''HeatTransfer: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1315.HeatTransfer.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HeatTransfer. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_heat_transfer_coefficient_for_plastic_gear_tooth(self) -> '_1316.HeatTransferCoefficientForPlasticGearTooth':
        '''HeatTransferCoefficientForPlasticGearTooth: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1316.HeatTransferCoefficientForPlasticGearTooth.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HeatTransferCoefficientForPlasticGearTooth. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_heat_transfer_resistance(self) -> '_1317.HeatTransferResistance':
        '''HeatTransferResistance: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1317.HeatTransferResistance.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HeatTransferResistance. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_impulse(self) -> '_1318.Impulse':
        '''Impulse: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1318.Impulse.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Impulse. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_index(self) -> '_1319.Index':
        '''Index: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1319.Index.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Index. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_integer(self) -> '_1320.Integer':
        '''Integer: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1320.Integer.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Integer. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_inverse_short_length(self) -> '_1321.InverseShortLength':
        '''InverseShortLength: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1321.InverseShortLength.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to InverseShortLength. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_inverse_short_time(self) -> '_1322.InverseShortTime':
        '''InverseShortTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1322.InverseShortTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to InverseShortTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_jerk(self) -> '_1323.Jerk':
        '''Jerk: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1323.Jerk.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Jerk. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_kinematic_viscosity(self) -> '_1324.KinematicViscosity':
        '''KinematicViscosity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1324.KinematicViscosity.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KinematicViscosity. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_length_long(self) -> '_1325.LengthLong':
        '''LengthLong: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1325.LengthLong.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthLong. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_length_medium(self) -> '_1326.LengthMedium':
        '''LengthMedium: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1326.LengthMedium.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthMedium. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_length_per_unit_temperature(self) -> '_1327.LengthPerUnitTemperature':
        '''LengthPerUnitTemperature: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1327.LengthPerUnitTemperature.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthPerUnitTemperature. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_length_short(self) -> '_1328.LengthShort':
        '''LengthShort: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1328.LengthShort.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthShort. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_length_to_the_fourth(self) -> '_1329.LengthToTheFourth':
        '''LengthToTheFourth: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1329.LengthToTheFourth.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthToTheFourth. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_length_very_long(self) -> '_1330.LengthVeryLong':
        '''LengthVeryLong: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1330.LengthVeryLong.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthVeryLong. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_length_very_short(self) -> '_1331.LengthVeryShort':
        '''LengthVeryShort: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1331.LengthVeryShort.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthVeryShort. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_length_very_short_per_length_short(self) -> '_1332.LengthVeryShortPerLengthShort':
        '''LengthVeryShortPerLengthShort: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1332.LengthVeryShortPerLengthShort.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LengthVeryShortPerLengthShort. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_linear_angular_damping(self) -> '_1333.LinearAngularDamping':
        '''LinearAngularDamping: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1333.LinearAngularDamping.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LinearAngularDamping. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_linear_angular_stiffness_cross_term(self) -> '_1334.LinearAngularStiffnessCrossTerm':
        '''LinearAngularStiffnessCrossTerm: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1334.LinearAngularStiffnessCrossTerm.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LinearAngularStiffnessCrossTerm. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_linear_damping(self) -> '_1335.LinearDamping':
        '''LinearDamping: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1335.LinearDamping.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LinearDamping. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_linear_flexibility(self) -> '_1336.LinearFlexibility':
        '''LinearFlexibility: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1336.LinearFlexibility.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LinearFlexibility. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_linear_stiffness(self) -> '_1337.LinearStiffness':
        '''LinearStiffness: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1337.LinearStiffness.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to LinearStiffness. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_mass(self) -> '_1338.Mass':
        '''Mass: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1338.Mass.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Mass. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_mass_per_unit_length(self) -> '_1339.MassPerUnitLength':
        '''MassPerUnitLength: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1339.MassPerUnitLength.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MassPerUnitLength. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_mass_per_unit_time(self) -> '_1340.MassPerUnitTime':
        '''MassPerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1340.MassPerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MassPerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_moment_of_inertia(self) -> '_1341.MomentOfInertia':
        '''MomentOfInertia: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1341.MomentOfInertia.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MomentOfInertia. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_moment_of_inertia_per_unit_length(self) -> '_1342.MomentOfInertiaPerUnitLength':
        '''MomentOfInertiaPerUnitLength: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1342.MomentOfInertiaPerUnitLength.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MomentOfInertiaPerUnitLength. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_moment_per_unit_pressure(self) -> '_1343.MomentPerUnitPressure':
        '''MomentPerUnitPressure: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1343.MomentPerUnitPressure.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MomentPerUnitPressure. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_number(self) -> '_1344.Number':
        '''Number: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1344.Number.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Number. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_percentage(self) -> '_1345.Percentage':
        '''Percentage: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1345.Percentage.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Percentage. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_power(self) -> '_1346.Power':
        '''Power: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1346.Power.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Power. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_power_per_small_area(self) -> '_1347.PowerPerSmallArea':
        '''PowerPerSmallArea: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1347.PowerPerSmallArea.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerPerSmallArea. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_power_per_unit_time(self) -> '_1348.PowerPerUnitTime':
        '''PowerPerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1348.PowerPerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerPerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_power_small(self) -> '_1349.PowerSmall':
        '''PowerSmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1349.PowerSmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerSmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_power_small_per_area(self) -> '_1350.PowerSmallPerArea':
        '''PowerSmallPerArea: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1350.PowerSmallPerArea.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerSmallPerArea. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_power_small_per_unit_area_per_unit_time(self) -> '_1351.PowerSmallPerUnitAreaPerUnitTime':
        '''PowerSmallPerUnitAreaPerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1351.PowerSmallPerUnitAreaPerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerSmallPerUnitAreaPerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_power_small_per_unit_time(self) -> '_1352.PowerSmallPerUnitTime':
        '''PowerSmallPerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1352.PowerSmallPerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerSmallPerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_pressure(self) -> '_1353.Pressure':
        '''Pressure: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1353.Pressure.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Pressure. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_pressure_per_unit_time(self) -> '_1354.PressurePerUnitTime':
        '''PressurePerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1354.PressurePerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PressurePerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_pressure_velocity_product(self) -> '_1355.PressureVelocityProduct':
        '''PressureVelocityProduct: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1355.PressureVelocityProduct.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PressureVelocityProduct. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_pressure_viscosity_coefficient(self) -> '_1356.PressureViscosityCoefficient':
        '''PressureViscosityCoefficient: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1356.PressureViscosityCoefficient.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PressureViscosityCoefficient. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_price(self) -> '_1357.Price':
        '''Price: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1357.Price.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Price. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_quadratic_angular_damping(self) -> '_1358.QuadraticAngularDamping':
        '''QuadraticAngularDamping: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1358.QuadraticAngularDamping.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to QuadraticAngularDamping. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_quadratic_drag(self) -> '_1359.QuadraticDrag':
        '''QuadraticDrag: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1359.QuadraticDrag.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to QuadraticDrag. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_rescaled_measurement(self) -> '_1360.RescaledMeasurement':
        '''RescaledMeasurement: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1360.RescaledMeasurement.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to RescaledMeasurement. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_rotatum(self) -> '_1361.Rotatum':
        '''Rotatum: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1361.Rotatum.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Rotatum. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_safety_factor(self) -> '_1362.SafetyFactor':
        '''SafetyFactor: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1362.SafetyFactor.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SafetyFactor. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_specific_acoustic_impedance(self) -> '_1363.SpecificAcousticImpedance':
        '''SpecificAcousticImpedance: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1363.SpecificAcousticImpedance.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpecificAcousticImpedance. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_specific_heat(self) -> '_1364.SpecificHeat':
        '''SpecificHeat: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1364.SpecificHeat.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpecificHeat. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_square_root_of_unit_force_per_unit_area(self) -> '_1365.SquareRootOfUnitForcePerUnitArea':
        '''SquareRootOfUnitForcePerUnitArea: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1365.SquareRootOfUnitForcePerUnitArea.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SquareRootOfUnitForcePerUnitArea. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_stiffness_per_unit_face_width(self) -> '_1366.StiffnessPerUnitFaceWidth':
        '''StiffnessPerUnitFaceWidth: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1366.StiffnessPerUnitFaceWidth.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StiffnessPerUnitFaceWidth. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_stress(self) -> '_1367.Stress':
        '''Stress: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1367.Stress.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Stress. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_temperature(self) -> '_1368.Temperature':
        '''Temperature: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1368.Temperature.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Temperature. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_temperature_difference(self) -> '_1369.TemperatureDifference':
        '''TemperatureDifference: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1369.TemperatureDifference.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TemperatureDifference. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_temperature_per_unit_time(self) -> '_1370.TemperaturePerUnitTime':
        '''TemperaturePerUnitTime: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1370.TemperaturePerUnitTime.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TemperaturePerUnitTime. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_text(self) -> '_1371.Text':
        '''Text: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1371.Text.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Text. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_thermal_contact_coefficient(self) -> '_1372.ThermalContactCoefficient':
        '''ThermalContactCoefficient: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1372.ThermalContactCoefficient.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ThermalContactCoefficient. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_thermal_expansion_coefficient(self) -> '_1373.ThermalExpansionCoefficient':
        '''ThermalExpansionCoefficient: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1373.ThermalExpansionCoefficient.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ThermalExpansionCoefficient. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_thermo_elastic_factor(self) -> '_1374.ThermoElasticFactor':
        '''ThermoElasticFactor: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1374.ThermoElasticFactor.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ThermoElasticFactor. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_time(self) -> '_1375.Time':
        '''Time: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1375.Time.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Time. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_time_short(self) -> '_1376.TimeShort':
        '''TimeShort: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1376.TimeShort.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TimeShort. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_time_very_short(self) -> '_1377.TimeVeryShort':
        '''TimeVeryShort: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1377.TimeVeryShort.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TimeVeryShort. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_torque(self) -> '_1378.Torque':
        '''Torque: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1378.Torque.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Torque. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_torque_converter_inverse_k(self) -> '_1379.TorqueConverterInverseK':
        '''TorqueConverterInverseK: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1379.TorqueConverterInverseK.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TorqueConverterInverseK. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_torque_converter_k(self) -> '_1380.TorqueConverterK':
        '''TorqueConverterK: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1380.TorqueConverterK.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TorqueConverterK. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_torque_per_unit_temperature(self) -> '_1381.TorquePerUnitTemperature':
        '''TorquePerUnitTemperature: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1381.TorquePerUnitTemperature.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TorquePerUnitTemperature. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_velocity(self) -> '_1382.Velocity':
        '''Velocity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1382.Velocity.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Velocity. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_velocity_small(self) -> '_1383.VelocitySmall':
        '''VelocitySmall: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1383.VelocitySmall.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to VelocitySmall. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_viscosity(self) -> '_1384.Viscosity':
        '''Viscosity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1384.Viscosity.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Viscosity. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_voltage(self) -> '_1385.Voltage':
        '''Voltage: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1385.Voltage.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Voltage. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_volume(self) -> '_1386.Volume':
        '''Volume: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1386.Volume.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Volume. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_wear_coefficient(self) -> '_1387.WearCoefficient':
        '''WearCoefficient: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1387.WearCoefficient.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to WearCoefficient. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_yank(self) -> '_1388.Yank':
        '''Yank: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1388.Yank.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Yank. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_1274.MeasurementBase]':
        '''List[MeasurementBase]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1274.MeasurementBase))
        return value


class ListWithSelectedItem_ColumnTitle(_1460.ColumnTitle, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ColumnTitle

    A specific implementation of 'ListWithSelectedItem' for 'ColumnTitle' types.
    '''

    __hash__ = None
    __qualname__ = 'ColumnTitle'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ColumnTitle.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_1460.ColumnTitle.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1460.ColumnTitle.TYPE

    @property
    def selected_value(self) -> '_1460.ColumnTitle':
        '''ColumnTitle: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1460.ColumnTitle)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_1460.ColumnTitle]':
        '''List[ColumnTitle]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_1460.ColumnTitle))
        return value


class ListWithSelectedItem_PowerLoad(_2120.PowerLoad, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_PowerLoad

    A specific implementation of 'ListWithSelectedItem' for 'PowerLoad' types.
    '''

    __hash__ = None
    __qualname__ = 'PowerLoad'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_PowerLoad.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2120.PowerLoad.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2120.PowerLoad.TYPE

    @property
    def selected_value(self) -> '_2120.PowerLoad':
        '''PowerLoad: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2120.PowerLoad)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_2120.PowerLoad]':
        '''List[PowerLoad]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2120.PowerLoad))
        return value


class ListWithSelectedItem_GearSet(_2178.GearSet, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_GearSet

    A specific implementation of 'ListWithSelectedItem' for 'GearSet' types.
    '''

    __hash__ = None
    __qualname__ = 'GearSet'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_GearSet.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2178.GearSet.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2178.GearSet.TYPE

    @property
    def selected_value(self) -> '_2178.GearSet':
        '''GearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2178.GearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_agma_gleason_conical_gear_set(self) -> '_2160.AGMAGleasonConicalGearSet':
        '''AGMAGleasonConicalGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2160.AGMAGleasonConicalGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AGMAGleasonConicalGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_bevel_differential_gear_set(self) -> '_2162.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2162.BevelDifferentialGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelDifferentialGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_bevel_gear_set(self) -> '_2166.BevelGearSet':
        '''BevelGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2166.BevelGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_concept_gear_set(self) -> '_2168.ConceptGearSet':
        '''ConceptGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2168.ConceptGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConceptGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_conical_gear_set(self) -> '_2170.ConicalGearSet':
        '''ConicalGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2170.ConicalGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConicalGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_cylindrical_gear_set(self) -> '_2172.CylindricalGearSet':
        '''CylindricalGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2172.CylindricalGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_face_gear_set(self) -> '_2175.FaceGearSet':
        '''FaceGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2175.FaceGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FaceGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_hypoid_gear_set(self) -> '_2181.HypoidGearSet':
        '''HypoidGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2181.HypoidGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HypoidGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self) -> '_2183.KlingelnbergCycloPalloidConicalGearSet':
        '''KlingelnbergCycloPalloidConicalGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2183.KlingelnbergCycloPalloidConicalGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidConicalGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> '_2185.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2185.KlingelnbergCycloPalloidHypoidGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidHypoidGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> '_2187.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2187.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidSpiralBevelGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_planetary_gear_set(self) -> '_2188.PlanetaryGearSet':
        '''PlanetaryGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2188.PlanetaryGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PlanetaryGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_spiral_bevel_gear_set(self) -> '_2190.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2190.SpiralBevelGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpiralBevelGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_straight_bevel_diff_gear_set(self) -> '_2192.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2192.StraightBevelDiffGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelDiffGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_straight_bevel_gear_set(self) -> '_2194.StraightBevelGearSet':
        '''StraightBevelGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2194.StraightBevelGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_worm_gear_set(self) -> '_2198.WormGearSet':
        '''WormGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2198.WormGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to WormGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_zerol_bevel_gear_set(self) -> '_2200.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2200.ZerolBevelGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ZerolBevelGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_2178.GearSet]':
        '''List[GearSet]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2178.GearSet))
        return value


class ListWithSelectedItem_FESubstructureNode(_2036.FESubstructureNode, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_FESubstructureNode

    A specific implementation of 'ListWithSelectedItem' for 'FESubstructureNode' types.
    '''

    __hash__ = None
    __qualname__ = 'FESubstructureNode'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_FESubstructureNode.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2036.FESubstructureNode.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2036.FESubstructureNode.TYPE

    @property
    def selected_value(self) -> '_2036.FESubstructureNode':
        '''FESubstructureNode: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2036.FESubstructureNode)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_2036.FESubstructureNode]':
        '''List[FESubstructureNode]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2036.FESubstructureNode))
        return value


class ListWithSelectedItem_Datum(_2097.Datum, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_Datum

    A specific implementation of 'ListWithSelectedItem' for 'Datum' types.
    '''

    __hash__ = None
    __qualname__ = 'Datum'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_Datum.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2097.Datum.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2097.Datum.TYPE

    @property
    def selected_value(self) -> '_2097.Datum':
        '''Datum: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2097.Datum)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_2097.Datum]':
        '''List[Datum]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2097.Datum))
        return value


class ListWithSelectedItem_Component(_2093.Component, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_Component

    A specific implementation of 'ListWithSelectedItem' for 'Component' types.
    '''

    __hash__ = None
    __qualname__ = 'Component'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_Component.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2093.Component.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2093.Component.TYPE

    @property
    def selected_value(self) -> '_2093.Component':
        '''Component: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2093.Component.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Component. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_abstract_shaft(self) -> '_2085.AbstractShaft':
        '''AbstractShaft: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2085.AbstractShaft.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AbstractShaft. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_abstract_shaft_or_housing(self) -> '_2086.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2086.AbstractShaftOrHousing.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AbstractShaftOrHousing. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_bearing(self) -> '_2089.Bearing':
        '''Bearing: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2089.Bearing.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Bearing. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_bolt(self) -> '_2091.Bolt':
        '''Bolt: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2091.Bolt.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Bolt. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_connector(self) -> '_2096.Connector':
        '''Connector: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2096.Connector.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Connector. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_datum(self) -> '_2097.Datum':
        '''Datum: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2097.Datum.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Datum. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_external_cad_model(self) -> '_2100.ExternalCADModel':
        '''ExternalCADModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2100.ExternalCADModel.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ExternalCADModel. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_fe_part(self) -> '_2101.FEPart':
        '''FEPart: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2101.FEPart.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FEPart. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_guide_dxf_model(self) -> '_2103.GuideDxfModel':
        '''GuideDxfModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2103.GuideDxfModel.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GuideDxfModel. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_mass_disc(self) -> '_2110.MassDisc':
        '''MassDisc: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2110.MassDisc.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MassDisc. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_measurement_component(self) -> '_2111.MeasurementComponent':
        '''MeasurementComponent: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2111.MeasurementComponent.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MeasurementComponent. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_mountable_component(self) -> '_2112.MountableComponent':
        '''MountableComponent: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2112.MountableComponent.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MountableComponent. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_oil_seal(self) -> '_2114.OilSeal':
        '''OilSeal: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2114.OilSeal.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to OilSeal. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_planet_carrier(self) -> '_2117.PlanetCarrier':
        '''PlanetCarrier: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2117.PlanetCarrier.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PlanetCarrier. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_point_load(self) -> '_2119.PointLoad':
        '''PointLoad: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2119.PointLoad.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PointLoad. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_power_load(self) -> '_2120.PowerLoad':
        '''PowerLoad: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2120.PowerLoad.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PowerLoad. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_unbalanced_mass(self) -> '_2125.UnbalancedMass':
        '''UnbalancedMass: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2125.UnbalancedMass.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to UnbalancedMass. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_virtual_component(self) -> '_2126.VirtualComponent':
        '''VirtualComponent: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2126.VirtualComponent.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to VirtualComponent. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_shaft(self) -> '_2129.Shaft':
        '''Shaft: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2129.Shaft.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Shaft. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_agma_gleason_conical_gear(self) -> '_2159.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2159.AGMAGleasonConicalGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AGMAGleasonConicalGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_bevel_differential_gear(self) -> '_2161.BevelDifferentialGear':
        '''BevelDifferentialGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2161.BevelDifferentialGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelDifferentialGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_bevel_differential_planet_gear(self) -> '_2163.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2163.BevelDifferentialPlanetGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelDifferentialPlanetGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_bevel_differential_sun_gear(self) -> '_2164.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2164.BevelDifferentialSunGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelDifferentialSunGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_bevel_gear(self) -> '_2165.BevelGear':
        '''BevelGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2165.BevelGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_concept_gear(self) -> '_2167.ConceptGear':
        '''ConceptGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2167.ConceptGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConceptGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_conical_gear(self) -> '_2169.ConicalGear':
        '''ConicalGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2169.ConicalGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConicalGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_cylindrical_gear(self) -> '_2171.CylindricalGear':
        '''CylindricalGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2171.CylindricalGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_cylindrical_planet_gear(self) -> '_2173.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2173.CylindricalPlanetGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalPlanetGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_face_gear(self) -> '_2174.FaceGear':
        '''FaceGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2174.FaceGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FaceGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_gear(self) -> '_2176.Gear':
        '''Gear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2176.Gear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Gear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_hypoid_gear(self) -> '_2180.HypoidGear':
        '''HypoidGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2180.HypoidGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HypoidGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2182.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2182.KlingelnbergCycloPalloidConicalGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2184.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2184.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2186.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2186.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_spiral_bevel_gear(self) -> '_2189.SpiralBevelGear':
        '''SpiralBevelGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2189.SpiralBevelGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpiralBevelGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_straight_bevel_diff_gear(self) -> '_2191.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2191.StraightBevelDiffGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelDiffGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_straight_bevel_gear(self) -> '_2193.StraightBevelGear':
        '''StraightBevelGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2193.StraightBevelGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_straight_bevel_planet_gear(self) -> '_2195.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2195.StraightBevelPlanetGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelPlanetGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_straight_bevel_sun_gear(self) -> '_2196.StraightBevelSunGear':
        '''StraightBevelSunGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2196.StraightBevelSunGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelSunGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_worm_gear(self) -> '_2197.WormGear':
        '''WormGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2197.WormGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to WormGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_zerol_bevel_gear(self) -> '_2199.ZerolBevelGear':
        '''ZerolBevelGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2199.ZerolBevelGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ZerolBevelGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_cycloidal_disc(self) -> '_2215.CycloidalDisc':
        '''CycloidalDisc: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2215.CycloidalDisc.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CycloidalDisc. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_ring_pins(self) -> '_2216.RingPins':
        '''RingPins: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2216.RingPins.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to RingPins. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_clutch_half(self) -> '_2225.ClutchHalf':
        '''ClutchHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2225.ClutchHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ClutchHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_concept_coupling_half(self) -> '_2228.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2228.ConceptCouplingHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConceptCouplingHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_coupling_half(self) -> '_2230.CouplingHalf':
        '''CouplingHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2230.CouplingHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CouplingHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_cvt_pulley(self) -> '_2233.CVTPulley':
        '''CVTPulley: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2233.CVTPulley.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CVTPulley. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_part_to_part_shear_coupling_half(self) -> '_2235.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2235.PartToPartShearCouplingHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PartToPartShearCouplingHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_pulley(self) -> '_2236.Pulley':
        '''Pulley: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2236.Pulley.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to Pulley. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_rolling_ring(self) -> '_2242.RollingRing':
        '''RollingRing: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2242.RollingRing.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to RollingRing. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_shaft_hub_connection(self) -> '_2244.ShaftHubConnection':
        '''ShaftHubConnection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2244.ShaftHubConnection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ShaftHubConnection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_spring_damper_half(self) -> '_2246.SpringDamperHalf':
        '''SpringDamperHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2246.SpringDamperHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpringDamperHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_synchroniser_half(self) -> '_2249.SynchroniserHalf':
        '''SynchroniserHalf: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2249.SynchroniserHalf.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SynchroniserHalf. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_synchroniser_part(self) -> '_2250.SynchroniserPart':
        '''SynchroniserPart: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2250.SynchroniserPart.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SynchroniserPart. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_synchroniser_sleeve(self) -> '_2251.SynchroniserSleeve':
        '''SynchroniserSleeve: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2251.SynchroniserSleeve.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SynchroniserSleeve. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_torque_converter_pump(self) -> '_2253.TorqueConverterPump':
        '''TorqueConverterPump: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2253.TorqueConverterPump.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TorqueConverterPump. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_torque_converter_turbine(self) -> '_2255.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2255.TorqueConverterTurbine.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to TorqueConverterTurbine. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_2093.Component]':
        '''List[Component]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2093.Component))
        return value


class ListWithSelectedItem_FELink(_2067.FELink, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_FELink

    A specific implementation of 'ListWithSelectedItem' for 'FELink' types.
    '''

    __hash__ = None
    __qualname__ = 'FELink'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_FELink.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2067.FELink.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2067.FELink.TYPE

    @property
    def selected_value(self) -> '_2067.FELink':
        '''FELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2067.FELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_electric_machine_stator_fe_link(self) -> '_2068.ElectricMachineStatorFELink':
        '''ElectricMachineStatorFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2068.ElectricMachineStatorFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ElectricMachineStatorFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_gear_mesh_fe_link(self) -> '_2070.GearMeshFELink':
        '''GearMeshFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2070.GearMeshFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GearMeshFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_gear_with_duplicated_meshes_fe_link(self) -> '_2071.GearWithDuplicatedMeshesFELink':
        '''GearWithDuplicatedMeshesFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2071.GearWithDuplicatedMeshesFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GearWithDuplicatedMeshesFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_multi_angle_connection_fe_link(self) -> '_2072.MultiAngleConnectionFELink':
        '''MultiAngleConnectionFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2072.MultiAngleConnectionFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MultiAngleConnectionFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_multi_node_connector_fe_link(self) -> '_2073.MultiNodeConnectorFELink':
        '''MultiNodeConnectorFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2073.MultiNodeConnectorFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MultiNodeConnectorFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_multi_node_fe_link(self) -> '_2074.MultiNodeFELink':
        '''MultiNodeFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2074.MultiNodeFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to MultiNodeFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_planetary_connector_multi_node_fe_link(self) -> '_2075.PlanetaryConnectorMultiNodeFELink':
        '''PlanetaryConnectorMultiNodeFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2075.PlanetaryConnectorMultiNodeFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PlanetaryConnectorMultiNodeFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_planet_based_fe_link(self) -> '_2076.PlanetBasedFELink':
        '''PlanetBasedFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2076.PlanetBasedFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PlanetBasedFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_planet_carrier_fe_link(self) -> '_2077.PlanetCarrierFELink':
        '''PlanetCarrierFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2077.PlanetCarrierFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PlanetCarrierFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_point_load_fe_link(self) -> '_2078.PointLoadFELink':
        '''PointLoadFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2078.PointLoadFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to PointLoadFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_rolling_ring_connection_fe_link(self) -> '_2079.RollingRingConnectionFELink':
        '''RollingRingConnectionFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2079.RollingRingConnectionFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to RollingRingConnectionFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_shaft_hub_connection_fe_link(self) -> '_2080.ShaftHubConnectionFELink':
        '''ShaftHubConnectionFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2080.ShaftHubConnectionFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ShaftHubConnectionFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_single_node_fe_link(self) -> '_2081.SingleNodeFELink':
        '''SingleNodeFELink: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2081.SingleNodeFELink.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SingleNodeFELink. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_2067.FELink]':
        '''List[FELink]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2067.FELink))
        return value


class ListWithSelectedItem_FESubstructure(_2034.FESubstructure, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_FESubstructure

    A specific implementation of 'ListWithSelectedItem' for 'FESubstructure' types.
    '''

    __hash__ = None
    __qualname__ = 'FESubstructure'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_FESubstructure.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2034.FESubstructure.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2034.FESubstructure.TYPE

    @property
    def selected_value(self) -> '_2034.FESubstructure':
        '''FESubstructure: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2034.FESubstructure)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_2034.FESubstructure]':
        '''List[FESubstructure]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2034.FESubstructure))
        return value


class ListWithSelectedItem_CylindricalGear(_2171.CylindricalGear, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_CylindricalGear

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalGear' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalGear'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_CylindricalGear.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2171.CylindricalGear.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2171.CylindricalGear.TYPE

    @property
    def selected_value(self) -> '_2171.CylindricalGear':
        '''CylindricalGear: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2171.CylindricalGear.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGear. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_2171.CylindricalGear]':
        '''List[CylindricalGear]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2171.CylindricalGear))
        return value


class ListWithSelectedItem_GuideDxfModel(_2103.GuideDxfModel, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_GuideDxfModel

    A specific implementation of 'ListWithSelectedItem' for 'GuideDxfModel' types.
    '''

    __hash__ = None
    __qualname__ = 'GuideDxfModel'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_GuideDxfModel.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2103.GuideDxfModel.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2103.GuideDxfModel.TYPE

    @property
    def selected_value(self) -> '_2103.GuideDxfModel':
        '''GuideDxfModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2103.GuideDxfModel)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_2103.GuideDxfModel]':
        '''List[GuideDxfModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2103.GuideDxfModel))
        return value


class ListWithSelectedItem_ConcentricPartGroup(_2134.ConcentricPartGroup, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ConcentricPartGroup

    A specific implementation of 'ListWithSelectedItem' for 'ConcentricPartGroup' types.
    '''

    __hash__ = None
    __qualname__ = 'ConcentricPartGroup'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ConcentricPartGroup.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2134.ConcentricPartGroup.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2134.ConcentricPartGroup.TYPE

    @property
    def selected_value(self) -> '_2134.ConcentricPartGroup':
        '''ConcentricPartGroup: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2134.ConcentricPartGroup)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_2134.ConcentricPartGroup]':
        '''List[ConcentricPartGroup]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2134.ConcentricPartGroup))
        return value


class ListWithSelectedItem_CylindricalGearSet(_2172.CylindricalGearSet, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_CylindricalGearSet

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalGearSet' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalGearSet'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_CylindricalGearSet.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2172.CylindricalGearSet.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2172.CylindricalGearSet.TYPE

    @property
    def selected_value(self) -> '_2172.CylindricalGearSet':
        '''CylindricalGearSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2172.CylindricalGearSet.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearSet. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_2172.CylindricalGearSet]':
        '''List[CylindricalGearSet]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2172.CylindricalGearSet))
        return value


class ListWithSelectedItem_GearSetDesign(_879.GearSetDesign, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_GearSetDesign

    A specific implementation of 'ListWithSelectedItem' for 'GearSetDesign' types.
    '''

    __hash__ = None
    __qualname__ = 'GearSetDesign'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_GearSetDesign.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_879.GearSetDesign.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _879.GearSetDesign.TYPE

    @property
    def selected_value(self) -> '_879.GearSetDesign':
        '''GearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _879.GearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to GearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_zerol_bevel_gear_set_design(self) -> '_883.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _883.ZerolBevelGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ZerolBevelGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_worm_gear_set_design(self) -> '_888.WormGearSetDesign':
        '''WormGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _888.WormGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to WormGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_straight_bevel_diff_gear_set_design(self) -> '_892.StraightBevelDiffGearSetDesign':
        '''StraightBevelDiffGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _892.StraightBevelDiffGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelDiffGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_straight_bevel_gear_set_design(self) -> '_896.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _896.StraightBevelGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StraightBevelGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_spiral_bevel_gear_set_design(self) -> '_900.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _900.SpiralBevelGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to SpiralBevelGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(self) -> '_904.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _904.KlingelnbergCycloPalloidSpiralBevelGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidSpiralBevelGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_design(self) -> '_908.KlingelnbergCycloPalloidHypoidGearSetDesign':
        '''KlingelnbergCycloPalloidHypoidGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _908.KlingelnbergCycloPalloidHypoidGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergCycloPalloidHypoidGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_klingelnberg_conical_gear_set_design(self) -> '_912.KlingelnbergConicalGearSetDesign':
        '''KlingelnbergConicalGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _912.KlingelnbergConicalGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to KlingelnbergConicalGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_hypoid_gear_set_design(self) -> '_916.HypoidGearSetDesign':
        '''HypoidGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _916.HypoidGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to HypoidGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_face_gear_set_design(self) -> '_924.FaceGearSetDesign':
        '''FaceGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _924.FaceGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to FaceGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_cylindrical_gear_set_design(self) -> '_955.CylindricalGearSetDesign':
        '''CylindricalGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _955.CylindricalGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_cylindrical_planetary_gear_set_design(self) -> '_966.CylindricalPlanetaryGearSetDesign':
        '''CylindricalPlanetaryGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _966.CylindricalPlanetaryGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalPlanetaryGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_conical_gear_set_design(self) -> '_1066.ConicalGearSetDesign':
        '''ConicalGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1066.ConicalGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConicalGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_concept_gear_set_design(self) -> '_1088.ConceptGearSetDesign':
        '''ConceptGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1088.ConceptGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to ConceptGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_bevel_gear_set_design(self) -> '_1092.BevelGearSetDesign':
        '''BevelGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1092.BevelGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to BevelGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_agma_gleason_conical_gear_set_design(self) -> '_1105.AGMAGleasonConicalGearSetDesign':
        '''AGMAGleasonConicalGearSetDesign: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1105.AGMAGleasonConicalGearSetDesign.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to AGMAGleasonConicalGearSetDesign. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_879.GearSetDesign]':
        '''List[GearSetDesign]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_879.GearSetDesign))
        return value


class ListWithSelectedItem_ShaftHubConnection(_2244.ShaftHubConnection, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ShaftHubConnection

    A specific implementation of 'ListWithSelectedItem' for 'ShaftHubConnection' types.
    '''

    __hash__ = None
    __qualname__ = 'ShaftHubConnection'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ShaftHubConnection.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2244.ShaftHubConnection.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2244.ShaftHubConnection.TYPE

    @property
    def selected_value(self) -> '_2244.ShaftHubConnection':
        '''ShaftHubConnection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2244.ShaftHubConnection)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_2244.ShaftHubConnection]':
        '''List[ShaftHubConnection]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2244.ShaftHubConnection))
        return value


class ListWithSelectedItem_TSelectableItem(Generic[TSelectableItem], mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_TSelectableItem

    A specific implementation of 'ListWithSelectedItem' for 'TSelectableItem' types.
    '''

    __hash__ = None
    __qualname__ = 'TSelectableItem'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_TSelectableItem.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.SelectedValue
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> 'TSelectableItem':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return TSelectableItem

    @property
    def selected_value(self) -> 'TSelectableItem':
        '''TSelectableItem: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(TSelectableItem)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[TSelectableItem]':
        '''List[TSelectableItem]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(TSelectableItem))
        return value


class ListWithSelectedItem_CylindricalGearSystemDeflection(_2380.CylindricalGearSystemDeflection, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_CylindricalGearSystemDeflection

    A specific implementation of 'ListWithSelectedItem' for 'CylindricalGearSystemDeflection' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalGearSystemDeflection'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_CylindricalGearSystemDeflection.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2380.CylindricalGearSystemDeflection.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2380.CylindricalGearSystemDeflection.TYPE

    @property
    def selected_value(self) -> '_2380.CylindricalGearSystemDeflection':
        '''CylindricalGearSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2380.CylindricalGearSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_cylindrical_gear_system_deflection_timestep(self) -> '_2381.CylindricalGearSystemDeflectionTimestep':
        '''CylindricalGearSystemDeflectionTimestep: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2381.CylindricalGearSystemDeflectionTimestep.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearSystemDeflectionTimestep. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_cylindrical_gear_system_deflection_with_ltca_results(self) -> '_2382.CylindricalGearSystemDeflectionWithLTCAResults':
        '''CylindricalGearSystemDeflectionWithLTCAResults: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2382.CylindricalGearSystemDeflectionWithLTCAResults.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalGearSystemDeflectionWithLTCAResults. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def selected_value_of_type_cylindrical_planet_gear_system_deflection(self) -> '_2383.CylindricalPlanetGearSystemDeflection':
        '''CylindricalPlanetGearSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2383.CylindricalPlanetGearSystemDeflection.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to CylindricalPlanetGearSystemDeflection. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_2380.CylindricalGearSystemDeflection]':
        '''List[CylindricalGearSystemDeflection]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2380.CylindricalGearSystemDeflection))
        return value


class ListWithSelectedItem_DesignState(_5286.DesignState, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_DesignState

    A specific implementation of 'ListWithSelectedItem' for 'DesignState' types.
    '''

    __hash__ = None
    __qualname__ = 'DesignState'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_DesignState.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_5286.DesignState.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5286.DesignState.TYPE

    @property
    def selected_value(self) -> '_5286.DesignState':
        '''DesignState: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5286.DesignState)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_5286.DesignState]':
        '''List[DesignState]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_5286.DesignState))
        return value


class ListWithSelectedItem_FEPart(_2101.FEPart, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_FEPart

    A specific implementation of 'ListWithSelectedItem' for 'FEPart' types.
    '''

    __hash__ = None
    __qualname__ = 'FEPart'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_FEPart.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2101.FEPart.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2101.FEPart.TYPE

    @property
    def selected_value(self) -> '_2101.FEPart':
        '''FEPart: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2101.FEPart)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_2101.FEPart]':
        '''List[FEPart]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2101.FEPart))
        return value


class ListWithSelectedItem_ResultLocationSelectionGroup(_5725.ResultLocationSelectionGroup, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ResultLocationSelectionGroup

    A specific implementation of 'ListWithSelectedItem' for 'ResultLocationSelectionGroup' types.
    '''

    __hash__ = None
    __qualname__ = 'ResultLocationSelectionGroup'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ResultLocationSelectionGroup.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_5725.ResultLocationSelectionGroup.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5725.ResultLocationSelectionGroup.TYPE

    @property
    def selected_value(self) -> '_5725.ResultLocationSelectionGroup':
        '''ResultLocationSelectionGroup: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5725.ResultLocationSelectionGroup)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_5725.ResultLocationSelectionGroup]':
        '''List[ResultLocationSelectionGroup]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_5725.ResultLocationSelectionGroup))
        return value


class ListWithSelectedItem_StaticLoadCase(_6556.StaticLoadCase, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_StaticLoadCase

    A specific implementation of 'ListWithSelectedItem' for 'StaticLoadCase' types.
    '''

    __hash__ = None
    __qualname__ = 'StaticLoadCase'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_StaticLoadCase.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_6556.StaticLoadCase.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6556.StaticLoadCase.TYPE

    @property
    def selected_value(self) -> '_6556.StaticLoadCase':
        '''StaticLoadCase: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6556.StaticLoadCase.TYPE not in self.enclosing.SelectedValue.__class__.__mro__:
            raise CastException('Failed to cast selected_value to StaticLoadCase. Expected: {}.'.format(self.enclosing.SelectedValue.__class__.__qualname__))

        return constructor.new_override(self.enclosing.SelectedValue.__class__)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_6556.StaticLoadCase]':
        '''List[StaticLoadCase]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_6556.StaticLoadCase))
        return value


class ListWithSelectedItem_DutyCycle(_5287.DutyCycle, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_DutyCycle

    A specific implementation of 'ListWithSelectedItem' for 'DutyCycle' types.
    '''

    __hash__ = None
    __qualname__ = 'DutyCycle'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_DutyCycle.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_5287.DutyCycle.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5287.DutyCycle.TYPE

    @property
    def selected_value(self) -> '_5287.DutyCycle':
        '''DutyCycle: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5287.DutyCycle)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_5287.DutyCycle]':
        '''List[DutyCycle]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_5287.DutyCycle))
        return value


class ListWithSelectedItem_float(float, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_float

    A specific implementation of 'ListWithSelectedItem' for 'float' types.
    '''

    __hash__ = None
    __qualname__ = 'float'

    def __new__(cls, instance_to_wrap: 'ListWithSelectedItem_float.TYPE'):
        return float.__new__(cls, instance_to_wrap.SelectedValue) if instance_to_wrap.SelectedValue else 0.0

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_float.TYPE'):
        try:
            self.enclosing = instance_to_wrap
            self.wrapped = instance_to_wrap.SelectedValue
        except (TypeError, AttributeError):
            pass

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> 'float':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return float

    @property
    def selected_value(self) -> 'float':
        '''float: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.enclosing.SelectedValue

    @property
    def available_values(self) -> 'List[float]':
        '''List[float]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_list_float(self.enclosing.AvailableValues)
        return value


class ListWithSelectedItem_ElectricMachineDataSet(_2025.ElectricMachineDataSet, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_ElectricMachineDataSet

    A specific implementation of 'ListWithSelectedItem' for 'ElectricMachineDataSet' types.
    '''

    __hash__ = None
    __qualname__ = 'ElectricMachineDataSet'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_ElectricMachineDataSet.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2025.ElectricMachineDataSet.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2025.ElectricMachineDataSet.TYPE

    @property
    def selected_value(self) -> '_2025.ElectricMachineDataSet':
        '''ElectricMachineDataSet: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2025.ElectricMachineDataSet)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_2025.ElectricMachineDataSet]':
        '''List[ElectricMachineDataSet]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2025.ElectricMachineDataSet))
        return value


class ListWithSelectedItem_PointLoad(_2119.PointLoad, mixins.ListWithSelectedItemMixin):
    '''ListWithSelectedItem_PointLoad

    A specific implementation of 'ListWithSelectedItem' for 'PointLoad' types.
    '''

    __hash__ = None
    __qualname__ = 'PointLoad'

    def __init__(self, instance_to_wrap: 'ListWithSelectedItem_PointLoad.TYPE'):
        try:
            self.enclosing = instance_to_wrap
        except (TypeError, AttributeError):
            pass
        super().__init__(instance_to_wrap.SelectedValue)

    @classmethod
    def wrapper_type(cls) -> '_LIST_WITH_SELECTED_ITEM':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls) -> '_2119.PointLoad.TYPE':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2119.PointLoad.TYPE

    @property
    def selected_value(self) -> '_2119.PointLoad':
        '''PointLoad: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2119.PointLoad)(self.enclosing.SelectedValue) if self.enclosing.SelectedValue else None

    @property
    def available_values(self) -> 'List[_2119.PointLoad]':
        '''List[PointLoad]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.enclosing.AvailableValues, constructor.new(_2119.PointLoad))
        return value
