# coding: utf-8
from deptree.internals.base import DBToolBaseNode


class MisGnc_v1_4_33(DBToolBaseNode):
    name = 'mis-v1.4.33'
    depends = [
        'tmis-1160', 'tmis-1421', 'tmis-1419', 'tmis-1410', 'tmis-1430', 'tmis-1259'
    ]
