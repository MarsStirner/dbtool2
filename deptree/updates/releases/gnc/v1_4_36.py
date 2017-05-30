# coding: utf-8
from deptree.internals.base import DBToolBaseNode


class MisGnc_v1_4_36(DBToolBaseNode):
    name = 'mis-v1.4.36'
    depends = [
        'mis-v1.4.35',
        'tmis-1449', 'tmis-1459', 'tmis-1365', 'tmis-1403'
    ]
