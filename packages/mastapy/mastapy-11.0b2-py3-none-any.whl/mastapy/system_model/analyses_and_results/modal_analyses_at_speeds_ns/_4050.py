﻿'''_4050.py

CVTBeltConnectionModalAnalysesAtSpeeds
'''


from mastapy.system_model.connections_and_sockets import _1877
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4019
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'CVTBeltConnectionModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnectionModalAnalysesAtSpeeds',)


class CVTBeltConnectionModalAnalysesAtSpeeds(_4019.BeltConnectionModalAnalysesAtSpeeds):
    '''CVTBeltConnectionModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _CVT_BELT_CONNECTION_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTBeltConnectionModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1877.CVTBeltConnection':
        '''CVTBeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1877.CVTBeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None
