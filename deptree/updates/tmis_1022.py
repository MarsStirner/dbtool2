# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

__author__ = 'viruzzz-kun'

logger = logging.getLogger('dbtool')


class AlterTakenTissueJournal(DBToolBaseNode):
    name = 'tmis-1022.1'
    depends = []

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            logger.info(u'Меняем таблицу TakenTissueJournal')
            c.execute(u'''
ALTER TABLE `TakenTissueJournal`
    ALTER `datetimeTaken` DROP DEFAULT''')
            c.execute(u'''
ALTER TABLE `TakenTissueJournal`
    ADD COLUMN `datetimePlanned` DATETIME NOT NULL COMMENT 'Датавремя забора (запланированная)' AFTER `unit_id`,
    CHANGE COLUMN `datetimeTaken` `datetimeTaken` DATETIME NULL DEFAULT NULL COMMENT 'Датавремя забора (факт)' AFTER `datetimePlanned`
''')


class DefaultsTakenTissueJournal(DBToolBaseNode):
    name = 'tmis-1022.2'
    depends = ['tmis-1022.1']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            logger.info(u'Заполняем значения TakenTissueJournal.datetimePlanned разумными умолчаниями')
            c.execute(u'''
UPDATE `TakenTissueJournal`
SET `TakenTissueJournal`.`datetimePlanned` = `TakenTissueJournal`.`datetimeTaken`
''')
            c.execute(u'''
UPDATE `TakenTissueJournal`, `Action`, `Action_TakenTissueJournal`
SET `TakenTissueJournal`.`datetimePlanned` = `Action`.`plannedEndDate`
WHERE
  (`TakenTissueJournal`.`id` = `Action_TakenTissueJournal`.`takenTissueJournal_id` AND `Action`.`id` = `Action_TakenTissueJournal`.action_id)
  OR
  (`TakenTissueJournal`.`id` = `Action`.`takenTissueJournal_id`)
''')
#             logger.info(u'Заполняем значения TakenTissueJournal.datetimeTaken NULL\'ами для ещё не взятых БМ')
#             c.execute(u'''
# UPDATE `TakenTissueJournal`
# SET `TakenTissueJournal`.`datetimeTaken` = NULL
# WHERE `TakenTissueJournal`.`status` IN (0, 1)
# ''')


class TMIS_1022(DBToolBaseNode):
    name = 'tmis-1022'
    depends = ['tmis-1022.1', 'tmis-1022.2']
