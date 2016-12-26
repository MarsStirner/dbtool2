# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class HospAppointmentsTula(DBToolBaseNode):
    name = 'rimis-1820'
    depends = ['rimis-1820.1', 'rimis-1820.2', 'rimis-1820.fix1', 'rimis-1820.fix2']


class ActionNumbersCommon(DBToolBaseNode):
    name = 'rimis-1820.common'
    depends = ['rimis-1820.1', 'rimis-1820.fix1.maintable', 'rimis-1820.common.kind_data']


class HospAppointmentsTulaFixes(DBToolBaseNode):
    name = 'rimis-1820.fix1'
    depends = ['rimis-1820.fix1.maintable', 'rimis-1820.tula_number_types', 'rimis-1820.fix1.trigger']


class ActionNumbersTableAdd(DBToolBaseNode):
    name = 'rimis-1820.1'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `ActionNumbers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_id` int(11) NOT NULL COMMENT '{Action}',
  `entity_type` enum('HOSP_APNT_TU') NOT NULL,
  `number` varchar(191) NOT NULL COMMENT 'Номер документа',
  `prefix` varchar(32) DEFAULT NULL COMMENT 'Дополнительный префикс',
  `postfix` varchar(32) DEFAULT NULL COMMENT 'Дополнительный постфикс',
  `date` date DEFAULT NULL COMMENT 'Тип сущности для генерации номера (''HOSP_APNT_TU''-направления на госпитализацию Тула)',
  PRIMARY KEY (`id`),
  KEY `idx_date` (`date`),
  KEY `fk_actionnumbers_action_idx` (`action_id`),
  CONSTRAINT `fk_actionnumbers_action` FOREIGN KEY (`action_id`) REFERENCES `Action` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Номера документов, которые генерируются при создании экшенов';
''')


class TulaHospApntNumbersActionTrigger(DBToolBaseNode):
    name = 'rimis-1820.2'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'DROP TRIGGER IF EXISTS onInsertAction')
            c.execute(u'''
CREATE DEFINER={0} TRIGGER `onInsertAction` AFTER INSERT ON `Action` FOR EACH ROW
BEGIN
    DECLARE apnt_postfix INT(11);
    DECLARE apnt_prefix INT(11);
    DECLARE apnt_org_code VARCHAR(50);
    DECLARE apnt_dep_code VARCHAR(50);
    DECLARE apnt_date_code VARCHAR(8);
    DECLARE apnt_number VARCHAR(191);

    DECLARE flatCode VARCHAR(64);
    SELECT `ActionType`.`flatCode` INTO flatCode FROM `ActionType` WHERE `ActionType`.`id` = NEW.`actionType_id`;

    IF flatCode = "tula_hosp" THEN
        SELECT
            CAST(prefix as UNSIGNED), CAST(postfix as UNSIGNED)
            INTO
            apnt_prefix, apnt_postfix
        FROM ActionNumbers
        WHERE date = DATE(NEW.begDate) AND entity_type = 'HOSP_APNT_TU'
        ORDER BY prefix DESC, postfix DESC LIMIT 1 FOR UPDATE;
        IF apnt_postfix IS NULL THEN
            SET apnt_postfix = 900;
            SET apnt_prefix = 0;
        ELSE
            SET apnt_postfix = apnt_postfix + 1;
            IF apnt_postfix > 999 THEN
                SET apnt_prefix = apnt_prefix + 1;
                SET apnt_postfix = 900;
            END IF;
        END IF;

        SELECT
            o.TFOMSCode, os.TFOMSCode
            INTO
            apnt_org_code, apnt_dep_code
        FROM Action a
            JOIN Event e ON a.event_id = e.id
            JOIN Person p ON e.execPerson_id = p.id
            JOIN Organisation o ON p.org_id = o.id
            JOIN OrgStructure os ON o.id = os.organisation_id
        WHERE a.id = NEW.id
        LIMIT 1;

        SET apnt_date_code = DATE_FORMAT(NEW.begDate, "%y%m%d");

        SET apnt_number = CONCAT(
            COALESCE(apnt_org_code, '000'),
            COALESCE(apnt_dep_code, '000'),
            apnt_date_code, apnt_postfix
        );

        INSERT INTO `ActionNumbers`
            (`action_id`, `entity_type`, `number`, `prefix`, `postfix`, `date`)
        VALUES
            (NEW.id, 'HOSP_APNT_TU', apnt_number,
             CAST(apnt_prefix as CHAR(32)),
             CAST(apnt_postfix as CHAR(32)),
             DATE(NEW.begDate));

    END IF;
