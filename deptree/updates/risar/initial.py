# coding: utf-8

from deptree. internals.base import DBToolBaseNode


# ignore: RIMIS-650; RIMIS-406; RIMIS-863; RIMIS-646; RIMIS-992; RMIS-822; RIMIS-1095
# process: RIMIS-883; RIMIS-795; RIMIS-643; RIMIS-814; RIMIS-980; RIMIS-945;
# RIMIS-823; RIMIS-1040; RIMIS-965; RIMIS-885; RIMIS-1023; RIMIS-797; RIMIS-1039+-

# not processed: TMIS-943; TMIS-1018; TMIS-1066; TMIS-936; TMIS-941; TMIS-895;
# TMIS-1035; TMIS-900; TMIS-853; TMIS-882; TMIS-630


class InitialRisarUpdate(DBToolBaseNode):
    name = 'risar_init.0'
    depends = [
        'rimis-1023', 'rimis-945', 'rimis-795.1', 'rimis-643', 'rimis-814',
        'rimis-980', 'rimis-795.2', 'rimis-797.3', 'rimis-1040', 'rimis-965',
        'rimis-885'
    ]


class PrevPregChildrenCreate(DBToolBaseNode):
    name = 'rimis-883'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `RisarPreviousPregnancy_Children` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_id` int(11) NOT NULL COMMENT '{Action}',
  `date` date DEFAULT NULL COMMENT 'Дата рождения или смерти',
  `time` time DEFAULT NULL COMMENT 'Время рождения или смерти',
  `sex` tinyint(1) DEFAULT NULL COMMENT 'Пол',
  `weight` double DEFAULT NULL COMMENT 'Масса',
  `length` double DEFAULT NULL COMMENT 'Длина',
  `maturity_rate_code` varchar(250) DEFAULT NULL COMMENT 'Степень доношенности ExtRb{rbRisarMaturity_Rate}',
  `apgar_score_1` int(11) DEFAULT NULL COMMENT 'Оценка по Апгар на 1 минуту',
  `apgar_score_5` int(11) DEFAULT NULL COMMENT 'Оценка по Апгар на 5 минуту',
  `apgar_score_10` int(11) DEFAULT NULL COMMENT 'Оценка по Апгар на 10 минуту',
  `alive` tinyint(1) DEFAULT NULL COMMENT 'Живой',
  `death_reason` varchar(50) DEFAULT NULL COMMENT 'Причина смерти',
  `died_at_code` varchar(250) DEFAULT NULL COMMENT 'Умер в срок ExtRb{rbRisarDiedAt}',
  `abnormal_development` tinyint(1) DEFAULT NULL COMMENT 'Аномалии развития',
  `neurological_disorders` tinyint(1) DEFAULT NULL COMMENT 'Неврологические нарушения',
  PRIMARY KEY (`id`),
  KEY `fk_RisarPreviousPregnancy_Children_Action_idx` (`action_id`),
  CONSTRAINT `fk_RisarPreviousPregnancy_Children_Action` FOREIGN KEY (`action_id`) REFERENCES `Action` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
''')


class PrevPregChildrenDeathReasonLength(DBToolBaseNode):
    name = 'rimis-1023'
    depends = ['rimis-883']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `RisarPreviousPregnancy_Children`
CHANGE COLUMN `death_reason` `death_reason` VARCHAR(1024) NULL DEFAULT NULL COMMENT 'Причина смерти' ;
''')


class EpicrisisChildrenCreate(DBToolBaseNode):
    name = 'rimis-945'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `RisarEpicrisis_Children` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `action_id` INT(11) NOT NULL COMMENT '{Action}',
    `date` DATE NULL DEFAULT NULL COMMENT 'Дата рождения или смерти',
    `time` TIME NULL DEFAULT NULL COMMENT 'Время рождения или смерти',
    `sex` TINYINT(1) NULL DEFAULT NULL COMMENT 'Пол',
    `weight` DOUBLE NULL DEFAULT NULL COMMENT 'Масса',
    `length` DOUBLE NULL DEFAULT NULL COMMENT 'Длина',
    `maturity_rate_code` VARCHAR(250) NULL DEFAULT NULL COMMENT 'Степень доношенности ExtRb{rbRisarMaturity_Rate}',
    `apgar_score_1` INT(11) NULL DEFAULT NULL COMMENT 'Оценка по Апгар на 1 минуту',
    `apgar_score_5` INT(11) NULL DEFAULT NULL COMMENT 'Оценка по Апгар на 5 минуту',
    `apgar_score_10` INT(11) NULL DEFAULT NULL COMMENT 'Оценка по Апгар на 10 минуту',
    `alive` TINYINT(1) NULL DEFAULT NULL COMMENT 'Живой',
    `death_reason` VARCHAR(50) NULL DEFAULT NULL COMMENT 'Причина смерти',
    PRIMARY KEY (`id`),
    INDEX `fk_RisarEpicrisis_Children_Action_idx` (`action_id`),
    CONSTRAINT `fk_RisarEpicrisis_Children_Action` FOREIGN KEY (`action_id`) REFERENCES `Action` (`id`) ON UPDATE CASCADE ON DELETE CASCADE
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB;''')

            c.execute(u'''
CREATE TABLE `RisarEpicrisis_Children_diseases` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `newborn_id` INT(11) NOT NULL COMMENT '{RisarEpicrisis_Children}',
    `mkb_id` INT(11) NOT NULL COMMENT '{MKB}',
    PRIMARY KEY (`id`),
    INDEX `newborn_id` (`newborn_id`),
    INDEX `FK_mkb_id_MKB` (`mkb_id`),
    CONSTRAINT `FK_mkb_id_MKB` FOREIGN KEY (`mkb_id`) REFERENCES `MKB` (`id`),
    CONSTRAINT `FK_newborn_id_RisarEpicrisis_Children` FOREIGN KEY (`newborn_id`) REFERENCES `RisarEpicrisis_Children` (`id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB;''')


class EpicrisisChildDeathCreate(DBToolBaseNode):
    name = 'rimis-795.1'
    depends = ['rimis-945']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `RisarEpicrisis_Children_death_reasons` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `newborn_id` INT(11) NOT NULL COMMENT '{RisarEpicrisis_Children}',
  `mkb_id` INT(11) NOT NULL COMMENT '{MKB}',
  PRIMARY KEY (`id`),
  INDEX `newborn_id` (`newborn_id`),
  INDEX `FK_mkb_id_MKB` (`mkb_id`),
  CONSTRAINT `RisarEpicrisis_Children_death_reasons_ibfk_1` FOREIGN KEY (`mkb_id`) REFERENCES `MKB` (`id`),
  CONSTRAINT `RisarEpicrisis_Children_death_reasons_ibfk_2` FOREIGN KEY (`newborn_id`) REFERENCES `RisarEpicrisis_Children` (`id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB;''')

            c.execute(u'''
ALTER TABLE `RisarEpicrisis_Children`
  DROP COLUMN `death_reason`;
''')

            c.execute(u'''
ALTER TABLE `RisarEpicrisis_Children`
  ADD COLUMN `death_reasons` VARCHAR(50) NULL COMMENT 'Причина смерти (временное поле)' AFTER `alive`;
''')

            c.execute(u'''
ALTER TABLE `RisarEpicrisis_Children_diseases`
  DROP FOREIGN KEY `FK_newborn_id_RisarEpicrisis_Children`;
''')

            c.execute(u'''
ALTER TABLE `RisarEpicrisis_Children_diseases`
  ADD CONSTRAINT `FK_newborn_id_RisarEpicrisis_Children` FOREIGN KEY (`newborn_id`) REFERENCES `RisarEpicrisis_Children` (`id`)
  ON DELETE CASCADE;
''')

            c.execute(u'''
ALTER TABLE `RisarEpicrisis_Children_death_reasons`
    DROP FOREIGN KEY `RisarEpicrisis_Children_death_reasons_ibfk_2`;
''')

            c.execute(u'''
ALTER TABLE `RisarEpicrisis_Children_death_reasons`
  ADD CONSTRAINT `RisarEpicrisis_Children_death_reasons_ibfk_2` FOREIGN KEY (`newborn_id`) REFERENCES `RisarEpicrisis_Children` (`id`)
  ON DELETE CASCADE;
''')


