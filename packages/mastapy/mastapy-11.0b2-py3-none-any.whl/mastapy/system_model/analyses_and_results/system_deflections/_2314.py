﻿'''_2314.py

GuideDxfModelSystemDeflection
'''


from mastapy.system_model.part_model import _2039
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6174
from mastapy.system_model.analyses_and_results.power_flows import _3317
from mastapy.system_model.analyses_and_results.system_deflections import _2274
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'GuideDxfModelSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelSystemDeflection',)


class GuideDxfModelSystemDeflection(_2274.ComponentSystemDeflection):
    '''GuideDxfModelSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2039.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2039.GuideDxfModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6174.GuideDxfModelLoadCase':
        '''GuideDxfModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6174.GuideDxfModelLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3317.GuideDxfModelPowerFlow':
        '''GuideDxfModelPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3317.GuideDxfModelPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
