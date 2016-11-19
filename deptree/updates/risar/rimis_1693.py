# coding: utf-8

from deptree. internals.base import DBToolBaseNode



class CreateTable(DBToolBaseNode):
    name = 'rimis-1693'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `Event_under_Persons_control` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `createDatetime` datetime NOT NULL COMMENT 'Дата создания записи',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'Отметка удаления записи',
  `event_id` int(11) NOT NULL COMMENT 'Event {Event}',
  `person_id` int(11) NOT NULL COMMENT 'Person {Person}',
  `begDate` datetime NOT NULL COMMENT 'Starting responsibility date',
  `endDate` datetime DEFAULT NULL COMMENT 'Disclaimer date',
  PRIMARY KEY (`id`),
  KEY `event_id` (`event_id`),
  KEY `person_id` (`person_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='Пациентки, взятые на контроль';
''')

