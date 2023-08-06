﻿'''_5616.py

CouplingCompoundSingleMeshWhineAnalysis
'''


from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses.compound import _5671
from mastapy._internal.python_net import python_net_import

_COUPLING_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses.Compound', 'CouplingCompoundSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingCompoundSingleMeshWhineAnalysis',)


class CouplingCompoundSingleMeshWhineAnalysis(_5671.SpecialisedAssemblyCompoundSingleMeshWhineAnalysis):
    '''CouplingCompoundSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _COUPLING_COMPOUND_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingCompoundSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
