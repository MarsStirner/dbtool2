# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')

query_add_autoclose_column = u'''
ALTER TABLE `ActionType` ADD COLUMN `autoclose_on_event_close` BIT NOT NULL DEFAULT b'1'
	COMMENT 'Автоматически закрывать экшены через N дней после закрытия ИБ' AFTER `hasPrescriptions`;
'''
query_set_default_autoclose_flag = u'''UPDATE `ActionType` SET `autoclose_on_event_close` = (`mnem` IN ('EXAM', 'EPI', 'JOUR', 'ORD', 'NOT', 'OTH', 'DIAG', 'THER')); '''

query_drop_autoclose_column = u'''ALTER TABLE `ActionType`	DROP COLUMN `autoclose_on_event_close`; '''


class AutoCloseActionTypeFlag(DBToolBaseNode):
    name = 'webmis-494'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            logger.info(u'''Add 'autoclose_on_event_close' column on ActionType table''')
            c.execute(query_add_autoclose_column)
            logger.info(u'''Set 'autoclose_on_event_close' ''')
            c.execute(query_set_default_autoclose_flag)


    @classmethod
    def downgrade(cls):
        with cls.connection as c:
            logger.info(u'''Drop 'autoclose_on_event_close' column on ActionType table''')
            c.execute(query_drop_autoclose_column)