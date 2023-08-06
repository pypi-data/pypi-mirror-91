﻿'''_3497.py

TorqueConverterConnectionCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _1944
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3375
from mastapy.system_model.analyses_and_results.power_flows.compound import _3423
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'TorqueConverterConnectionCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnectionCompoundPowerFlow',)


class TorqueConverterConnectionCompoundPowerFlow(_3423.CouplingConnectionCompoundPowerFlow):
    '''TorqueConverterConnectionCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_CONNECTION_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterConnectionCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1944.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1944.TorqueConverterConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1944.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1944.TorqueConverterConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3375.TorqueConverterConnectionPowerFlow]':
        '''List[TorqueConverterConnectionPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3375.TorqueConverterConnectionPowerFlow))
        return value

    @property
    def connection_power_flow_load_cases(self) -> 'List[_3375.TorqueConverterConnectionPowerFlow]':
        '''List[TorqueConverterConnectionPowerFlow]: 'ConnectionPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionPowerFlowLoadCases, constructor.new(_3375.TorqueConverterConnectionPowerFlow))
        return value
