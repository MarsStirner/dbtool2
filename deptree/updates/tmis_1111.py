# -*- coding: utf-8 -*-
from deptree.internals.base import DBToolBaseNode


class ServiceTotalSumOptimisation(DBToolBaseNode):
    name = 'tmis-1111'
    depends = ['tmis-1111.1', 'tmis-1111.2']


class ServiceTotalSumColumn(DBToolBaseNode):
    name = 'tmis-1111.1'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `Service`
ADD COLUMN `sum` DECIMAL(15,2) NOT NULL DEFAULT 0 AFTER `external_id`;
''')


class ServiceTotalSumMigration(DBToolBaseNode):
    name = 'tmis-1111.2'
    depends = ['tmis-1111.1']

    @classmethod
    def upgrade(cls):
        raise NotImplementedError