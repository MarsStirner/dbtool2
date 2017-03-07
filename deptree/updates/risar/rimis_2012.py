# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class AddFetusStateField(DBToolBaseNode):
    name = 'rimis-2012'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u''' ALTER TABLE `RisarFetusState` ADD COLUMN `contigous_part_code` VARCHAR(250) NULL COMMENT 'Место нахождения предлежащей части' AFTER `presenting_part_code`;''')


