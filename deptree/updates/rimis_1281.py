# -*- coding: utf-8 -*-

import logging

from collections import namedtuple
from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')

TABLE_NAME = "rbPrintTemplate"
PREFIX = ""
POSTFIX = "_dupl"
MAX_CODE_LENGTH = 32


class Rimis1281(DBToolBaseNode):
    name = 'rimis-1281'
    depends = ['rimis-1281.migration', 'rimis-1281.code-unique']


class Rimis1281CodeLengthIncrease(DBToolBaseNode):
    name = 'rimis-1281.code-increase'
    depends = []

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            logger.info(u"\t>> Меняем рамер поля code до: {0} символов".format(MAX_CODE_LENGTH))
            c.execute(u"""ALTER TABLE {0}
                      CHANGE `code` `code` VARCHAR(32) CHARSET utf8
                                            COLLATE utf8_general_ci NOT NULL   COMMENT 'Код'""".format(TABLE_NAME))


class Rimis1281TemplateCodeFix(DBToolBaseNode):
    name = 'rimis-1281.migration'
    depends = ['rimis-1281.code-increase', ]

    @classmethod
    def upgrade(cls):
        table_fields = ['id', 'code', 'name', 'context', 'fileName', 'default', 'dpdAgreement', 'render',
                        'templateText', 'deleted']
        grouped_fieds = ['code', 'context', 'cnt', 'ids']

        make_nd = lambda name, fields: namedtuple(name, " ".join(fields))

        TemplateRow = make_nd('TemplateRow', table_fields)
        Duplicate = make_nd('Duplicate', grouped_fieds)
        still_dupes = []
        dup_new_code = {}
        with cls.connection as c:
            logger.info(u"\t Переименовываем шаблоны".format(MAX_CODE_LENGTH))
            c.execute(u'''select code, context, count(*) as cnt,  GROUP_CONCAT(id) AS ids from {0}
                                        group by code, context  having cnt > 1 order by cnt desc;'''.format(TABLE_NAME))
            duplicates = map(lambda x: Duplicate(*x), c.fetchall())
            for duplicate in duplicates:
                _skip_first, _comma, ids = duplicate.ids.partition(',')
                if ids:
                    c.execute(u'''select * from {table} where id in ({ids})'''.format(**{'ids': ids,
                                                                                         "table": TABLE_NAME}))
                    templates_to_rename = map(lambda x: TemplateRow(*x), c.fetchall())
                    for nm, tpl in enumerate(templates_to_rename, 1):
                        new_code = PREFIX + tpl.code + POSTFIX + str(nm)
                        if len(new_code) > MAX_CODE_LENGTH:
                            still_dupes.append(tpl)
                            dup_new_code[tpl.id] = new_code
                            continue

                        upd = u"""update {table} set code='{code}' where id = {id}""".format(**{'code': new_code,
                                                                                                'id': tpl.id,
                                                                                                'table': TABLE_NAME})
                        try:
                            logger.info(u"\t " + upd)
                            c.execute(upd)
                        except Exception as e:
                            print upd
                            print e

        for dup in still_dupes:
            logger.info(u"""\t\t Шаблон с id: {id}, кодом: {code}, контекстом: {context} не был исправлен,
                                    т.к. кода:{new_code} не поместился в поле code({max_field_length})""". \
                        format(new_code=dup_new_code[dup.id],
                               max_field_length=MAX_CODE_LENGTH,
                               **dup.__dict__))


class Rimis1281UniqueCodeContext(DBToolBaseNode):
    name = 'rimis-1281.code-unique'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            logger.info(u"\tУстанавливаем уникальность на поля: Unique(code, context)")
            c.execute(u"""ALTER TABLE {0} ADD UNIQUE INDEX (`code`, `context`); """.format(TABLE_NAME))