class UserMeasuresSupport(DBToolBaseNode):
    name = 'rimis-980'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `EventMeasure`
  ALTER `schemeMeasure_id` DROP DEFAULT;
''')

        c.execute(u'''
ALTER TABLE `EventMeasure`
  CHANGE COLUMN `schemeMeasure_id` `schemeMeasure_id` INT(11) NULL COMMENT '{ExpertSchemeMeasure}' AFTER `event_id`,
  ADD COLUMN `measure_id` INT NULL COMMENT '{Measure}' AFTER `action_id`,
  ADD INDEX `fk_measure_idx` (`measure_id`),
  ADD CONSTRAINT `fk_eventmeasure_measure` FOREIGN KEY (`measure_id`) REFERENCES `Measure` (`id`) ON UPDATE CASCADE;
''')

        c.execute(u'''
DELIMITER $$
CREATE DEFINER={0} TRIGGER `beforeInsertEventMeasure` BEFORE INSERT ON `EventMeasure`
FOR EACH ROW
BEGIN
    IF NOT (NEW.schemeMeasure_id > 0 OR NEW.measure_id > 0) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'EventMeasure check constraint on (schemeMeasure_id, measure_id) failed', MYSQL_ERRNO = ER_SIGNAL_EXCEPTION;
    END IF;
