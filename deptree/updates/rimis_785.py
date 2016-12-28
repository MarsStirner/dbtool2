# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class RIMIS785_rbRadzinskyRiskRate(DBToolBaseNode):
    name = 'rimis-785'
    depends = ['rimis-682']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''ALTER TABLE `rbRadzinskyRiskRate` ADD COLUMN `name_masc` VARCHAR(45) NULL  AFTER `value` ;''')
            c.execute(u'''UPDATE rbRadzinskyRiskRate SET name_masc = 'низкий' where code='low';''')
            c.execute(u'''UPDATE rbRadzinskyRiskRate SET name_masc = 'средний' where code='medium';''')
            c.execute(u'''UPDATE rbRadzinskyRiskRate SET name_masc = 'высокий' where code='high';''')

