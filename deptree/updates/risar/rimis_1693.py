# coding: utf-8

from deptree.internals.base import DBToolBaseNode



class CreateTableEventPersonsControl(DBToolBaseNode):
    name = 'rimis-1693'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `EventPersonsControl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `createDatetime` datetime NOT NULL COMMENT 'Дата создания записи',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'Отметка удаления записи',
  `event_id` int(11) NOT NULL COMMENT 'Event {Event}',
  `person_id` int(11) NOT NULL COMMENT 'Person {Person}',
  `begDate` datetime NOT NULL COMMENT 'Starting responsibility date',
  `endDate` datetime DEFAULT NULL COMMENT 'Disclaimer date',
  PRIMARY KEY (`id`),
  KEY `fk_eventpersonscontrol_event_idx` (`event_id`),
  KEY `fk_eventpersonscontrol_person_idx` (`person_id`),
  CONSTRAINT `fk_eventpersonscontrol_event` FOREIGN KEY (`event_id`) REFERENCES `Event` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_eventpersonscontrol_person` FOREIGN KEY (`person_id`) REFERENCES `Person` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Обращения, взятые на контроль';
''')
