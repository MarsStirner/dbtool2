# coding: utf-8

from deptree. internals.base import DBToolBaseNode


class EventMeasureCancelReason(DBToolBaseNode):
    name = 'rimis-1659'
    depends = ['rimis-1659.1', 'rimis-1659.2']


class CreaterbMeasureCancelReason(DBToolBaseNode):
    name = 'rimis-1659.1'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `rbMeasureCancelReason` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(16) NOT NULL,
  `name` VARCHAR(64) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'Причина отказа от мероприятия';
''')

            data = [
                ('01', u'Мероприятие выполняется в рамках амбулаторного наблюдения'),
                ('02', u'Отказ пациентки от выполнения мероприятия'),
            ]
            c.executemany(u'''
INSERT INTO `rbMeasureCancelReason` (`code`, `name`) VALUES (%s, %s);
''', data)


class EventMeasureCancelReasonAddField(DBToolBaseNode):
    name = 'rimis-1659.2'
    depends = ['rimis-1659.1']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `EventMeasure`
ADD COLUMN `cancelReason_id` INT(11) NULL DEFAULT NULL COMMENT '{rbMeasureCancelReason}' AFTER `measure_id`,
ADD INDEX `fk_eventmeasure_cancelreason_idx` (`cancelReason_id` ASC);
''')

            c.execute(u'''
ALTER TABLE `EventMeasure`
ADD CONSTRAINT `fk_eventmeasure_cancelreason`
  FOREIGN KEY (`cancelReason_id`)
  REFERENCES `rbMeasureCancelReason` (`id`)
  ON DELETE RESTRICT
  ON UPDATE CASCADE;
''')
