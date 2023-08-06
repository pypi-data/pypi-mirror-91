﻿'''_3280.py

BoltPowerFlow
'''


from mastapy.system_model.part_model import _2028
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6116
from mastapy.system_model.analyses_and_results.power_flows import _3285
from mastapy._internal.python_net import python_net_import

_BOLT_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'BoltPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltPowerFlow',)


class BoltPowerFlow(_3285.ComponentPowerFlow):
    '''BoltPowerFlow

    This is a mastapy class.
    '''

    TYPE = _BOLT_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2028.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2028.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6116.BoltLoadCase':
        '''BoltLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6116.BoltLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
