#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import logging
from itertools import product, izip, count

from deptree.internals.base import _DBToolBase, db_transactional

logger = logging.getLogger('dbtool')


class EmptyList(Exception):
    pass


def get_points(rowcount):
    if rowcount < 1:
        raise EmptyList
    return [(x * (rowcount - 1) / 100, x) for x in xrange(101)]


def join(t):
    return u''.join(t)


class _DBToolDepersonalize(_DBToolBase):
    def __percentage(self, rowcounts):
        if self.interactive:
            sys.stderr.write(u'%i%% ' % rowcounts[0][1])
            sys.stderr.flush()
        else:
            logger.info(u'%i%% ' % rowcounts[0][1])
        del rowcounts[0]

    def perform_depersonalize(self):
        self.depersonalize_client()
        self.depersonalize_person()
        self.depersonalize_documents()

    @db_transactional
    def depersonalize_client(self):
        db = self.connection
        logger.info(u'Деперсонализуем пациентов...')
        try:
            sql = u"UPDATE `Client` SET `lastName` = %s, `firstName` = %s, `patrName` = %s WHERE `id` = %s"
            with db as cursor, db as write_cursor:
                cursor.execute("SELECT COUNT(1) FROM `Client`")
                rowcount = cursor.fetchone()[0]
                if not rowcount:
                    raise EmptyList
                rowcounts = get_points(rowcount)
                logger.info(u'Всего %i' % rowcount)

                cursor.execute("SELECT `id` FROM `Client` FOR UPDATE")

                cache = []

                for ((client_id,), data, rown) in izip(cursor, product(u'абвгде', repeat=6), count()):
                    cache.append((join(data), join(data), join(data), client_id))
                    # write_cursor.execute(sql, )
                    if rown == rowcounts[0][0]:
                        write_cursor.executemany(sql, cache)
                        self.__percentage(rowcount)
                        cache = []
        except EmptyList:
            logger.info(u'Пациенты не найдены')

    @db_transactional
    def depersonalize_person(self):
        db = self.connection
        logger.info(u'Деперсонализуем врачей...')
        sql = u"UPDATE `Person` SET `lastName` = %s, `firstName` = %s, `patrName` = %s WHERE `id` = %s"
        try:
            with db as cursor, db as write_cursor:
                cursor.execute("SELECT COUNT(1) FROM `Person`")
                rowcount = cursor.fetchone()[0]
                if not rowcount:
                    raise EmptyList
                rowcounts = get_points(rowcount)
                logger.info(u'Всего %i' % rowcount)

                cursor.execute("SELECT `id` FROM `Person` FOR UPDATE")

                cache = []

                for ((person_id,), data, rown) in izip(cursor, product(u'едгвба', repeat=6), count()):
                    write_cursor.execute(sql, (join(data), join(data), join(data), person_id))
                    if rown == rowcounts[0][0]:
                        write_cursor.executemany(sql, cache)
                        self.__percentage(rowcount)
                        cache = []
        except EmptyList:
            logger.info(u'Врачи не найдены')

    @db_transactional
    def depersonalize_documents(self):
        db = self.connection
        logger.info(u'Деперсонализуем документы...')
        sql = u"UPDATE `ClientDocument` SET `number` = %s WHERE `id` = %s"
        try:
            with db as cursor, db as write_cursor:
                cursor.execute("SELECT COUNT(1) FROM `ClientDocument`")
                rowcount = cursor.fetchone()[0]
                if not rowcount:
                    raise EmptyList
                rowcounts = get_points(rowcount)
                logger.info(u'Всего %i' % rowcount)

                cursor.execute("SELECT `id` FROM `ClientDocument` FOR UPDATE")

                cache = []

                for ((doc_id,), data, rown) in izip(cursor, product(u'123456789', repeat=6), count()):
                    write_cursor.execute(sql, (join(data), doc_id))
                    if rown == rowcounts[0][0]:
                        write_cursor.executemany(sql, cache)
                        self.__percentage(rowcount)
                        cache = []
        except EmptyList:
            logger.info(u'Документы не найдены')

