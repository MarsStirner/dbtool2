# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode


logger = logging.getLogger('dbtool')


class FixTTJBarcodeDuplication(DBToolBaseNode):
    name = 'tmis-1233'
    depends = ['tmis-1233.1', 'tmis-1233.2', 'tmis-1233.3']


class AddTTJBarcodeTable(DBToolBaseNode):
    name = 'tmis-1233.1'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `TTJ_BARCODE` (
  `barcode` INT(11) NOT NULL,
  `period` INT(11) NOT NULL,
  PRIMARY KEY (`barcode`, `period`))
ENGINE = InnoDB
COMMENT = 'Баркоды журнала забора биоматериала';
''')


class ChangeBeforeInsertTTJTrigger(DBToolBaseNode):
    name = 'tmis-1233.2'
    depends = ['tmis-1233.1']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''DROP TRIGGER IF EXISTS TTJ_INSERT''')

            c.execute(u'''
CREATE DEFINER={0} TRIGGER `TTJ_INSERT` BEFORE INSERT ON `TakenTissueJournal` FOR EACH ROW BEGIN
    DECLARE n_period INT;
    DECLARE n_barcode INT;
    DECLARE vLockName VARCHAR(64) CHARSET utf8;
    DECLARE err_msg VARCHAR(255);

    SET vLockName = CONCAT(DATABASE(), '_TTJ_INSERT');
        IF NEW.barcode is NULL OR NEW.period is NULL THEN
            SELECT
                barcode, period
            INTO
                n_barcode, n_period
            FROM `TTJ_BARCODE`
            ORDER BY `period` DESC, `barcode` DESC LIMIT 1 FOR UPDATE;
            SET n_barcode = n_barcode + 1;
            IF n_barcode > 999999 THEN
                SET n_period = n_period + 1;
                SET n_barcode = 100000;
            END IF;
            INSERT INTO TTJ_BARCODE (`barcode`, `period`) VALUES (n_barcode, n_period);

            SET NEW.barcode = n_barcode;
            SET NEW.period = n_period;
        END IF;
END'''.format(cls.config['definer']))


class SetInitialBarcodeAndPeriodFromTTJ(DBToolBaseNode):
    name = 'tmis-1233.3'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'SELECT barcode, period FROM TakenTissueJournal '
                      u'ORDER BY period DESC, barcode DESC LIMIT 1')
            res = c.fetchone()
            if res:
                barcode, period = res
            else:
                barcode, period = 100000, 1

            c.execute(u'INSERT INTO `TTJ_BARCODE` (`barcode`, `period`) VALUES (%s, %s)',
                      (barcode, period))
