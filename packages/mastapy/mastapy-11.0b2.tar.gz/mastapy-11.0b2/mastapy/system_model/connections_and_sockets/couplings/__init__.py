'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1994 import ClutchConnection
    from ._1995 import ClutchSocket
    from ._1996 import ConceptCouplingConnection
    from ._1997 import ConceptCouplingSocket
    from ._1998 import CouplingConnection
    from ._1999 import CouplingSocket
    from ._2000 import PartToPartShearCouplingConnection
    from ._2001 import PartToPartShearCouplingSocket
    from ._2002 import SpringDamperConnection
    from ._2003 import SpringDamperSocket
    from ._2004 import TorqueConverterConnection
    from ._2005 import TorqueConverterPumpSocket
    from ._2006 import TorqueConverterTurbineSocket
