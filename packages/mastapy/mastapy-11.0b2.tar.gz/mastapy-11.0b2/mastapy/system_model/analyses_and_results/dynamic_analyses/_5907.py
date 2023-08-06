'''_5907.py

ConceptCouplingHalfDynamicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2228
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6437
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5918
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_HALF_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'ConceptCouplingHalfDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingHalfDynamicAnalysis',)


class ConceptCouplingHalfDynamicAnalysis(_5918.CouplingHalfDynamicAnalysis):
    '''ConceptCouplingHalfDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_HALF_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingHalfDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2228.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2228.ConceptCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6437.ConceptCouplingHalfLoadCase':
        '''ConceptCouplingHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6437.ConceptCouplingHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
