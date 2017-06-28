# coding: utf-8
"""
Следующая разрабатываемая версия.
"""
from deptree.internals.base import DBToolBaseNode


class MisGnc_v1_4_next(DBToolBaseNode):
    name = 'mis-v1.4.next'
    depends = [
        'mis-v1.4.40',
    ]
