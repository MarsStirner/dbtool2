# coding: utf-8

from deptree. internals.base import DBToolBaseNode


class Risar_v2_3_latest(DBToolBaseNode):
    """
    Последняя существующая версия ветки 2.3.
    Может расширяться новыми зависимостями.
    Является зависимостью для установки обновлений версий 2.4
    """
    name = 'risar-v2.3.latest'
    depends = [
        'risar_init.0',
        'rimis-1244'
    ]
