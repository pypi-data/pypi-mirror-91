﻿'''_3968.py

PlanetaryConnectionCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1888
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3847
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _3980
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'PlanetaryConnectionCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnectionCompoundModalAnalysesAtStiffnesses',)


class PlanetaryConnectionCompoundModalAnalysesAtStiffnesses(_3980.ShaftToMountableComponentConnectionCompoundModalAnalysesAtStiffnesses):
    '''PlanetaryConnectionCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_CONNECTION_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryConnectionCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1888.PlanetaryConnection':
        '''PlanetaryConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1888.PlanetaryConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1888.PlanetaryConnection':
        '''PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1888.PlanetaryConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3847.PlanetaryConnectionModalAnalysesAtStiffnesses]':
        '''List[PlanetaryConnectionModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3847.PlanetaryConnectionModalAnalysesAtStiffnesses))
        return value

    @property
    def connection_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_3847.PlanetaryConnectionModalAnalysesAtStiffnesses]':
        '''List[PlanetaryConnectionModalAnalysesAtStiffnesses]: 'ConnectionModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysesAtStiffnessesLoadCases, constructor.new(_3847.PlanetaryConnectionModalAnalysesAtStiffnesses))
        return value
