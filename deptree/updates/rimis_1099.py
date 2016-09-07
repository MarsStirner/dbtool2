# coding: utf-8

from deptree. internals.base import DBToolBaseNode


class DiagnosisEndDateTimeAndFixes(DBToolBaseNode):
    name = 'rimis-1099'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `Diagnosis`
CHANGE COLUMN `endDate` `endDate` DATETIME NULL DEFAULT NULL COMMENT 'Дата окончания заболевания' ;
''')

            c.ececute(u'''
DROP TRIGGER IF EXISTS `afterDeleteDiagnostic` ;
''')

            c.ececute(u'''
ALTER TABLE `Diagnosis`
CHANGE COLUMN `diagnosisType_id` `diagnosisType_id` INT(11) NULL COMMENT 'Тип диагноза {rbDiagnosisType}' ,
CHANGE COLUMN `MKB` `MKB` VARCHAR(8) NULL COMMENT 'Код по МКБ X (с пятым знаком)' ,
CHANGE COLUMN `MKBEx` `MKBEx` VARCHAR(8) NULL COMMENT 'Вторая секция кода по МКБ X (с пятым знаком)' ;
''')

            c.ececute(u'''
ALTER TABLE `Diagnostic`
CHANGE COLUMN `event_id` `event_id` INT(11) NULL COMMENT 'Событие {Event}' ,
CHANGE COLUMN `diagnosisType_id` `diagnosisType_id` INT(11) NULL DEFAULT NULL COMMENT 'Тип диагноза {rbDiagnosisType}' ,
CHANGE COLUMN `sanatorium` `sanatorium` TINYINT(1) NULL DEFAULT 0 COMMENT 'Сан-кур лечение: 0-не нуждается, 1-нуждается, 2-направлен, 3-пролечен' ,
CHANGE COLUMN `hospital` `hospital` TINYINT(1) NULL DEFAULT 0 COMMENT 'Госпитализация : 0-не нуждается, 1-нуждается, 2-направлен, 3-пролечен' ,
CHANGE COLUMN `speciality_id` `speciality_id` INT(11) NULL DEFAULT NULL COMMENT 'Специальность {rbSpeciality}' ,
CHANGE COLUMN `notes` `notes` TEXT NULL DEFAULT NULL COMMENT 'Примечания' ,
CHANGE COLUMN `version` `version` INT(10) UNSIGNED NOT NULL DEFAULT 0 COMMENT 'Версия данных' ;
''')
