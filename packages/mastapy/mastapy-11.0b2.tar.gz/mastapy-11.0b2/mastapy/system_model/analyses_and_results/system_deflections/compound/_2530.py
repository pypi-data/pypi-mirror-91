'''_2530.py

CycloidalDiscPlanetaryBearingConnectionCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets.cycloidal import _1990
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2372
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2487
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'CycloidalDiscPlanetaryBearingConnectionCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscPlanetaryBearingConnectionCompoundSystemDeflection',)


class CycloidalDiscPlanetaryBearingConnectionCompoundSystemDeflection(_2487.AbstractShaftToMountableComponentConnectionCompoundSystemDeflection):
    '''CycloidalDiscPlanetaryBearingConnectionCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscPlanetaryBearingConnectionCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1990.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1990.CycloidalDiscPlanetaryBearingConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1990.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1990.CycloidalDiscPlanetaryBearingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2372.CycloidalDiscPlanetaryBearingConnectionSystemDeflection]':
        '''List[CycloidalDiscPlanetaryBearingConnectionSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2372.CycloidalDiscPlanetaryBearingConnectionSystemDeflection))
        return value

    @property
    def connection_system_deflection_load_cases(self) -> 'List[_2372.CycloidalDiscPlanetaryBearingConnectionSystemDeflection]':
        '''List[CycloidalDiscPlanetaryBearingConnectionSystemDeflection]: 'ConnectionSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionLoadCases, constructor.new(_2372.CycloidalDiscPlanetaryBearingConnectionSystemDeflection))
        return value
