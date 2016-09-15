# -*- coding: utf-8 -*-

import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class Rimis1382(DBToolBaseNode):
    name = 'rimis-1382'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            logger.info(u"\t >>> Добавляем поле nationality_code в таблицу Client")
            c.execute(u"""ALTER TABLE `hospital1_risar`.`Client`
      ADD COLUMN `nationality_code` VARCHAR(255) NULL   COMMENT 'Национальность{rbOKIN_Nationality}' AFTER `sex`;""")
