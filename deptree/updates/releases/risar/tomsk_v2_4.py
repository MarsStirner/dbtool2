# coding: utf-8
"""
Набор обновлений для установки в регионе Томской области
"""
from deptree.internals.base import DBToolBaseNode


class TomskRisar_v2_4(DBToolBaseNode):
    name = 'risar-v2.4.tomsk'
    depends = [
        'rimis-1885',
    ]