END'''.format(cls.config['definer']))


class ActionNumbersTypeKindTables(DBToolBaseNode):
    name = 'rimis-1820.type_kind_tables'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `rbActionNumberKind` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(16) NOT NULL,
  `name` VARCHAR(64) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'Вид номера документа';
''')

            c.execute(u'''
CREATE TABLE `rbActionNumberType` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(16) NOT NULL COMMENT 'Ожидается использование первых двух цифр из кладр кода региона',
  `name` VARCHAR(64) NOT NULL,
  `kind_id` INT(11) NOT NULL COMMENT '{rbActionNumberKind}',
  PRIMARY KEY (`id`),
  KEY `fk_rbactionnumbertype_kind` (`kind_id`),
  CONSTRAINT `fk_rbactionnumbertype_kind` FOREIGN KEY (`kind_id`) REFERENCES `rbActionNumberKind` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'Конкретный тип номера документа в данном регионе';
''')


class ActionNumbersKindCommonData(DBToolBaseNode):
    name = 'rimis-1820.common.kind_data'
    depends = ['rimis-1820.type_kind_tables']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            data = [
                ('hosp_appointment', u'Направление на госпитализацию'),
            ]
            c.executemany(u'''
INSERT INTO `rbActionNumberKind` (`code`, `name`) VALUES (%s, %s);
''', data)


class ActionNumbersTypeTula(DBToolBaseNode):
    name = 'rimis-1820.tula_number_types'
    depends = ['rimis-1820.type_kind_tables', 'rimis-1820.common.kind_data']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute('SELECT id FROM rbActionNumberKind where code = "hosp_appointment" ')
            hosp_apnt_kind_id = c.fetchone()[0]
            data = [
                ('71', u'Направление на госпитализацию', hosp_apnt_kind_id),  # 71 - кладр код Тульской области
            ]
            c.executemany(u'''
INSERT INTO `rbActionNumberType` (`code`, `name`, `kind_id`) VALUES (%s, %s, %s);
''', data)


class ActionNumbersTableUpdateTypeField(DBToolBaseNode):
    name = 'rimis-1820.fix1.maintable'
    depends = ['rimis-1820.type_kind_tables']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `ActionNumbers`
CHANGE COLUMN `entity_type` `numberType_id` INT(11) NOT NULL COMMENT '{rbActionNumberType}' ,
CHANGE COLUMN `date` `date` DATE NULL DEFAULT NULL ;
''')
            c.execute('SET foreign_key_checks = 0;')
            c.execute(u'''
ALTER TABLE `ActionNumbers`
  ADD CONSTRAINT `fk_actionnumbers_type` FOREIGN KEY (`numberType_id`)
  REFERENCES `rbActionNumberType` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
''')
            c.execute('SET foreign_key_checks = 1;')


class TulaHospApntNumbersActionTriggerEdit(DBToolBaseNode):
    name = 'rimis-1820.fix1.trigger'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'DROP TRIGGER IF EXISTS onInsertAction')
            c.execute(u'''
CREATE DEFINER={0} TRIGGER `onInsertAction` AFTER INSERT ON `Action` FOR EACH ROW
BEGIN
    DECLARE apnt_postfix INT(11);
    DECLARE apnt_prefix INT(11);
    DECLARE apnt_org_code VARCHAR(50);
    DECLARE apnt_dep_code VARCHAR(50);
    DECLARE apnt_date_code VARCHAR(8);
    DECLARE apnt_number VARCHAR(191);
    DECLARE number_type_id INT(11);

    DECLARE flatCode VARCHAR(64);
    SELECT `ActionType`.`flatCode` INTO flatCode FROM `ActionType` WHERE `ActionType`.`id` = NEW.`actionType_id`;

    IF flatCode = "tula_hosp" THEN
        SELECT
            rbActionNumberType.id INTO number_type_id
        FROM rbActionNumberType
            JOIN rbActionNumberKind ON rbActionNumberType.kind_id = rbActionNumberKind.id
        WHERE rbActionNumberType.code = "71" AND rbActionNumberKind.code = "hosp_appointment" LIMIT 1;

        SELECT
            CAST(prefix as UNSIGNED), CAST(postfix as UNSIGNED)
            INTO
            apnt_prefix, apnt_postfix
        FROM ActionNumbers
        WHERE date = DATE(NEW.begDate) AND numberType_id = number_type_id
        ORDER BY prefix DESC, postfix DESC LIMIT 1 FOR UPDATE;
        IF apnt_postfix IS NULL THEN
            SET apnt_postfix = 900;
            SET apnt_prefix = 0;
        ELSE
            SET apnt_postfix = apnt_postfix + 1;
            IF apnt_postfix > 999 THEN
                SET apnt_prefix = apnt_prefix + 1;
                SET apnt_postfix = 900;
            END IF;
        END IF;

        SELECT
            o.TFOMSCode, os.TFOMSCode
            INTO
            apnt_org_code, apnt_dep_code
        FROM Action a
            JOIN Event e ON a.event_id = e.id
            JOIN Person p ON e.execPerson_id = p.id
            JOIN Organisation o ON p.org_id = o.id
            JOIN OrgStructure os ON o.id = os.organisation_id
        WHERE a.id = NEW.id
        LIMIT 1;

        SET apnt_date_code = DATE_FORMAT(NEW.begDate, "%y%m%d");

        SET apnt_number = CONCAT(
            COALESCE(apnt_org_code, '000'),
            COALESCE(apnt_dep_code, '000'),
            apnt_date_code, apnt_postfix
        );

        INSERT INTO `ActionNumbers`
            (`action_id`, `numberType_id`, `number`, `prefix`, `postfix`, `date`)
        VALUES
            (NEW.id, number_type_id, apnt_number,
             CAST(apnt_prefix as CHAR(32)),
             CAST(apnt_postfix as CHAR(32)),
             DATE(NEW.begDate));

    END IF;
