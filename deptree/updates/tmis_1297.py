# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class FixPersonOldUUIDIndex(DBToolBaseNode):
    name = 'tmis-1297'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''ALTER TABLE `Person` DROP INDEX `uuid_id` ;''')
