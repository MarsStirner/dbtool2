# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class OrganisationTableRegionCode(DBToolBaseNode):
    name = 'rimis-1854'
    depends = ['rimis-1854.add', 'rimis-1854.datamigrate']


class OrganisationTableRegionCodeAdd(DBToolBaseNode):
    name = 'rimis-1854.add'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u"""
ALTER TABLE `rbBloodType`
ADD COLUMN `regionalCode` VARCHAR(64) NULL COMMENT 'региональный код' AFTER `name`;
""")
            c.execute(u"""
ALTER TABLE `rbSocStatusClass`
ADD COLUMN `regionalCode` VARCHAR(64) NULL COMMENT 'региональный код' AFTER `name`;
""")
            c.execute(u"""
ALTER TABLE `rbSocStatusType`
CHANGE COLUMN `FFOMSCode` VARCHAR(64) NULL COMMENT 'региональный код' AFTER `TFOMSCode`;
""")
            c.execute(u"""
ALTER TABLE `rbResult`
CHANGE COLUMN `regionalCode` VARCHAR(64) NULL COMMENT 'региональный код' AFTER `continued`;
""")
            c.execute(u"""
ALTER TABLE `rbAcheResult`
ADD COLUMN `regionalCode` VARCHAR(64) NULL COMMENT 'региональный код' AFTER `name`;
""")
            c.execute(u"""
ALTER TABLE `rbDiseaseCharacter`
ADD COLUMN `regionalCode` VARCHAR(64) NULL COMMENT 'региональный код' AFTER `name`;
""")
            c.execute(u"""
ALTER TABLE `rbDispanser`
ADD COLUMN `regionalCode` VARCHAR(64) NULL COMMENT 'региональный код' AFTER `name`;
""")

            c.execute(u"""
ALTER TABLE `rbPerinatalRiskRate`
ADD COLUMN `regionalCode` VARCHAR(64) NULL COMMENT 'региональный код' AFTER `name`;
""")
            c.execute(u"""
ALTER TABLE `rbPregnancyPathology`
ADD COLUMN `regionalCode` VARCHAR(64) NULL COMMENT 'региональный код' AFTER `name`;
""")
            c.execute(u"""
ALTER TABLE `rbErrandStatus`
ADD COLUMN `regionalCode` VARCHAR(64) NULL COMMENT 'региональный код' AFTER `name`;
""")
            c.execute(u"""
ALTER TABLE `rbPreEclampsiaRate`
ADD COLUMN `regionalCode` VARCHAR(64) NULL COMMENT 'региональный код' AFTER `name`;
""")
            c.execute(u"""
ALTER TABLE `rbRadzinskyRiskRate`
ADD COLUMN `regionalCode` VARCHAR(64) NULL COMMENT 'региональный код' AFTER `value`;
""")
            c.execute(u"""
ALTER TABLE `rbProfMedHelp`
ADD COLUMN `regionalCode` VARCHAR(64) NULL COMMENT 'региональный код' AFTER `name`;
""")
            c.execute(u"""
ALTER TABLE `rbConditionMedHelp`
ADD COLUMN `regionalCode` VARCHAR(64) NULL COMMENT 'региональный код' AFTER `name`;
""")

            c.execute(u"""
ALTER TABLE `rbFinance`
ADD COLUMN `regionalCode` VARCHAR(64) NULL COMMENT 'региональный код' AFTER `name`;
""")

            c.execute(u"""
ALTER TABLE `rbMeasureStatus`
ADD COLUMN `regionalCode` VARCHAR(64) NULL COMMENT 'региональный код' AFTER `name`;
""")

            c.execute(u"""
ALTER TABLE `MKB`
ADD COLUMN `regionalCode` VARCHAR(64) NULL COMMENT 'региональный код' AFTER `deleted`;
""")

            c.execute(u"""
ALTER TABLE `Measure`
ADD COLUMN `regionalCode` VARCHAR(64) NULL COMMENT 'региональный код' AFTER `templateAction_id`;
""")


class OrganisationTableMigrateTFOMSCode(DBToolBaseNode):
    name = 'rimis-1854.datamigrate'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u"""
UPDATE `rbBloodType` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbSocStatusClass` t set t.regionalCode = t.code WHERE t.code > '';
""")

            c.execute(u"""
UPDATE `rbAcheResult` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbDiseaseCharacter` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbDispanser` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbPerinatalRiskRate` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbPregnancyPathology` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbErrandStatus` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbPreEclampsiaRate` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbRadzinskyRiskRate` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbProfMedHelp` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbConditionMedHelp` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbFinance` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbMeasureStatus` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `Measure` t set t.regionalCode = t.code WHERE t.code > '';
""")
