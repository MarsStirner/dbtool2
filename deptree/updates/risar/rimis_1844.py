# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class OrganisationTableRegionCode(DBToolBaseNode):
    name = 'rimis-1844'
    depends = ['rimis-1844.add', 'rimis-1844.datamigrate']


class OrganisationTableRegionCodeAdd(DBToolBaseNode):
    name = 'rimis-1844.add'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u"""
ALTER TABLE `Organisation`
ADD COLUMN `FFOMSCode` VARCHAR(50) NULL COMMENT 'Код ФФОМС' AFTER `TFOMSCode`;
""")
            c.execute(u"""
ALTER TABLE `Organisation`
ADD COLUMN `regionalCode` VARCHAR(50) NULL COMMENT 'региональный код' AFTER `FFOMSCode`;
""")


class OrganisationTableMigrateTFOMSCode(DBToolBaseNode):
    name = 'rimis-1844.datamigrate'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u"""
UPDATE `Organisation` org
set org.regionalCode = org.TFOMSCode
WHERE org.TFOMSCode > '';
""")