END$$
DELIMITER ;
'''.format(cls.config['definer']))

        c.execute(u'''
DELIMITER $$
CREATE DEFINER={0} TRIGGER `beforeUpdateEventMeasure` BEFORE UPDATE ON `EventMeasure`
FOR EACH ROW
BEGIN
    IF NOT (NEW.schemeMeasure_id > 0 OR NEW.measure_id > 0) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'EventMeasure check constraint on (schemeMeasure_id, measure_id) failed', MYSQL_ERRNO = ER_SIGNAL_EXCEPTION;
    END IF;
END$$
DELIMITER ;
'''.format(cls.config['definer']))


class FetusStateCreate(DBToolBaseNode):
    name = 'rimis-823'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `FetusState` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `action_id` INT(11) NOT NULL COMMENT 'Описание действия {Action}',
    `position_code` VARCHAR(250) NULL DEFAULT NULL COMMENT 'Положение {rbRisarFetus_Position}',
    `position_2_code` VARCHAR(250) NULL DEFAULT NULL COMMENT 'Позиция {rbRisarFetus_Position_2}',
    `type_code` VARCHAR(250) NULL DEFAULT NULL COMMENT 'Вид {rbRisarFetus_Type}',
    `presenting_part_code` VARCHAR(250) NULL DEFAULT NULL COMMENT 'Предлежащая часть {rbRisarPresenting_Part}',
    `heartbeat_code` VARCHAR(250) NULL DEFAULT NULL COMMENT 'Сердцебиение {rbRisarFetus_Heartbeat}',
    `heart_rate` INT(11) NULL DEFAULT NULL COMMENT 'ЧСС, уд/мин',
    `delay_code` VARCHAR(250) NULL DEFAULT NULL COMMENT 'Задержка в развитии {rbRisarFetus_Delay}',
    `ktg_input` TINYINT(1) NOT NULL DEFAULT '0' COMMENT 'Ввод данных КТГ',
    `basal_code` VARCHAR(250) NULL DEFAULT NULL COMMENT 'Базальный ритм {rbRisarBasal}',
    `variability_range_code` VARCHAR(250) NULL DEFAULT NULL COMMENT 'Вариабельность (амплитуда) {rbRisarVariabilityRange}',
    `frequency_per_minute_code` VARCHAR(250) NULL DEFAULT NULL COMMENT 'Вариабельность (частота в минуту) {rbRisarFrequencyPerMinute}',
    `acceleration_code` VARCHAR(250) NULL DEFAULT NULL COMMENT 'Акселерации за 30 минут {rbRisarAcceleration}',
    `deceleration_code` VARCHAR(250) NULL DEFAULT NULL COMMENT 'Децелерации за 30 минут {rbRisarDeceleration}',
    PRIMARY KEY (`id`),
    INDEX `action_id` (`action_id`),
    INDEX `position_code` (`position_code`),
    INDEX `position_2_code` (`position_2_code`),
    INDEX `type_code` (`type_code`),
    INDEX `presenting_part_code` (`presenting_part_code`),
    INDEX `heartbeat_code` (`heartbeat_code`),
    INDEX `delay_code` (`delay_code`),
    INDEX `basal_code` (`basal_code`),
    INDEX `variability_range_code` (`variability_range_code`),
    INDEX `frequency_per_minute_code` (`frequency_per_minute_code`),
    INDEX `acceleration_code` (`acceleration_code`),
    INDEX `deceleration_code` (`deceleration_code`)
)
COMMENT='Состояние плода в разделе Осмотры'
COLLATE='utf8_general_ci'
ENGINE=InnoDB;
''')


