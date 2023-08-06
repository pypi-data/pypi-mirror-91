﻿'''_3926.py

CouplingCompoundModalAnalysesAtStiffnesses
'''


from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import _3981
from mastapy._internal.python_net import python_net_import

_COUPLING_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'CouplingCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingCompoundModalAnalysesAtStiffnesses',)


class CouplingCompoundModalAnalysesAtStiffnesses(_3981.SpecialisedAssemblyCompoundModalAnalysesAtStiffnesses):
    '''CouplingCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _COUPLING_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingCompoundModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
