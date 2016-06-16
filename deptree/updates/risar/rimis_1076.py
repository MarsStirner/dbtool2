# coding: utf-8

from deptree. internals.base import DBToolBaseNode


class ErrandsCommunications(DBToolBaseNode):
    name = 'rimis-1076'
    depends = ['rimis-1076.1', 'rimis-1076.2']


class ErrandsCommunicationsAdf(DBToolBaseNode):
    name = 'rimis-1076.2'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `Errand` ADD COLUMN `communications` TEXT NULL COMMENT 'Контакты(телефоны, емайлы, скайпы)' AFTER `status_id`;
''')
