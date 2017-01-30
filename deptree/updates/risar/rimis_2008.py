# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class ReserveTypeChanges(DBToolBaseNode):
    name = 'rimis-2008'
    depends = ['rimis-2008.rb_create', 'rimis-2008.add_fields']


class rbReserveTypeCreate(DBToolBaseNode):
    name = 'rimis-2008.rb_create'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u"""
CREATE TABLE `rbReserveType` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(8) NOT NULL,
  `name` VARCHAR(64) NOT NULL,
  `color` VARCHAR(16) NOT NULL,
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'Отметка удаления записи',
  `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'Тип резерва';
""")


class ScheduleFieldsAdd(DBToolBaseNode):
    name = 'rimis-2008.add_fields'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u"""
ALTER TABLE `Schedule`
	ADD COLUMN `appointment_permitted` TINYINT(4) NOT NULL DEFAULT '1' COMMENT 'Разрешена запись на прием' AFTER `deleted`;
""")
            c.execute(u"""
ALTER TABLE `Schedule`
	ADD COLUMN `reserve_type_id` INT(11) NULL DEFAULT NULL AFTER `finance_id`;
""")
            c.execute(u'''
ALTER TABLE `Schedule`
	ADD CONSTRAINT `fk_schedule_reserve_type` FOREIGN KEY (`reserve_type_id`) REFERENCES `rbReserveType` (`id`) ON UPDATE NO ACTION;
''')
