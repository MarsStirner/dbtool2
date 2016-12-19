# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class OrgStructureTableRegionCode(DBToolBaseNode):
    name = 'rimis-1852'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u"""
ALTER TABLE `OrgStructure`
ADD COLUMN `TFOMSCode` VARCHAR(50) NULL COMMENT 'Код ТФОМС' AFTER `show`;
""")
            c.execute(u"""
ALTER TABLE `OrgStructure`
ADD COLUMN `regionalCode` VARCHAR(50) NULL COMMENT 'региональный код' AFTER `TFOMSCode`;
""")
