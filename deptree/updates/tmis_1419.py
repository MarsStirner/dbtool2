# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class APT_AddFieldNotLoadableWithTemplate(DBToolBaseNode):
    name = 'tmis-1419'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''ALTER TABLE `ActionPropertyType`
ADD COLUMN `notLoadableWithTemplate` TINYINT(1) NULL DEFAULT NULL COMMENT 'Свойство не должно копироваться из шаблонного в другие документы' AFTER `modifyPerson_id`;
''')