END'''.format(cls.config['definer']))


class TulaHospApntNumbersActionTriggerEdit2(DBToolBaseNode):
    name = 'rimis-1820.fix2'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'DROP TRIGGER IF EXISTS onInsertAction')

            c.execute(u'''
CREATE DEFINER={0} TRIGGER `Action_BEFORE_INSERT` BEFORE INSERT ON `Action` FOR EACH ROW
BEGIN
    DECLARE apnt_dep_code VARCHAR(50);

    DECLARE flatCode VARCHAR(64);
    SELECT `ActionType`.`flatCode` INTO flatCode FROM `ActionType` WHERE `ActionType`.`id` = NEW.`actionType_id`;

    IF flatCode = "tula_hosp" THEN
        SELECT
            IF(`OrgStructure`.id IS NOT NULL, COALESCE(`OrgStructure`.TFOMScode, "000"), NULL) INTO apnt_dep_code
        FROM Action
            INNER JOIN (
                SELECT max(`Action`.id) AS action_id, `Action`.event_id AS event_id
                FROM `Action`
                    INNER JOIN (
                        SELECT max(`Action`.`begDate`) AS max_beg_date, `Event`.id AS event_id
                        FROM `Action` INNER JOIN `Event` ON `Event`.id = `Action`.event_id
                        INNER JOIN `ActionType` ON `ActionType`.id = `Action`.`actionType_id`
                        WHERE `Event`.deleted = 0 AND `Action`.deleted = 0 AND `ActionType`.`flatCode` IN ("risarFirstInspection", "risarSecondInspection", "risarPCCheckUp", "risarPuerperaCheckUp", "gynecological_visit_general_checkUp") AND `Action`.`endDate` IS NULL
                        GROUP BY `Event`.id
                    ) AS `MaxActionBegDates` ON `MaxActionBegDates`.max_beg_date = `Action`.`begDate` AND `MaxActionBegDates`.event_id = `Action`.event_id
                    INNER JOIN `ActionType` ON `Action`.actionType_id = `ActionType`.id
                WHERE `Action`.deleted = 0 AND `ActionType`.`flatCode` IN ("risarFirstInspection", "risarSecondInspection", "risarPCCheckUp", "risarPuerperaCheckUp", "gynecological_visit_general_checkUp") AND `Action`.`endDate` IS NULL
                GROUP BY `Action`.event_id
            ) AS `EventLatestCheckups` ON `EventLatestCheckups`.action_id = `Action`.id
            INNER JOIN `ActionProperty` ON `Action`.id = `ActionProperty`.action_id
            INNER JOIN `ActionPropertyType` ON `ActionPropertyType`.id = `ActionProperty`.type_id
            INNER JOIN `ActionProperty_OrgStructure` ON `ActionProperty`.id = `ActionProperty_OrgStructure`.id
            INNER JOIN `OrgStructure` ON `ActionProperty_OrgStructure`.value = `OrgStructure`.id
        WHERE Action.event_id = NEW.event_id AND `ActionPropertyType`.code = "department";
        IF (apnt_dep_code IS NULL) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Невозможно создать направление - не выбрано отделение в осмотре врача';
        END IF;

    END IF;
END'''.format(cls.config['definer']))

            c.execute(u'''
