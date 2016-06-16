# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import _DBToolBase, db_transactional

logger = logging.getLogger('dbtool')


# noinspection SqlResolve
class _DBToolInitDB(_DBToolBase):

    @db_transactional
    def init_db(self):
        """
        Подготавливает БД для работы с dbtool2.
        Идет создание таблицы InstalledDbUpdates.
        """
        logger.info(u'Инициализация базы данных... Создание таблицы `InstalledDbUpdates`')
        with self.connection as c:
            c.execute(u'''
CREATE TABLE IF NOT EXISTS `InstalledDbUpdates` (
    `name` VARCHAR(128) NOT NULL,
    PRIMARY KEY (`name`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB;''')
