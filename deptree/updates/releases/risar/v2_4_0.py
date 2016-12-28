# coding: utf-8

from deptree. internals.base import DBToolBaseNode


class Risar_v2_4_0(DBToolBaseNode):
    name = 'risar-v2.4.0'
    depends = [
        'risar-v2.3.latest',
        'rimis-1210', 'rimis-682'
    ]
