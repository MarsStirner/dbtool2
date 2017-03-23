# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class ReceivedAptOrgStructTransferRename(DBToolBaseNode):
    name = 'tmis-1410'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''UPDATE ActionType, ActionPropertyType
SET ActionPropertyType.code = %s
WHERE ActionType.id = ActionPropertyType.actionType_id AND ActionType.flatCode = %s AND
ActionPropertyType.code = %s''', ('orgStructTransfer', 'received', 'orgStructDirection'))
