# coding: utf-8

from deptree.internals.base import DBToolBaseNode


class Risar_v2_4_9(DBToolBaseNode):
    name = 'risar-v2.4.9'
    depends = [
        'risar-v2.4.0',
        'rimis-1281', 'rimis-1472', 'rimis-1382'
    ]
