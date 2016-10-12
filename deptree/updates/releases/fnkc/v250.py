# coding: utf-8

from deptree. internals.base import DBToolBaseNode


class FNKC_V250(DBToolBaseNode):
    """
    Первая версия для обновления бд ФНКЦ, использующая dbtool2
    """
    name = 'fnkc-v250'
    depends = [
        'tmis-1233',
        'webmis-494'
    ]
