﻿'''_1691.py

LoadedBallBearingResults
'''


from mastapy.bearings.bearing_results.rolling import _1764, _1722
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_LOADED_BALL_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedBallBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedBallBearingResults',)


class LoadedBallBearingResults(_1722.LoadedRollingBearingResults):
    '''LoadedBallBearingResults

    This is a mastapy class.
    '''

    TYPE = _LOADED_BALL_BEARING_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedBallBearingResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def track_truncation(self) -> '_1764.TrackTruncationSafetyFactorResults':
        '''TrackTruncationSafetyFactorResults: 'TrackTruncation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1764.TrackTruncationSafetyFactorResults)(self.wrapped.TrackTruncation) if self.wrapped.TrackTruncation else None
