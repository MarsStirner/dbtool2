# -*- coding: utf-8 -*-
import logging

import MySQLdb
from deptree.internals.base import _DBToolBase, DBToolBaseNode, db_transactional

logger = logging.getLogger('dbtool')


__author__ = 'viruzzz-kun'


# noinspection SqlResolve
class _DBToolDowngrader(_DBToolBase):
    @db_transactional
    def _make_downgrades(self, sequence):
        """
        Выполняет удаление апгрейдов
        :type sequence: list
        :param sequence: последовательность даунгрейдов
        :return:
        """
        with self.connection as cursor:
            for name in sequence:
                node = DBToolBaseNode.get(name)
                logger.info(u'Откат изменения %s', name)
                if self.dry_run:
                    continue
                try:
                    if hasattr(node, 'downgrade'):
                        node.downgrade()
                except MySQLdb.ProgrammingError, e:
                    raise
                else:
                    cursor.execute('DELETE FROM InstalledDbUpdates WHERE `name` = %s', (name, ))

    def _get_real_targets(self, targets):
        return set(self.installed_updates) & set(targets)

    def _get_not_really_targets(self, targets):
        return set(targets) - set(self.installed_updates)

    def perform_downgrades(self, targets):
        """
        "Разговаривающий" с пользователем "трамплин"
        :param targets:
        :return:
        """
        real_targets = self._get_real_targets(targets)
        not_really = self._get_not_really_targets(targets)
        if not_really:
            logger.warning(u'Следующие изменения не установлены, поэтому не будут откачены: %s', ', '.join(not_really))
        if not real_targets:
            logger.warning(u'Нечего откатывать')
            return
        sequence = DBToolBaseNode.dependents(real_targets, self.installed_updates)
        logger.info(u'Откатываем %s', ', '.join(real_targets))
        if sequence:
            logger.warning('Также будут откачены %s', ', '.join(sequence))
        if self._proceed():
            self._make_downgrades(sequence + list(real_targets))
        else:
            logger.info(u'Откат прерван пользователем')


