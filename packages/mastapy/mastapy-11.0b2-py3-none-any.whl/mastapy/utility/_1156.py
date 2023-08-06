﻿'''_1156.py

PerMachineSettings
'''


from mastapy.utility import _1157
from mastapy._internal.python_net import python_net_import

_PER_MACHINE_SETTINGS = python_net_import('SMT.MastaAPI.Utility', 'PerMachineSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('PerMachineSettings',)


class PerMachineSettings(_1157.PersistentSingleton):
    '''PerMachineSettings

    This is a mastapy class.
    '''

    TYPE = _PER_MACHINE_SETTINGS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PerMachineSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
