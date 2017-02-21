# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class TTJ_Client_to_Event(DBToolBaseNode):
    name = 'tmis-1421'
    depends = ['tmis-1421.add_client1', 'tmis-1421.migrate_clients',
               'tmis-1421.nullify_columns']


class TTJ_AddColumnClientId(DBToolBaseNode):
    name = 'tmis-1421.add_client1'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''ALTER TABLE `TakenTissueJournal`
ADD COLUMN `event_id` INT(11) NULL DEFAULT NULL COMMENT '{Event}' AFTER `id`;
''')
            c.execute(u'''
ALTER TABLE `TakenTissueJournal`
  ADD CONSTRAINT `fk_ttj_event` FOREIGN KEY (`event_id`)
  REFERENCES `Event` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
''')


class TTJ_MigrateClientColumn(DBToolBaseNode):
    name = 'tmis-1421.migrate_clients'
    depends = ['tmis-1421.add_client1']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''UPDATE
TakenTissueJournal ttj JOIN Event e ON ttj.externalId = e.externalId AND ttj.client_id = e.client_id
SET ttj.event_id = e.id
''')


class TTJ_DropClientExternalIdColumns(DBToolBaseNode):
    name = 'tmis-1421.nullify_columns'
    depends = ['tmis-1421.migrate_clients']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `TakenTissueJournal`
DROP FOREIGN KEY `takentissuejournal_ibfk_1`;
''')
            c.execute(u'''
ALTER TABLE `TakenTissueJournal`
CHANGE COLUMN `client_id` `client_id` INT(11) NULL COMMENT 'Пациент предоставивший образец {Client} [не используется]',
CHANGE COLUMN `externalId` `externalId` VARCHAR(30) NULL COMMENT 'Внешний идентификатор [не используется]' ;''')
            c.execute(u'''
ALTER TABLE `TakenTissueJournal`
ADD CONSTRAINT `takentissuejournal_ibfk_1`
  FOREIGN KEY (`client_id`)
  REFERENCES `Client` (`id`)
  ON DELETE CASCADE;
''')