class FetusStateMetaFieldsAndIndexes(DBToolBaseNode):
    name = 'rimis-797.1'
    depends = ['rimis-823']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `FetusState`
    ADD COLUMN `createDatetime` DATETIME NOT NULL COMMENT 'Дата создания записи' AFTER `deceleration_code`,
    ADD COLUMN `createPerson_id` INT(11) NULL DEFAULT NULL COMMENT 'Автор записи {Person}' AFTER `createDatetime`,
    ADD COLUMN `modifyDatetime` DATETIME NOT NULL COMMENT 'Дата изменения записи' AFTER `createPerson_id`,
    ADD COLUMN `modifyPerson_id` INT(11) NULL DEFAULT NULL COMMENT 'Автор изменения записи {Person}' AFTER `modifyDatetime`,
    ADD COLUMN `deleted` TINYINT(1) NOT NULL DEFAULT '0' COMMENT 'Отметка удаления записи' AFTER `modifyPerson_id`;
''')

            c.execute(u'''
ALTER TABLE `FetusState`
    DROP INDEX `position_code`,
    DROP INDEX `position_2_code`,
    DROP INDEX `type_code`,
    DROP INDEX `presenting_part_code`,
    DROP INDEX `heartbeat_code`,
    DROP INDEX `delay_code`,
    DROP INDEX `basal_code`,
    DROP INDEX `variability_range_code`,
    DROP INDEX `frequency_per_minute_code`,
    DROP INDEX `acceleration_code`,
    DROP INDEX `deceleration_code`;
''')


class FetusStateHeartbeatsCreateAndRenames(DBToolBaseNode):
    name = 'rimis-797.2'
    depends = ['rimis-797.1']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `FetusState_heartbeats` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `fetus_state_id` INT(11) NOT NULL DEFAULT '0',
    `heartbeat_code` VARCHAR(250) NOT NULL,
    INDEX `fetus_state_id` (`fetus_state_id`),
    PRIMARY KEY (`id`),
    CONSTRAINT `FK1_FetusState` FOREIGN KEY (`fetus_state_id`) REFERENCES `FetusState` (`id`)
)
COMMENT='Сердцебиение плода'
COLLATE='utf8_general_ci'
ENGINE=InnoDB;
''')

            c.execute(u'''
ALTER TABLE `FetusState`
    DROP COLUMN `heartbeat_code`;
''')

            c.execute(u'''
ALTER TABLE `FetusState_heartbeats`
    ALTER `heartbeat_code` DROP DEFAULT;
''')

            c.execute(u'''
ALTER TABLE `FetusState_heartbeats`
    CHANGE COLUMN `heartbeat_code` `heartbeat_code` VARCHAR(250) NOT NULL COMMENT 'Сердцебиение {rbRisarFetus_Heartbeat}' AFTER `fetus_state_id`;
''')

            c.execute(u'''
RENAME TABLE `FetusState_heartbeats` TO `RisarFetusState_heartbeats`;
''')

            c.execute(u'''
RENAME TABLE `FetusState` TO `RisarFetusState`;
''')


