'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1483 import ColumnInputOptions
    from ._1484 import DataInputFileOptions
