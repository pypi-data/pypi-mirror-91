﻿'''_4119.py

StraightBevelPlanetGearModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model.gears import _2131
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4114
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_PLANET_GEAR_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'StraightBevelPlanetGearModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelPlanetGearModalAnalysesAtSpeeds',)


class StraightBevelPlanetGearModalAnalysesAtSpeeds(_4114.StraightBevelDiffGearModalAnalysesAtSpeeds):
    '''StraightBevelPlanetGearModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_PLANET_GEAR_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelPlanetGearModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2131.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2131.StraightBevelPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
