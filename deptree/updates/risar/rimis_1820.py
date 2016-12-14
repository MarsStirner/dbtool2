# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class HospAppointmentsTula(DBToolBaseNode):
    name = 'rimis-1820'
    depends = ['rimis-1820.1', 'rimis-1820.2']


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
            o.TFOMScode, o.Departmentcode
            INTO
            apnt_org_code, apnt_dep_code
        FROM Action a
            JOIN Event e ON a.event_id = e.id
            JOIN Person p ON e.execPerson_id = p.id
            JOIN Organisation o ON p.org_id = o.id
        WHERE a.id = NEW.id;

        SET apnt_date_code = DATE_FORMAT(NEW.begDate, "%y%m%d");

        SET apnt_number = CONCAT(apnt_org_code, apnt_dep_code, apnt_date_code, apnt_postfix);

        INSERT INTO `ActionNumbers`
            (`action_id`, `entity_type`, `number`, `prefix`, `postfix`, `date`)
        VALUES
            (NEW.id, 'HOSP_APNT_TU', apnt_number,
             CAST(apnt_prefix as CHAR(32)),
             CAST(apnt_postfix as CHAR(32)),
             DATE(NEW.begDate));

    END IF;
END'''.format(cls.config['definer']))
