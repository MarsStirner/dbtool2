# coding: utf-8

from deptree. internals.base import DBToolBaseNode


class Risar_v2_4_41(DBToolBaseNode):
    name = 'risar-v2.4.41'
    depends = [
        'risar-v2.4.38',
        'rimis-1854', 'rimis-2008', 'rimis-1696', 'rimis-1981'
    ]
