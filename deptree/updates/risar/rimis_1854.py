# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class OrganisationTableRegionCode(DBToolBaseNode):
    name = 'rimis-1854'
    depends = ['rimis-1711', 'rimis-1854.add', 'rimis-1854.change', 'rimis-1854.datamigrate']


class RefbooksRegionCodeChange(DBToolBaseNode):
    name = 'rimis-1854.change'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u"""
ALTER TABLE `Organisation`
CHANGE COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '';
""")
            c.execute(u"""
ALTER TABLE `OrgStructure`
CHANGE COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '';
""")
            c.execute(u"""
ALTER TABLE `Person`
CHANGE COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '';
""")
            c.execute(u"""
ALTER TABLE `rbAcheResult`
CHANGE COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '';
""")
            c.execute(u"""
ALTER TABLE `rbDocumentType`
CHANGE COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '';
""")
            c.execute(u"""
ALTER TABLE `rbEventProfile`
CHANGE COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '';
""")
            c.execute(u"""
ALTER TABLE `rbFinance`
CHANGE COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '';
""")
            c.execute(u"""
ALTER TABLE `rbJobType`
CHANGE COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '';
""")
            c.execute(u"""
ALTER TABLE `rbMedicalAidProfile`
CHANGE COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '';
""")
            c.execute(u"""
ALTER TABLE `rbMedicalAidUnit`
CHANGE COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '';
""")
            c.execute(u"""
ALTER TABLE `rbMesSpecification`
CHANGE COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '';
""")
            c.execute(u"""
ALTER TABLE `rbNomenclature`
CHANGE COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '';
""")
            c.execute(u"""
ALTER TABLE `rbPolicyType`
CHANGE COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '';
""")
            c.execute(u"""
ALTER TABLE `rbPost`
CHANGE COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '';
""")
            c.execute(u"""
ALTER TABLE `rbRelationType`
CHANGE COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '';
""")
            c.execute(u"""
ALTER TABLE `rbSocStatusType`
CHANGE COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '';
""")
            c.execute(u"""
ALTER TABLE `rbResult`
CHANGE COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '';
""")
            c.execute(u"""
ALTER TABLE `rbSpeciality`
CHANGE COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '';
""")
            c.execute(u"""
ALTER TABLE `rbTempInvalidReason`
CHANGE COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '';
""")
            c.execute(u"""
ALTER TABLE `ActionPropertyTemplate`
CHANGE COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '';
""")


class RefbooksRegionCodeAdd(DBToolBaseNode):
    name = 'rimis-1854.add'
    """
    ALTER TABLE `rbPost`
	CHANGE COLUMN `regionalCode` `regionalCode` VARCHAR(9) NOT NULL DEFAULT '' COMMENT 'Региональный код' AFTER `name`;
	"""
    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u"""
ALTER TABLE `rbBloodType`
ADD COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код' AFTER `name`;
""")
            c.execute(u"""
ALTER TABLE `rbSocStatusClass`
ADD COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код' AFTER `name`;
""")
#             c.execute(u"""
# ALTER TABLE `rbAcheResult`
# ADD COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код' AFTER `name`;
# """)
            c.execute(u"""
ALTER TABLE `rbDiseaseCharacter`
ADD COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код' AFTER `name`;
""")
            c.execute(u"""
ALTER TABLE `rbDispanser`
ADD COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код' AFTER `name`;
""")

            c.execute(u"""
ALTER TABLE `rbPerinatalRiskRate`
ADD COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код' AFTER `name`;
""")
            c.execute(u"""
ALTER TABLE `rbPregnancyPathology`
ADD COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код' AFTER `name`;
""")
            c.execute(u"""
ALTER TABLE `rbErrandStatus`
ADD COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код' AFTER `name`;
""")
            c.execute(u"""
ALTER TABLE `rbPreEclampsiaRate`
ADD COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код' AFTER `name`;
""")
            c.execute(u"""
ALTER TABLE `rbRadzinskyRiskRate`
ADD COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код' AFTER `value`;
""")
            c.execute(u"""
ALTER TABLE `rbProfMedHelp`
ADD COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код' AFTER `name`;
""")
            c.execute(u"""
ALTER TABLE `rbConditionMedHelp`
ADD COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код' AFTER `name`;
""")

#             c.execute(u"""
# ALTER TABLE `rbFinance`
# ADD COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код' AFTER `name`;
# """)

            c.execute(u"""
ALTER TABLE `rbMeasureStatus`
ADD COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код' AFTER `name`;
""")

            c.execute(u"""
ALTER TABLE `MKB`
ADD COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код' AFTER `deleted`;
""")

            c.execute(u"""
ALTER TABLE `Measure`
ADD COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код' AFTER `templateAction_id`;
""")


class RefbooksTableMigrateCode(DBToolBaseNode):
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
UPDATE `MKB` t set t.regionalCode = t.DiagID WHERE t.DiagID > '';
""")
            c.execute(u"""
UPDATE `Measure` t set t.regionalCode = t.code WHERE t.code > '';
""")
