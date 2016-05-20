#!/usr/bin/pypy
# -*- coding: utf-8 -*-
from datetime import datetime
import logging
from HTMLParser import HTMLParser

import os
import re
from deptree.internals.base import _DBToolBase, db_transactional

__author__ = 'mmalkov'

logger = logging.getLogger('dbtool')


mattersRe = re.compile(ur'(?P<rus>.*) \((?P<lat>.*)\)')


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._data = {}
        self._currentName = ''
        self._currentRLS = None

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            a = dict(attrs)
            self._currentName = a['name']

    def unknown_decl(self, data):
        val = data[6:]
        if self._currentName == 'URL':
            self._currentRLS = int(val[val.index('/') + 1:val.rindex('.html')])
            self._data[self._currentRLS] = {}
            return
        elif self._currentName == 'NDV':
            am = getActMatters(val)
            self._data[self._currentRLS]['ACTMATTERS'] = am or val
            return
        self._data[self._currentRLS][self._currentName] = val


def getActMatters(string):
    match = mattersRe.match(string)
    if not match:
        return string, None
    else:
        gDict = match.groupdict()
        return gDict['rus'], gDict['lat']


# noinspection PyPep8Naming
class _DBToolRlsImport(_DBToolBase):
    def user_rls_import(self, path=None):
        logger.info(u'Импортирование справочника РЛС может занять очень много времени (от нескольких минут до часа)')
        if self._proceed():
            self.perform_rls_import(path)
        else:
            logger.info(u'Импортирование справочника РЛС прервано пользователем')

    @db_transactional
    def perform_rls_import(self, path=None):
        """Преобразование одного жирного РЛСовского файла к ЯМЛ-представлению. Требует не менее 3 ГБ свободной ОЗУ!!!"""
        """Для работы необходимо не менее 3 ГиБ свободной ОЗУ, желательно использовать интерпретатор PyPy
        (быстрее в 4-7 раз) Преобразование может занять очень много времени (около 10 минут с PyPy)"""
        # Fixme: Use rbUnits and rnUnitGroup
        if self.dry_run:
            logger.warning(u'Фиктивный прогон невозможен для импорта справочника РЛС.')
            return

        config = self.config
        dbc = self.connection

        d_Packing = {}
        d_Filling = {}
        d_TradeName = {}
        d_AM = {}
        d_Form = {}
        d_Unit = {}
        d_Nomen = {}

        rd_Packing = {}
        rd_Filling = {}
        rd_TradeName = {}
        rd_AM = {}
        rd_Form = {}
        rd_Unit = {}

        fields = (
            'actMatters_id', 'tradeName_id', 'form_id', 'packing_id', 'filling_id', 'unit_id', 'dosageValue',
            'dosageUnit_id', 'drugLifetime', 'regDate'
        )

        logger.info(u'Загрузка таблиц из БД')
        with dbc as cursor:
            logger.info('... `rbUnit`')
            cursor.execute('''SELECT `id`, `code`, `name` FROM `rbUnit`; ''')
            for row in cursor:
                rd_Unit[row[1]] = row[0]
                d_Unit[row[0]] = row[1:]

            logger.info('... `rlsPacking`')
            cursor.execute('''SELECT `id`, `name` FROM `rlsPacking`; ''')
            for row in cursor:
                rd_Packing[row[1]] = row[0]
                d_Packing[row[0]] = row[1]

            logger.info('... `rlsFilling`')
            cursor.execute('''SELECT `id`, `name` FROM `rlsFilling`; ''')
            for row in cursor:
                rd_Filling[row[1]] = row[0]
                d_Filling[row[0]] = row[1]

            logger.info('... `rlsForm`')
            cursor.execute('''SELECT `id`, `name` FROM `rlsForm`; ''')
            for row in cursor:
                rd_Form[row[1]] = row[0]
                d_Form[row[0]] = row[1]

            logger.info('... `rlsTradeName`')
            cursor.execute('''SELECT `id`, `localName`, `name` FROM `rlsTradeName`; ''')
            for row in cursor:
                rd_TradeName[row[1:]] = row[0]
                d_TradeName[row[0]] = row[1:]

            logger.info('... `rlsActMatters`')
            cursor.execute('''SELECT `id`, `localName`, `name` FROM `rlsActMatters`; ''')
            for row in cursor:
                rd_AM[row[1:]] = row[0]
                d_AM[row[0]] = row[1:]

            logger.info('... `rlsNomen`')
            cursor.execute('''SELECT * FROM `rlsNomen`; ''')
            for row in cursor:
                d_Nomen[row[0]] = row[1:]

        logger.info(u"Анализируем справочник РЛС...")
        p = MyHTMLParser()

        pathName = path or config['rlsPath']
        for fileName in os.listdir(pathName):
            with open(os.path.join(pathName, fileName), 'rt', buffering=16777216) as fin:
                buf = fin.read()
                p.feed(buf.decode('utf-16'))

        logger.info(u"Начинаем загрузку...")
        with dbc as cursor:
            for rlsId, rlsData in p._data.iteritems():
                dosage = None
                dosageUnit = rlsData.get(
                    'DFMASS_SHORTNAME', rlsData.get(
                        'DFCONC_SHORTNAME', rlsData.get(
                            'DFACT_SHORTNAME', rlsData.get(
                                'DFSIZE_SHORTNAME'))))
                dosageUnitLong = rlsData.get(
                    'DFMASS_FULLNAME', rlsData.get(
                        'DFCONC_FULLNAME', rlsData.get(
                            'DFACT_FULLNAME', rlsData.get(
                                'DFSIZE_FULLNAME'))))
                if not (dosageUnit and dosageUnitLong):
                    dosageUnit = rlsData.get(
                        'PPACKMASS_SHORTNAME', rlsData.get(
                            'PPACKVOLUME_SHORTNAME'))
                    dosageUnitLong = rlsData.get(
                        'PPACKMASS_FULLNAME', rlsData.get(
                            'PPACKVOLUME_FULLNAME'))
                    if dosageUnit and dosageUnitLong:
                        dosage = rlsData.get(
                            'PPACKMASS', rlsData.get(
                                'PPACKVOLUME'))
                    else:
                        dosage = rlsData.get('DRUGDOSE')
                        if dosage is not None:
                            dosageUnit = u'шт'
                            dosageUnitLong = u'штука'
                else:
                    dosage = rlsData.get(
                        'DFMASS', rlsData.get(
                            'DFCONC', rlsData.get(
                                'DFACT', rlsData.get(
                                    'DFSIZE', rlsData.get(
                                        'DRUGDOSE')))))
                if dosage is None:
                    dUnit_id = None
                else:
                    dUnit_id = rd_Unit.get(dosageUnit)
                    if (not dUnit_id) and dosageUnit and dosageUnitLong:
                        cursor.execute('''INSERT INTO `rbUnit` (`code`, `name`) VALUES (%s, %s)''',
                                       (dosageUnit, dosageUnitLong))
                        dUnit_id = cursor.lastrowid
                        d_Unit[dUnit_id] = dosageUnit
                        rd_Unit[dosageUnit] = dUnit_id

                unit = rlsData.get(
                    'PPACKMASS_SHORTNAME', rlsData.get(
                        'PPACKVOLUME_SHORTNAME', rlsData.get(
                            'DFMASS_SHORTNAME', u'шт')))
                unitLong = rlsData.get(
                    'PPACKMASS_FULLNAME', rlsData.get(
                        'PPACKVOLUME_FULLNAME', rlsData.get(
                            'DFMASS_FULLNAME', u'штука')))

                unit_id = rd_Unit.get(unit)
                if (not unit_id) and unit and unitLong:
                    cursor.execute('''INSERT INTO `rbUnit` (`code`, `name`) VALUES (%s, %s)''',
                                   (unit, unitLong))
                    unit_id = cursor.lastrowid
                    d_Unit[unit_id] = unit
                    rd_Unit[unit] = unit_id

                regD = rlsData.get('REGDATE')
                if regD:
                    regDate = datetime.strptime(regD, '%Y%m%d').date()
                else:
                    regDate = None

                name = rlsData.get('TRADENAME'), rlsData.get('LATNAME')
                name_id = rd_TradeName.get(name)
                if not name_id:
                    # print 'TradeName', name[0], name[1], 'not found'
                    cursor.execute('''INSERT INTO `rlsTradeName` (`localName`, `name`) VALUES (%s, %s)''', name)
                    name_id = cursor.lastrowid
                    d_TradeName[name_id] = name
                    rd_TradeName[name] = name_id

                packing = rlsData.get('UPACK_SHORTNAME')
                if packing:
                    packing_id = rd_Packing.get(packing)
                    if not packing_id:
                        # print 'Packing', packing, 'not found'
                        cursor.execute('''INSERT INTO `rlsPacking` (`name`) VALUES (%s)''', packing)
                        packing_id = cursor.lastrowid
                        d_Packing[packing_id] = packing
                        rd_Packing[packing] = packing_id
                else:
                    packing_id = None

                filling = rlsData.get('PPACK_FULLNAME')
                if filling:
                    filling_id = rd_Filling.get(filling)
                    if not filling_id:
                        # print 'Filling', filling, 'not found'
                        cursor.execute('''INSERT INTO `rlsFilling` (`name`) VALUES (%s)''', filling)
                        filling_id = cursor.lastrowid
                        d_Filling[filling_id] = filling
                        rd_Filling[filling] = filling_id
                else:
                    filling_id = None

                form = rlsData.get('DRUGFORM_FULLNAME')
                if form:
                    form_id = rd_Form.get(form)
                    if not form_id:
                        # print 'Form', form, 'not found'
                        cursor.execute('''INSERT INTO `rlsForm` (`name`) VALUES (%s)''', form)
                        form_id = cursor.lastrowid
                        d_Form[form_id] = form
                        rd_Form[form] = form_id
                else:
                    form_id = None

                matter = rlsData.get('ACTMATTERS')
                if matter:
                    matter_id = rd_AM.get(matter)
                    if not matter_id:
                        cursor.execute('''INSERT INTO `rlsActMatters` (`localName`, `name`) VALUES (%s, %s)''',
                                       matter)
                        matter_id = cursor.lastrowid
                        d_AM[matter_id] = matter
                        rd_AM[matter] = matter_id
                else:
                    matter_id = None

                try:
                    lifetime = int(rlsData.get('DRUGLIFETIME'))
                except:
                    lifetime = None

                dbData = d_Nomen.get(rlsId)
                data = {
                    'id': rlsId,
                    'actMatters_id': matter_id,
                    'tradeName_id': name_id,
                    'form_id': form_id,
                    'filling_id': filling_id,
                    'packing_id': packing_id,
                    'unit_id': unit_id,
                    'dosageUnit_id': dUnit_id,
                    'dosageValue': dosage,
                    'regDate': regDate,
                    'drugLifetime': lifetime,
                }
                if dbData:
                    if any([dbData[n] != data[k] for n, k in enumerate(fields)]):
                        reason = '\n    '.join(
                            ['%s: %s != %s' % (k, dbData[n], data[k])
                             for n, k in enumerate(fields)
                             if dbData[n] != data[k]
                            ])
                        logger.info(u'Обновление rls:%i ибо:\n    %s', rlsId, reason)
                        sql = u'UPDATE rlsNomen SET ' \
                              u'`actMatters_id` = %(actMatters_id)s, ' \
                              u'`tradeName_id` = %(tradeName_id)s, ' \
                              u'`form_id` = %(form_id)s, ' \
                              u'`packing_id` = %(packing_id)s, ' \
                              u'`filling_id` = %(filling_id)s, ' \
                              u'`unit_id` = %(unit_id)s, ' \
                              u'`dosageValue` = %(dosageValue)s, ' \
                              u'`dosageUnit_id` = %(dosageUnit_id)s, ' \
                              u'`regDate` = %(regDate)s, ' \
                              u'`drugLifetime` = %(drugLifetime)s ' \
                              u'WHERE `id` = %(id)s'
                        try:
                            cursor.execute(sql, data)
                        except TypeError:
                            logger.critical(u'Внимание!\n%s', repr(data))
                            raise
                else:
                    sql = u'INSERT INTO rlsNomen (`id`, `actMatters_id`, `tradeName_id`, `form_id`, `packing_id`, ' \
                          u'`filling_id`,`unit_id`,`dosageValue`, `dosageUnit_id`, `regDate`, `drugLifetime`) ' \
                          u'VALUES (%(id)s, %(actMatters_id)s, %(tradeName_id)s, %(form_id)s, %(packing_id)s, ' \
                          u'%(filling_id)s, %(unit_id)s, %(dosageValue)s, %(dosageUnit_id)s, %(regDate)s, ' \
                          u'%(drugLifetime)s)'
                    cursor.execute(sql, data)


