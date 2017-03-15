# coding: utf-8
"""
Набор обновлений для установки в регионе Саратовской области
"""
from deptree.internals.base import DBToolBaseNode


class SaratovRisar_v2_4(DBToolBaseNode):
    name = 'risar-v2.4.saratov'
    depends = [
        'rimis-2157',
    ]
