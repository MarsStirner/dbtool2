# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class LabActionNotes(DBToolBaseNode):
    name = 'tmis-1384'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''ALTER TABLE `ActionType`
ADD COLUMN `noteMandatory` TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'Заметка является обязательной для заполнения при создании Action' AFTER `hasPrescriptions`;
''')
            c.execute(u'''
ALTER TABLE `ActionPropertyType`
ADD COLUMN `noteMandatory` TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'Заметка является обязательной для заполнения при создании ActionProperty' AFTER `notLoadableWithTemplate`;
''')
            c.execute(u'''
ALTER TABLE `ActionProperty`
ADD COLUMN `note` TEXT NULL DEFAULT NULL AFTER `version`;
''')
