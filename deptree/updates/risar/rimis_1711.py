# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class RbTablesRegionCodeAdd(DBToolBaseNode):
    name = 'rimis-1711'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u"""
ALTER TABLE `rbFinance`
ADD COLUMN `regionalCode` VARCHAR(16) NULL COMMENT 'региональный код' AFTER `code`;
""")
            c.execute(u"""
ALTER TABLE `rbPolicyType`
ADD COLUMN `regionalCode` VARCHAR(16) NULL COMMENT 'региональный код' AFTER `TFOMSCode`;
""")
            c.execute(u"""
ALTER TABLE `rbAcheResult`
ADD COLUMN `regionalCode` VARCHAR(16) NULL COMMENT 'региональный код' AFTER `code`;
""")