class FetusStateFK1Change(DBToolBaseNode):
    name = 'rimis-795.2'
    depends = ['rimis-797.2']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `RisarFetusState_heartbeats`
  DROP FOREIGN KEY `FK1_FetusState`;
''')

            c.execute(u'''
ALTER TABLE `RisarFetusState_heartbeats`
  ADD CONSTRAINT `FK1_FetusState` FOREIGN KEY (`fetus_state_id`) REFERENCES `RisarFetusState` (`id`) ON DELETE CASCADE;
''')


class ActionIdentificationCreate(DBToolBaseNode):
    name = 'rimis-797.3'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `ActionIdentification` (
    `id` INT NOT NULL,
    `action_id` INT NOT NULL COMMENT 'Документ',
    `external_id` VARCHAR(50) NOT NULL COMMENT 'ID документа во внешней системе',
    `external_system_id` INT NOT NULL COMMENT 'ID внешней системы {rbAccountingSystem}',
    PRIMARY KEY (`id`),
    INDEX `action_id` (`action_id`),
    INDEX `external_id` (`external_id`),
    CONSTRAINT `action_id_FK` FOREIGN KEY (`action_id`) REFERENCES `Action` (`id`),
    CONSTRAINT `external_system_id_FK` FOREIGN KEY (`external_system_id`) REFERENCES `rbAccountingSystem` (`id`)
)
COMMENT='Учетные номера в различных системах'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
''')

            c.execute(u'''
ALTER TABLE `ActionIdentification`
    ADD UNIQUE INDEX `action_id_external_id_external_system_id` (`action_id`, `external_id`, `external_system_id`);
''')

            c.execute(u'''
ALTER TABLE `ActionIdentification`
    CHANGE COLUMN `id` `id` INT(11) NOT NULL AUTO_INCREMENT FIRST;
''')


class RsrPrintTemplatemetaCreate(DBToolBaseNode):
    name = 'rimis-1022'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `rbRisarPrintTemplateMeta` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`template_uri` VARCHAR(255) NOT NULL,
	`type` ENUM('Integer','Float','String','Boolean','Date','Time','List','Multilist','RefBook','Organisation','OrgStructure','Person','Service','SpecialVariable','MKB','Area') NOT NULL,
	`name` VARCHAR(128) NOT NULL,
	`title` TINYTEXT NOT NULL,
	`description` TINYTEXT NOT NULL,
	`arguments` MEDIUMTEXT NULL,
	`defaultValue` TEXT NULL,
	PRIMARY KEY (`id`),
	UNIQUE INDEX `template_uri_name` (`template_uri`, `name`)
)
COMMENT='Метаданные шаблона печати'
COLLATE='utf8_general_ci'
ENGINE=InnoDB;
''')


class RsrPrintTemplatemetaChangeTypeEnum(DBToolBaseNode):
    name = 'rimis-1039'
    depends = ['rimis-1022']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `rbRisarPrintTemplateMeta`
  CHANGE COLUMN `type` `type` ENUM('Integer','Float','String','Boolean','Date','Time','List','Multilist','RefBook','Organisation',
  'OrgStructure','Person','Service','SpecialVariable','MKB','Area','MultiRefBook','MultiOrganisation','MultiOrgStructure',
  'MultiPerson','MultiService','MultiMKB','MultiArea') NOT NULL AFTER `template_uri`;
''')


class RsrPrintTemplatemetaChangeRequired(DBToolBaseNode):
    name = 'rimis-1040'
    depends = ['rimis-1039']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `rbRisarPrintTemplateMeta`
  CHANGE COLUMN `description` `description` TINYTEXT NULL AFTER `title`,
  ADD COLUMN `required`  TINYINT(1) NOT NULL AFTER `defaultValue`;
