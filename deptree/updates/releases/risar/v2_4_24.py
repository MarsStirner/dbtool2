# coding: utf-8

from deptree. internals.base import DBToolBaseNode


class Risar_v2_4_24(DBToolBaseNode):
    name = 'risar-v2.4.24'
    depends = [
        'risar-v2.4.21',
        'rimis-1455.foreign-keys', 'rimis-1659'
    ]
