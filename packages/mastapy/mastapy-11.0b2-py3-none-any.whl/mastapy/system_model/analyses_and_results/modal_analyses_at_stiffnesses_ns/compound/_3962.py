﻿'''_3962.py

MountableComponentCompoundModalAnalysesAtStiffnesses
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _3914
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'MountableComponentCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('MountableComponentCompoundModalAnalysesAtStiffnesses',)


class MountableComponentCompoundModalAnalysesAtStiffnesses(_3914.ComponentCompoundModalAnalysesAtStiffnesses):
    '''MountableComponentCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _MOUNTABLE_COMPONENT_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MountableComponentCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
