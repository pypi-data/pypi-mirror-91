﻿'''_5498.py

CVTSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2163
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5466
from mastapy._internal.python_net import python_net_import

_CVT_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'CVTSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTSingleMeshWhineAnalysis',)


class CVTSingleMeshWhineAnalysis(_5466.BeltDriveSingleMeshWhineAnalysis):
    '''CVTSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2163.CVT':
        '''CVT: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2163.CVT)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
