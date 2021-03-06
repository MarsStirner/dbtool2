# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class RefbooksTableRegionCode(DBToolBaseNode):
    name = 'rimis-1854'
    depends = ['rimis-1717', 'rimis-1844', 'rimis-1852', 'rimis-1711', 'rimis-1854.add',
               'rimis-1854.change', 'rimis-1854.datamigrate', 'rimis-1854.datamigrate2',
               'rimis-1854.add2']


class RefbooksTableRegionCode2(DBToolBaseNode):
    name = 'rimis-1854-2'
    depends = ['rimis-1854', 'rimis-1854.datamigrate3']


class RefbooksRegionCodeChange(DBToolBaseNode):
    name = 'rimis-1854.change'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u"""
ALTER TABLE `Organisation`
CHANGE COLUMN `regionalCode` `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код';
""")
            c.execute(u"""
ALTER TABLE `OrgStructure`
CHANGE COLUMN `regionalCode` `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код';
""")
            c.execute(u"""
ALTER TABLE `Person`
CHANGE COLUMN `regionalCode` `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код';
""")
            c.execute(u"""
ALTER TABLE `rbAcheResult`
CHANGE COLUMN `regionalCode` `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код';
""")
            c.execute(u"""
ALTER TABLE `rbDocumentType`
CHANGE COLUMN `regionalCode` `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код';
""")
            c.execute(u"""
ALTER TABLE `rbFinance`
CHANGE COLUMN `regionalCode` `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код';
""")
            c.execute(u"""
ALTER TABLE `rbJobType`
CHANGE COLUMN `regionalCode` `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код';
""")
            c.execute(u"""
ALTER TABLE `rbMedicalAidProfile`
CHANGE COLUMN `regionalCode` `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код';
""")
            c.execute(u"""
ALTER TABLE `rbMesSpecification`
CHANGE COLUMN `regionalCode` `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код';
""")
            c.execute(u"""
ALTER TABLE `rbPolicyType`
CHANGE COLUMN `regionalCode` `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код';
""")
            c.execute(u"""
ALTER TABLE `rbPost`
CHANGE COLUMN `regionalCode` `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код';
""")
            c.execute(u"""
ALTER TABLE `rbRelationType`
CHANGE COLUMN `regionalCode` `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код';
""")
            c.execute(u"""
ALTER TABLE `rbSocStatusType`
CHANGE COLUMN `regionalCode` `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код';
""")
            c.execute(u"""
ALTER TABLE `rbResult`
CHANGE COLUMN `regionalCode` `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код';
""")
            c.execute(u"""
ALTER TABLE `rbSpeciality`
CHANGE COLUMN `regionalCode` `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код';
""")
            c.execute(u"""
ALTER TABLE `ActionPropertyTemplate`
CHANGE COLUMN `regionalCode` `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код';
""")

# эти таблицы используются только в печати
            c.execute(u"""
ALTER TABLE `rbEventProfile`
CHANGE COLUMN `regionalCode` `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код';
""")
            c.execute(u"""
ALTER TABLE `rbMedicalAidUnit`
CHANGE COLUMN `regionalCode` `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код';
""")
            c.execute(u"""
ALTER TABLE `rbNomenclature`
CHANGE COLUMN `regionalCode` `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код';
""")
            c.execute(u"""
ALTER TABLE `rbTempInvalidReason`
CHANGE COLUMN `regionalCode` `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код';
""")


class RefbooksRegionCodeAdd(DBToolBaseNode):
    name = 'rimis-1854.add'

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


class RefbooksRegionCodeAdd2(DBToolBaseNode):
    name = 'rimis-1854.add2'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u"""
ALTER TABLE `rbTraumaType`
ADD COLUMN `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код' AFTER `name`;
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

#             c.execute(u"""
# UPDATE `rbAcheResult` t set t.regionalCode = t.code WHERE t.code > '';
# """)
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
#             c.execute(u"""
# UPDATE `rbFinance` t set t.regionalCode = t.code WHERE t.code > '';
# """)
            c.execute(u"""
UPDATE `rbMeasureStatus` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `MKB` t set t.regionalCode = t.DiagID WHERE t.DiagID > '';
""")
            c.execute(u"""
UPDATE `Measure` t set t.regionalCode = t.code WHERE t.code > '';
""")


class RefbooksTableMigrate2Code(DBToolBaseNode):
    name = 'rimis-1854.datamigrate2'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:

            c.execute(u"""
UPDATE `rbDocumentType` t set t.regionalCode = t.TFOMSCode WHERE t.TFOMSCode > '';
""")
            c.execute(u"""
UPDATE `rbEventProfile` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbJobType` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbMedicalAidProfile` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbMedicalAidUnit` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbMesSpecification` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbNomenclature` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbPolicyType` t set t.regionalCode = t.TFOMSCode WHERE t.TFOMSCode > '';
""")
            c.execute(u"""
UPDATE `rbPost` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbRelationType` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbSocStatusType` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbResult` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbSpeciality` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbTempInvalidReason` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `ActionPropertyTemplate` t set t.regionalCode = t.code WHERE t.code > '';
""")


class RefbooksTableMigrate3Code(DBToolBaseNode):
    name = 'rimis-1854.datamigrate3'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:

            c.execute(u"""
UPDATE `rbAcheResult` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbFinance` t set t.regionalCode = t.code WHERE t.code > '';
""")
            c.execute(u"""
UPDATE `rbReserveType` t set t.regionalCode = t.code WHERE t.code > '';
""")
