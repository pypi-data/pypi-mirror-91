'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1485 import CustomLineChart
    from ._1486 import CustomTableAndChart
