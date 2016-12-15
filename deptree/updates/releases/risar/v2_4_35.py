# coding: utf-8

from deptree. internals.base import DBToolBaseNode


class Risar_v2_4_35(DBToolBaseNode):
    name = 'risar-v2.4.35'
    depends = [
        'risar-v2.4.33',
        'rimis-1797', 'rimis-1820.1'
    ]
