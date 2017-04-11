# coding: utf-8
from deptree.internals.base import DBToolBaseNode


class MisGnc_v1_4_34(DBToolBaseNode):
    name = 'mis-v1.4.34'
    depends = [
        'mis-v1.4.33', 'tmis-1382', 'tmis-1406', 'tmis-1384', 'tmis-1385',
    ]
