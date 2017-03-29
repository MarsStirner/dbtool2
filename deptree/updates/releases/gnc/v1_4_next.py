# coding: utf-8
"""
Следующая разрабатываемая версия.
"""
from deptree.internals.base import DBToolBaseNode


class MisGnc_v1_4_next(DBToolBaseNode):
    name = 'mis-v1.4.next'
    depends = [

        'tmis-1160', 'tmis-1421', 'tmis-1419', 'tmis-1410', 'tmis-1430',
    ]
