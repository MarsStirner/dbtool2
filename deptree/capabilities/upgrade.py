# -*- coding: utf-8 -*-
import logging

import MySQLdb
from deptree.internals.base import _DBToolBase, DBToolBaseNode, db_transactional
from deptree.internals.models import DependencyNotFound

logger = logging.getLogger('dbtool')

__author__ = 'viruzzz-kun'


# noinspection SqlResolve
class _DBToolUpgrader(_DBToolBase):
    def _get_sequence(self, targets):
        """
        Возвращает фактическую последовательность установки зависимостей
        :type targets: list|set
        :param targets: Целевые апгрейды
        :return:
        """
        result = []
        stops = self.installed_updates[:]
        for target in targets:
            try:
                node = DBToolBaseNode.get(target)
                sequence = node.resolve(*stops)
                result.extend(sequence)
                stops.extend(sequence)
            except DependencyNotFound, e:
                logger.error(u'Зависимость %s не найдена', e.node_name)
        return result

    @db_transactional
    def _make_upgrades(self, sequence):
        """
        Выполные установку зависимостей согласно последовательности
        :type sequence: list
        :param sequence: Последовательность
        :return:
        """
        with self.connection as cursor:
            for name in sequence:
                node = DBToolBaseNode.get(name)
                logger.info(u'Выполняется обновление %s', name)
                if self.dry_run:
                    continue
                try:
                    if hasattr(node, 'upgrade'):
                        node.upgrade()
                except MySQLdb.ProgrammingError:
                    raise
                else:
                    cursor.execute('INSERT INTO InstalledDbUpdates (`name`) VALUES (%s)', (name, ))

    def perform_updates(self, targets):
        """
        "Говорящий" с пользователем "трамплин"
        :type targets: list|str
        :param targets: Целевые апгрейды
        :return:
        """
        logger.info(u'Запрошена установка обновлений: %s', ', '.join(targets))
        sequence = self._get_sequence(targets)
        if not sequence:
            logger.info(u'Нечего устанавливать')
            return
        logger.info(u'Будут установлены следующие обновления:\n%s', ', '.join(sequence))
        if self._proceed():
            self._make_upgrades(sequence)
        else:
            logger.info(u'Установка обновлений прервана пользователем')


