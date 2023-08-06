'''_5886.py

AssemblyDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2083, _2122
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6417, _6544
from mastapy.system_model.analyses_and_results.dynamic_analyses import (
    _5887, _5889, _5892, _5898,
    _5899, _5901, _5906, _5910,
    _5920, _5922, _5924, _5928,
    _5935, _5936, _5937, _5944,
    _5951, _5954, _5955, _5956,
    _5958, _5961, _5965, _5966,
    _5967, _5976, _5969, _5971,
    _5975, _5981, _5983, _5987,
    _5990, _5993, _5998, _6001,
    _6005, _6008, _5879
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'AssemblyDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyDynamicAnalysis',)


class AssemblyDynamicAnalysis(_5879.AbstractAssemblyDynamicAnalysis):
    '''AssemblyDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2083.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2083.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6417.AssemblyLoadCase':
        '''AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6417.AssemblyLoadCase.TYPE not in self.wrapped.AssemblyLoadCase.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to AssemblyLoadCase. Expected: {}.'.format(self.wrapped.AssemblyLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyLoadCase.__class__)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def bearings(self) -> 'List[_5887.BearingDynamicAnalysis]':
        '''List[BearingDynamicAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5887.BearingDynamicAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_5889.BeltDriveDynamicAnalysis]':
        '''List[BeltDriveDynamicAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5889.BeltDriveDynamicAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5892.BevelDifferentialGearSetDynamicAnalysis]':
        '''List[BevelDifferentialGearSetDynamicAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5892.BevelDifferentialGearSetDynamicAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_5898.BoltDynamicAnalysis]':
        '''List[BoltDynamicAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5898.BoltDynamicAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_5899.BoltedJointDynamicAnalysis]':
        '''List[BoltedJointDynamicAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5899.BoltedJointDynamicAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_5901.ClutchDynamicAnalysis]':
        '''List[ClutchDynamicAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5901.ClutchDynamicAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_5906.ConceptCouplingDynamicAnalysis]':
        '''List[ConceptCouplingDynamicAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5906.ConceptCouplingDynamicAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5910.ConceptGearSetDynamicAnalysis]':
        '''List[ConceptGearSetDynamicAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5910.ConceptGearSetDynamicAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_5920.CVTDynamicAnalysis]':
        '''List[CVTDynamicAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5920.CVTDynamicAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_5922.CycloidalAssemblyDynamicAnalysis]':
        '''List[CycloidalAssemblyDynamicAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_5922.CycloidalAssemblyDynamicAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_5924.CycloidalDiscDynamicAnalysis]':
        '''List[CycloidalDiscDynamicAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_5924.CycloidalDiscDynamicAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5928.CylindricalGearSetDynamicAnalysis]':
        '''List[CylindricalGearSetDynamicAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5928.CylindricalGearSetDynamicAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5935.FaceGearSetDynamicAnalysis]':
        '''List[FaceGearSetDynamicAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5935.FaceGearSetDynamicAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_5936.FEPartDynamicAnalysis]':
        '''List[FEPartDynamicAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_5936.FEPartDynamicAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5937.FlexiblePinAssemblyDynamicAnalysis]':
        '''List[FlexiblePinAssemblyDynamicAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5937.FlexiblePinAssemblyDynamicAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5944.HypoidGearSetDynamicAnalysis]':
        '''List[HypoidGearSetDynamicAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5944.HypoidGearSetDynamicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5951.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5951.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5954.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5954.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5955.MassDiscDynamicAnalysis]':
        '''List[MassDiscDynamicAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5955.MassDiscDynamicAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5956.MeasurementComponentDynamicAnalysis]':
        '''List[MeasurementComponentDynamicAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5956.MeasurementComponentDynamicAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5958.OilSealDynamicAnalysis]':
        '''List[OilSealDynamicAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5958.OilSealDynamicAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5961.PartToPartShearCouplingDynamicAnalysis]':
        '''List[PartToPartShearCouplingDynamicAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5961.PartToPartShearCouplingDynamicAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5965.PlanetCarrierDynamicAnalysis]':
        '''List[PlanetCarrierDynamicAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5965.PlanetCarrierDynamicAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5966.PointLoadDynamicAnalysis]':
        '''List[PointLoadDynamicAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5966.PointLoadDynamicAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5967.PowerLoadDynamicAnalysis]':
        '''List[PowerLoadDynamicAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5967.PowerLoadDynamicAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5976.ShaftHubConnectionDynamicAnalysis]':
        '''List[ShaftHubConnectionDynamicAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5976.ShaftHubConnectionDynamicAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_5969.RingPinsDynamicAnalysis]':
        '''List[RingPinsDynamicAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_5969.RingPinsDynamicAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5971.RollingRingAssemblyDynamicAnalysis]':
        '''List[RollingRingAssemblyDynamicAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5971.RollingRingAssemblyDynamicAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_5975.ShaftDynamicAnalysis]':
        '''List[ShaftDynamicAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5975.ShaftDynamicAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5981.SpiralBevelGearSetDynamicAnalysis]':
        '''List[SpiralBevelGearSetDynamicAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5981.SpiralBevelGearSetDynamicAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5983.SpringDamperDynamicAnalysis]':
        '''List[SpringDamperDynamicAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5983.SpringDamperDynamicAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5987.StraightBevelDiffGearSetDynamicAnalysis]':
        '''List[StraightBevelDiffGearSetDynamicAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5987.StraightBevelDiffGearSetDynamicAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5990.StraightBevelGearSetDynamicAnalysis]':
        '''List[StraightBevelGearSetDynamicAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5990.StraightBevelGearSetDynamicAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_5993.SynchroniserDynamicAnalysis]':
        '''List[SynchroniserDynamicAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5993.SynchroniserDynamicAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_5998.TorqueConverterDynamicAnalysis]':
        '''List[TorqueConverterDynamicAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5998.TorqueConverterDynamicAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_6001.UnbalancedMassDynamicAnalysis]':
        '''List[UnbalancedMassDynamicAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_6001.UnbalancedMassDynamicAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_6005.WormGearSetDynamicAnalysis]':
        '''List[WormGearSetDynamicAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_6005.WormGearSetDynamicAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_6008.ZerolBevelGearSetDynamicAnalysis]':
        '''List[ZerolBevelGearSetDynamicAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_6008.ZerolBevelGearSetDynamicAnalysis))
        return value
