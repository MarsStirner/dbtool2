# coding: utf-8

from deptree. internals.base import DBToolBaseNode


class Risar_v2_4_33(DBToolBaseNode):
    name = 'risar-v2.4.33'
    depends = [
        'risar-v2.4.28',
        'rimis-1691', 'rimis-785'
    ]
