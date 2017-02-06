# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class Rimis1981(DBToolBaseNode):
    name = 'rimis-1981'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''ALTER TABLE `RisarFetusState` ADD COLUMN `stv_evaluation` DOUBLE NULL DEFAULT NULL COMMENT 'оценка по STV'  AFTER `fisher_ktg_rate_id`;''')
