﻿'''_5516.py

ImportedFEComponentSingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2042
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6186
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5459
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_COMPONENT_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'ImportedFEComponentSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFEComponentSingleMeshWhineAnalysis',)


class ImportedFEComponentSingleMeshWhineAnalysis(_5459.AbstractShaftOrHousingSingleMeshWhineAnalysis):
    '''ImportedFEComponentSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_COMPONENT_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFEComponentSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2042.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2042.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6186.ImportedFEComponentLoadCase':
        '''ImportedFEComponentLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6186.ImportedFEComponentLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[ImportedFEComponentSingleMeshWhineAnalysis]':
        '''List[ImportedFEComponentSingleMeshWhineAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ImportedFEComponentSingleMeshWhineAnalysis))
        return value
