# coding: utf-8

from deptree. internals.base import DBToolBaseNode


class Risar_v2_4_38(DBToolBaseNode):
    name = 'risar-v2.4.38'
    depends = [
        'risar-v2.4.35',
        'rimis-1820.common', 'rimis-1844', 'rimis-1852', 'rimis-1894'
    ]
