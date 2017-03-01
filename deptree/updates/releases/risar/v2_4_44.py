# coding: utf-8

from deptree.internals.base import DBToolBaseNode


class Risar_v2_4_44(DBToolBaseNode):
    name = 'risar-v2.4.44'
    depends = [
        'risar-v2.4.41',
        'rimis-1990', 'rimis-2034', 'rimis-2109', 'rimis-1854.datamigrate3',
        'rimis-1854-2', 'rimis-2121'
    ]
