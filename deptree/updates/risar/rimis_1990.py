# coding: utf-8
from deptree.internals.base import DBToolBaseNode


class RemoveNonNullProperty(DBToolBaseNode):
    name = 'rimis-1990'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
                ALTER TABLE `ClientAllergy`
                CHANGE COLUMN `power` `power` INT(11) NULL ;
            ''')
