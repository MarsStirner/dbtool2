# coding: utf-8
from deptree.internals.base import DBToolBaseNode


class MisGnc_v1_4_35(DBToolBaseNode):
    name = 'mis-v1.4.35'
    depends = [
        'mis-v1.4.34',
        'tmis-1361',
        'tmis-1449',
    ]
