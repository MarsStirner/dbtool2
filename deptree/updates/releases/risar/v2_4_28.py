# coding: utf-8

from deptree.internals.base import DBToolBaseNode


class Risar_v2_4_28(DBToolBaseNode):
    name = 'risar-v2.4.28'
    depends = [
        'risar-v2.4.24',
        'rimis-1693', 'rimis-1717', 'rimis-1696', 'rimis-1711'
    ]
