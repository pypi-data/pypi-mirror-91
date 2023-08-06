﻿'''_3529.py

ClutchParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2156
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6119
from mastapy.system_model.analyses_and_results.system_deflections import _2272
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3545
from mastapy._internal.python_net import python_net_import

_CLUTCH_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'ClutchParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchParametricStudyTool',)


class ClutchParametricStudyTool(_3545.CouplingParametricStudyTool):
    '''ClutchParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2156.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2156.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6119.ClutchLoadCase':
        '''ClutchLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6119.ClutchLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def assembly_system_deflection_results(self) -> 'List[_2272.ClutchSystemDeflection]':
        '''List[ClutchSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2272.ClutchSystemDeflection))
        return value
