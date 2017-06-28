# coding: utf-8
from deptree.internals.base import DBToolBaseNode


class MisGnc_v1_4_40(DBToolBaseNode):
    name = 'mis-v1.4.40'
    depends = [
        'mis-v1.4.38',
        'tmis-1189'
    ]
