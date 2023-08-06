﻿'''_2129.py

StraightBevelGear
'''


from mastapy.gears.gear_designs.straight_bevel import _731
from mastapy._internal import constructor
from mastapy.system_model.part_model.gears import _2101
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelGear')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGear',)


class StraightBevelGear(_2101.BevelGear):
    '''StraightBevelGear

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGear.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bevel_gear_design(self) -> '_731.StraightBevelGearDesign':
        '''StraightBevelGearDesign: 'BevelGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_731.StraightBevelGearDesign)(self.wrapped.BevelGearDesign) if self.wrapped.BevelGearDesign else None

    @property
    def straight_bevel_gear_design(self) -> '_731.StraightBevelGearDesign':
        '''StraightBevelGearDesign: 'StraightBevelGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_731.StraightBevelGearDesign)(self.wrapped.StraightBevelGearDesign) if self.wrapped.StraightBevelGearDesign else None