CREATE DEFINER={0} TRIGGER `Action_AFTER_INSERT` AFTER INSERT ON `Action` FOR EACH ROW
BEGIN
    DECLARE apnt_postfix INT(11);
    DECLARE apnt_prefix INT(11);
    DECLARE apnt_org_code VARCHAR(50);
    DECLARE apnt_dep_code VARCHAR(50);
    DECLARE apnt_date_code VARCHAR(8);
    DECLARE apnt_number VARCHAR(191);
    DECLARE number_type_id INT(11);

    DECLARE flatCode VARCHAR(64);
    SELECT `ActionType`.`flatCode` INTO flatCode FROM `ActionType` WHERE `ActionType`.`id` = NEW.`actionType_id`;

    IF flatCode = "tula_hosp" THEN
        SELECT
            rbActionNumberType.id INTO number_type_id
        FROM rbActionNumberType
            JOIN rbActionNumberKind ON rbActionNumberType.kind_id = rbActionNumberKind.id
        WHERE rbActionNumberType.code = "71" AND rbActionNumberKind.code = "hosp_appointment" LIMIT 1;

        SELECT
            CAST(prefix as UNSIGNED), CAST(postfix as UNSIGNED)
            INTO
            apnt_prefix, apnt_postfix
        FROM ActionNumbers
        WHERE date = DATE(NEW.begDate) AND numberType_id = number_type_id
        ORDER BY prefix DESC, postfix DESC LIMIT 1 FOR UPDATE;
        IF apnt_postfix IS NULL THEN
            SET apnt_postfix = 900;
            SET apnt_prefix = 0;
        ELSE
            SET apnt_postfix = apnt_postfix + 1;
            IF apnt_postfix > 999 THEN
                SET apnt_prefix = apnt_prefix + 1;
                SET apnt_postfix = 900;
            END IF;
        END IF;

        SELECT
            o.TFOMSCode INTO apnt_org_code
        FROM Action a
            JOIN Event e ON a.event_id = e.id
            JOIN Person p ON e.execPerson_id = p.id
            JOIN Organisation o ON p.org_id = o.id
        WHERE a.id = NEW.id;

        SELECT
            IF(`OrgStructure`.id IS NOT NULL, COALESCE(`OrgStructure`.TFOMScode, "000"), NULL) INTO apnt_dep_code
        FROM Action
            INNER JOIN (
                SELECT max(`Action`.id) AS action_id, `Action`.event_id AS event_id
                FROM `Action`
                    INNER JOIN (
                        SELECT max(`Action`.`begDate`) AS max_beg_date, `Event`.id AS event_id
                        FROM `Action` INNER JOIN `Event` ON `Event`.id = `Action`.event_id
                        INNER JOIN `ActionType` ON `ActionType`.id = `Action`.`actionType_id`
                        WHERE `Event`.deleted = 0 AND `Action`.deleted = 0 AND `ActionType`.`flatCode` IN ("risarFirstInspection", "risarSecondInspection", "risarPCCheckUp", "risarPuerperaCheckUp", "gynecological_visit_general_checkUp") AND `Action`.`endDate` IS NULL
                        GROUP BY `Event`.id
                    ) AS `MaxActionBegDates` ON `MaxActionBegDates`.max_beg_date = `Action`.`begDate` AND `MaxActionBegDates`.event_id = `Action`.event_id
                    INNER JOIN `ActionType` ON `Action`.actionType_id = `ActionType`.id
                WHERE `Action`.deleted = 0 AND `ActionType`.`flatCode` IN ("risarFirstInspection", "risarSecondInspection", "risarPCCheckUp", "risarPuerperaCheckUp", "gynecological_visit_general_checkUp") AND `Action`.`endDate` IS NULL
                GROUP BY `Action`.event_id
            ) AS `EventLatestCheckups` ON `EventLatestCheckups`.action_id = `Action`.id
            INNER JOIN `ActionProperty` ON `Action`.id = `ActionProperty`.action_id
            INNER JOIN `ActionPropertyType` ON `ActionPropertyType`.id = `ActionProperty`.type_id
            INNER JOIN `ActionProperty_OrgStructure` ON `ActionProperty`.id = `ActionProperty_OrgStructure`.id
            INNER JOIN `OrgStructure` ON `ActionProperty_OrgStructure`.value = `OrgStructure`.id
        WHERE Action.event_id = NEW.event_id AND `ActionPropertyType`.code = "department";
        IF (apnt_dep_code IS NULL) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Невозможно создать направление - не выбрано отделение в осмотре врача';
        END IF;

        SET apnt_date_code = DATE_FORMAT(NEW.begDate, "%y%m%d");

        SET apnt_number = CONCAT(
            COALESCE(apnt_org_code, '000'),
            COALESCE(apnt_dep_code, '000'),
            apnt_date_code, apnt_postfix
        );

        INSERT INTO `ActionNumbers`
            (`action_id`, `numberType_id`, `number`, `prefix`, `postfix`, `date`)
        VALUES
            (NEW.id, number_type_id, apnt_number,
             CAST(apnt_prefix as CHAR(32)),
             CAST(apnt_postfix as CHAR(32)),
             DATE(NEW.begDate));

    END IF;
END'''.format(cls.config['definer']))
