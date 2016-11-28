# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class RIMIS1691addcolumns(DBToolBaseNode):
    name = 'rimis-1691'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
            ALTER TABLE `hospital1_risar`.`Event_Persons` ADD COLUMN `createDatetime` DATETIME NULL  AFTER `endDate` , ADD COLUMN `createPerson_id` INT(11) NOT NULL  AFTER `createDatetime` ;
''')

