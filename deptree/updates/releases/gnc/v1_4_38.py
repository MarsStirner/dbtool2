# coding: utf-8
from deptree.internals.base import DBToolBaseNode


class MisGnc_v1_4_38(DBToolBaseNode):
    name = 'mis-v1.4.38'
    depends = [
        'mis-v1.4.36',
        'tmis-1379', 'tmis-1487',
    ]
