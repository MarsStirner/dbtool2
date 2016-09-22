# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


sql_drop_index = u'ALTER TABLE `{0}` DROP INDEX `{1}`'
sql_drop_fk = u'ALTER TABLE `{0}` DROP FOREIGN KEY `{1}`'


class FixSomeIndexesAndFKsInActionAndEvent(DBToolBaseNode):
    name = 'tmis-1245'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            # Event
            for idx in ('IDX_Event_id', 'FK_Event_Event_LocalContract', 'uuid_id',
                        'client_id', 'eventType_id'):
                try:
                    c.execute(sql_drop_index.format('Event', idx))
                except Exception, e:
                    logger.warning(u'Не был удален {0} в Event: {1}'.format(idx, unicode(e)))

            for fk in ('FK_Event_Event_LocalContract', 'Event_mesSpecification'):
                try:
                    c.execute(sql_drop_fk.format('Event', fk))
                except Exception, e:
                    logger.warning(u'Не был удален {0} в Event: {1}'.format(fk, unicode(e)))

            c.execute(u'''ALTER TABLE `Event`
ADD INDEX `fk_event_client_idx` (`client_id` ASC)''')

            c.execute(u'''ALTER TABLE `Event`
ADD CONSTRAINT `fk_event_client`
  FOREIGN KEY (`client_id`)  REFERENCES `Client` (`id`)
  ON DELETE RESTRICT ON UPDATE CASCADE''')

            c.execute(u'''ALTER TABLE `Event`
ADD INDEX `fk_event_event_type_idx` (`eventType_id` ASC)''')

            c.execute(u'''ALTER TABLE `Event`
ADD CONSTRAINT `fk_event_event_type`
  FOREIGN KEY (`eventType_id`) REFERENCES `EventType` (`id`)
  ON DELETE RESTRICT ON UPDATE CASCADE''')

            # Action
            for idx in ('IDX_Action_id', 'coord_person', 'uuid_id', 'prescription_id',
                        'finance_id', 'actionType_id', 'event_id', 'fk_action_actiontype_idx'):
                try:
                    c.execute(sql_drop_index.format('Action', idx))
                except Exception, e:
                    logger.warning(u'Не был удален {0} в Action: {1}'.format(idx, unicode(e)))

            for fk in ('fk_coord_person', 'FK_Action_ActionType_id'):
                try:
                    c.execute(sql_drop_fk.format('Action', fk))
                except Exception, e:
                    logger.warning(u'Не был удален {0} в Action: {1}'.format(fk, unicode(e)))

            c.execute(u'''ALTER TABLE `Action`
ADD INDEX `fk_action_event_idx` (`event_id` ASC)''')

            c.execute(u'''ALTER TABLE `Action`
ADD CONSTRAINT `fk_action_event`
  FOREIGN KEY (`event_id`) REFERENCES `Event` (`id`)
  ON DELETE RESTRICT ON UPDATE CASCADE''')

            c.execute(u'''ALTER TABLE `Action`
ADD INDEX `fk_action_actiontype_idx` (`actionType_id` ASC)''')

            c.execute(u'''ALTER TABLE `Action`
ADD CONSTRAINT `fk_action_actiontype`
  FOREIGN KEY (`actionType_id`) REFERENCES `ActionType` (`id`)
  ON DELETE RESTRICT ON UPDATE CASCADE''')

            c.execute(u'''ALTER TABLE `Action`
ADD INDEX `fk_action_beg_date_idx` (`begDate` ASC)''')

            c.execute(u'''ALTER TABLE `Action`
ADD INDEX `fk_action_ped_idx` (`plannedEndDate` ASC)''')
