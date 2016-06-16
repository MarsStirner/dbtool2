# -*- coding: utf-8 -*-
import logging

import MySQLdb
import re
from deptree.internals.base import _DBToolBase, db_transactional

logger = logging.getLogger('dbtool')


__author__ = 'viruzzz-kun'


# noinspection SqlResolve
class _DBToolDefinerChanger(_DBToolBase):
    def user_change_definers(self):
        logger.warning(
            u'Все DEFINER\'ы для триггеров, процедур и видов в БД %s будут заменены %s',
            self._format_db_name(),
            self.config['definer'],
        )
        if self._proceed():
            self.change_definers()
        else:
            logger.info(u'Изменение DEFINER\'ов прервано пользователем')

    @db_transactional
    def change_definers(self):
        """
        Сменяет дефайнеров в БД
        :return:
        """
        logger.info(u'Установка DEFINER\'ов в базе %s', self._format_db_name())
        current_db_name = self.config['dbname']
        new_definer = self.config['definer']

        with self.connection as c:
            logger.info(u'- Обрабатываются триггеры')
            c.execute(
                'SELECT `TRIGGER_NAME`, `DEFINER` '
                'FROM `information_schema`.`TRIGGERS` '
                'WHERE `TRIGGER_SCHEMA` = "%s"' % current_db_name)
            for name, definer in c:
                logger.info(' - - %s', name)
                definer = '`' + '`@`'.join(definer.split('@')) + '`'  # mis@% -> `mis`@`%`
                c.execute('SHOW CREATE TRIGGER %s' % name)
                create_text = c.fetchone()[2]
                create_text = create_text.replace(definer, new_definer)
                if not self.dry_run:
                    c.execute('DROP TRIGGER IF EXISTS %s' % name)
                    c.execute(create_text)

            logger.info(u'- Обрабатываются процедуры')
            if not self.dry_run:
                c.execute(
                    'UPDATE `mysql`.`proc` SET `definer` = "%s" '
                    'WHERE `db`="%s"' % (new_definer.replace('`', ''), current_db_name))

            logger.info(u'- Обрабатываются виды')
            c.execute(
                'SELECT `TABLE_NAME` '
                'FROM `information_schema`.`TABLES` '
                'WHERE `TABLE_TYPE` = "VIEW" AND `TABLE_SCHEMA` = "%s"' % current_db_name)
            wrong_views = []
            for (name, ) in c:
                try:
                    logger.info(u' - - %s', name)
                    c.execute('SHOW CREATE VIEW %s' % name)
                    create_stmt = c.fetchone()[1]
                    create_stmt = re.sub(r'`\w+`@`[\w\.%]+`', new_definer, create_stmt)
                    create_stmt = create_stmt.replace('CREATE', 'CREATE OR REPLACE')
                    if not self.dry_run:
                        c.execute(create_stmt)
                except MySQLdb.OperationalError as e:
                    # Случай, когда вьюха в теле ссылается на другую вьюху, у которой еще
                    # не поменялся дефайнер, может вызвать проблемы, если такого дефайнера
                    # нет в текущей бд. Такие случаи пропускаются
                    if '1449' in str(e):
                        wrong_views.append(name)
                    else:
                        raise
            if wrong_views:
                logger.warning(u'Возникла проблема изменения дефайнеров для следующих представлений: %s. '
                               u'Требуется ручное вмешательство.', u', '.join(wrong_views))


