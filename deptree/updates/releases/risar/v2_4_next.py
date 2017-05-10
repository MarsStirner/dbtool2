# coding: utf-8
"""
Следующая разрабатываемая версия.
"""
from deptree.internals.base import DBToolBaseNode


class Risar_v2_4_next(DBToolBaseNode):
    name = None  # 'risar-v2.4.'
    depends = [
        'risar-v2.4.45',
        'rimis-2201',

    ]
