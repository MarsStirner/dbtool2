# coding: utf-8

from deptree.internals.base import DBToolBaseNode


class Risar_v2_4_21(DBToolBaseNode):
    name = 'risar-v2.4.21'
    depends = [
        'risar-v2.4.9',
        'rimis-1455', 'rimis-1465', 'rimis-1348',
        # from 2.3:
        'rimis-1099'
    ]
