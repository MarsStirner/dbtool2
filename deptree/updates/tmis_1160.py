# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class Action_TTJ_ForeignKeys(DBToolBaseNode):
    name = 'tmis-1160'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''SET foreign_key_checks = 0;''')
            c.execute(u'''
ALTER TABLE `Action_TakenTissueJournal`
ADD INDEX `fk_action_ttj_action_idx` (`action_id` ASC);
ALTER TABLE `Action_TakenTissueJournal`
ADD CONSTRAINT `fk_action_ttj_action`
  FOREIGN KEY (`action_id`)
  REFERENCES `Action` (`id`)
  ON DELETE RESTRICT
  ON UPDATE CASCADE;
''')
            c.execute(u'''
ALTER TABLE `Action_TakenTissueJournal`
ADD INDEX `fk_action_ttj_ttj_idx` (`takenTissueJournal_id` ASC);
ALTER TABLE `Action_TakenTissueJournal`
ADD CONSTRAINT `fk_action_ttj_ttj`
  FOREIGN KEY (`takenTissueJournal_id`)
  REFERENCES `TakenTissueJournal` (`id`)
  ON DELETE RESTRICT
  ON UPDATE CASCADE;
''')
            c.execute(u'''SET foreign_key_checks = 1;''')
