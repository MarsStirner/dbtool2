# coding: utf-8
from deptree.internals.base import DBToolBaseNode


class ExtendFieldLength(DBToolBaseNode):
    name = 'rimis-2034'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
                ALTER TABLE `rbProfMedHelp`
                CHANGE COLUMN `name` `name` VARCHAR(256) NOT NULL COMMENT 'Наименование' AFTER `code`;
            ''')