''')


class AddEventManager(DBToolBaseNode):
    name = 'rimis-965'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `Event`
  ADD COLUMN `manager_id` INT(11) NULL DEFAULT NULL COMMENT 'Заведующий {Person}' AFTER `assistant_id`;
''')


class CreateConciliumTables(DBToolBaseNode):
    name = 'rimis-885'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `RisarConcilium` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `createDatetime` datetime NOT NULL,
  `createPerson_id` int(11) DEFAULT NULL,
  `modifyDatetime` datetime NOT NULL,
  `modifyPerson_id` int(11) DEFAULT NULL,
  `event_id` int(11) NOT NULL COMMENT '{Event}',
  `date` date NOT NULL,
  `hospital_id` int(11) NOT NULL COMMENT 'ЛПУ консилиума {Organisation}',
  `doctor_id` int(11) NOT NULL COMMENT 'Лечащий врач {Person}',
  `patient_presence` tinyint(1) DEFAULT NULL COMMENT 'Присутствие пациента на консилиуме (0-нет, 1-да)',
  `mkb_id` int(11) NOT NULL COMMENT 'Основной диагноз {MKB}',
  `reason` varchar(1024) NOT NULL DEFAULT '' COMMENT 'Причина проведения консилиума',
  `patient_condition` longtext COMMENT 'Состояние пациента',
  `decision` longtext NOT NULL COMMENT 'Заключение консилиума',
  PRIMARY KEY (`id`),
  KEY `fk_risarconcilium_hospital_idx` (`hospital_id`),
  KEY `fk_risarconcilium_doctor_idx` (`doctor_id`),
  KEY `fk_risarconcilium_mkb_idx` (`mkb_id`),
  KEY `fk_risarconcilium_event_idx` (`event_id`),
  CONSTRAINT `fk_risarconcilium_doctor` FOREIGN KEY (`doctor_id`) REFERENCES `Person` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_risarconcilium_event` FOREIGN KEY (`event_id`) REFERENCES `Event` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_risarconcilium_hospital` FOREIGN KEY (`hospital_id`) REFERENCES `Organisation` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_risarconcilium_mkb` FOREIGN KEY (`mkb_id`) REFERENCES `MKB` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Консилиум';
''')

            c.execute(u'''
CREATE TABLE `RisarConcilium_Members` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `concilium_id` int(11) NOT NULL COMMENT '{RisarConcilium}',
  `person_id` int(11) NOT NULL COMMENT '{Person}',
  `opinion` longtext COMMENT 'особое мнение врача',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unq_person_concilium_idx` (`concilium_id`,`person_id`),
  KEY `fk_risarconcilium_members_person_idx` (`person_id`),
  CONSTRAINT `fk_risarconcilium_members_person` FOREIGN KEY (`person_id`) REFERENCES `Person` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_risarconcilium_members_risarconcilium` FOREIGN KEY (`concilium_id`) REFERENCES `RisarConcilium` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Состав консилиума';
''')

            c.execute(u'''
CREATE TABLE `RisarConcilium_Identification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `concilium_id` int(11) NOT NULL COMMENT '{RisarConcilium}',
  `external_id` varchar(250) NOT NULL COMMENT 'Идентификатор во внешней системе',
  `external_system_id` int(11) NOT NULL COMMENT '{rbAccountingSystem}',
  PRIMARY KEY (`id`),
  KEY `fk_risarconcilium_identification_concilium_idx` (`concilium_id`),
  KEY `fk_risarconcilium_identification_rbaccountingsystem_idx` (`external_system_id`),
  CONSTRAINT `fk_risarconcilium_identification_concilium` FOREIGN KEY (`concilium_id`) REFERENCES `RisarConcilium` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_risarconcilium_identification_rbaccountingsystem` FOREIGN KEY (`external_system_id`) REFERENCES `rbAccountingSystem` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Идентификаторы во внешних системах для консилиума';
''')
