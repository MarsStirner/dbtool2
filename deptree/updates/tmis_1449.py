# coding: utf-8


from deptree.internals.base import DBToolBaseNode


class AddColumnMaxSubServices(DBToolBaseNode):
    name = 'tmis-1449'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `rbService`
ADD COLUMN `maxSubServices` TINYINT(1) NOT NULL DEFAULT '0' COMMENT 'Максимальное количество назначаемых подуслуг' AFTER `isComplex`;
''')
