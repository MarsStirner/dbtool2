# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class vrbPersonWithSpecialityAddFullName(DBToolBaseNode):
    name = 'rimis-1797'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u"""
CREATE
     OR REPLACE ALGORITHM = UNDEFINED
    DEFINER = {0}
    SQL SECURITY DEFINER
VIEW `vrbPersonWithSpeciality` AS
    SELECT
        `Person`.`id` AS `id`,
        `Person`.`code` AS `code`,
        `Person`.`deleted` AS `deleted`,
        CONCAT(`Person`.`lastName`,
                _UTF8' ',
                IF((`Person`.`firstName` = _UTF8''),
                    _UTF8'',
                    CONCAT(LEFT(`Person`.`firstName`, 1), _UTF8'.')),
                IF((`Person`.`patrName` = _UTF8''),
                    _UTF8'',
                    CONCAT(LEFT(`Person`.`patrName`, 1), _UTF8'.')),
                IF(ISNULL(`rbSpeciality`.`name`),
                    _UTF8'',
                    CONCAT(_UTF8', ', `rbSpeciality`.`name`))) AS `name`,
        CONCAT(`Person`.`lastName`,
                _UTF8' ',
                IF((`Person`.`firstName` = _UTF8''),
                    _UTF8'',
                    CONCAT(`Person`.`firstName`, _UTF8' ')),
                IF((`Person`.`patrName` = _UTF8''),
                    _UTF8'',
                    CONCAT(`Person`.`patrName`, _UTF8' ')),
                IF(ISNULL(`rbSpeciality`.`name`),
                    _UTF8'',
                    CONCAT(_UTF8' (', `rbSpeciality`.`name`, _UTF8')'))) AS `full_name`,
        `Person`.`speciality_id` AS `speciality_id`,
        `Person`.`org_id` AS `org_id`,
        `Person`.`orgStructure_id` AS `orgStructure_id`,
        `Person`.`retireDate` AS `retireDate`
    FROM
        (`Person`
        LEFT JOIN `rbSpeciality` ON ((`rbSpeciality`.`id` = `Person`.`speciality_id`)));
""".format(cls.config['definer']))
