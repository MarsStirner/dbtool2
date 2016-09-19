# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class FixStoredProcedureFormatAddress(DBToolBaseNode):
    name = 'tmis-1230'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''DROP function IF EXISTS `formatAddress`;''')

            c.execute(u'''
CREATE DEFINER={0} FUNCTION `formatAddress`(aAddress_id INT) RETURNS varchar(250) CHARSET utf8
    READS SQL DATA
    DETERMINISTIC
    COMMENT 'return formatted address'
BEGIN
    DECLARE vHouse_id        INT;
    DECLARE vKLADRCode       VARCHAR(13) CHARSET utf8;
    DECLARE vKLADRStreetCode VARCHAR(17) CHARSET utf8;
    DECLARE vStreetFreeInput VARCHAR(128) CHARSET utf8;
    DECLARE vTown            VARCHAR(250) CHARSET utf8;
    DECLARE vStreet          VARCHAR(250) CHARSET utf8;
    DECLARE vNumber          VARCHAR(16) CHARSET utf8;
    DECLARE vCorpus          VARCHAR(16) CHARSET utf8;
    DECLARE vFlat            VARCHAR(16) CHARSET utf8;
    SELECT house_id, flat INTO vHouse_id, vFlat FROM Address WHERE id = aAddress_id LIMIT 1;
    IF NOT ISNULL(vHouse_id) THEN
        SELECT
            KLADRCode, KLADRStreetCode, streetFreeInput, number, corpus
            INTO vKLADRCode, vKLADRStreetCode, vStreetFreeInput, vNumber, vCorpus
        FROM AddressHouse WHERE id = vHouse_id LIMIT 1;
        IF NOT ISNULL(vKLADRCode) AND vKLADRCode != '' THEN
            SET vTown = getTownName(vKLADRCode);
        END IF;
        IF NOT ISNULL(vKLADRStreetCode) AND vKLADRStreetCode != '' THEN
            SET vStreet = getStreetName(vKLADRStreetCode);
        ELSEIF NOT ISNULL(vStreetFreeInput) THEN
            SET vStreet = vStreetFreeInput;
        END IF;
        IF NOT ISNULL(vNumber) AND vNumber != '' THEN
            SET vNumber = CONCAT(_utf8'д.', vNumber);
        ELSE
            SET vNumber = NULL;
        END IF;
        IF NOT ISNULL(vCorpus) AND vCorpus != '' THEN
            SET vCorpus = CONCAT(_utf8'к.', vCorpus);
        ELSE
            SET vCorpus = NULL;
        END IF;
    END IF;
    IF NOT ISNULL(vFlat) AND vFlat != '' THEN
        SET vFlat = CONCAT(_utf8'кв.', vFlat);
    ELSE
        SET vFlat = NULL;
    END IF;
    RETURN CONCAT_WS(', ', vTown, vStreet, vNumber, vCorpus, vFlat);
END'''.format(cls.config['definer']))
