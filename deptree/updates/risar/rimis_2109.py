# coding: utf-8
from deptree.internals.base import DBToolBaseNode


class rbReserveTypeDefaultColor(DBToolBaseNode):
    name = 'rimis-2109'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `rbReserveType`
CHANGE COLUMN `color` `color` VARCHAR(16) NOT NULL DEFAULT '#777777' AFTER `name`;
            ''')
