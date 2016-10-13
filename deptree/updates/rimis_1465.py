# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class Rimis1465(DBToolBaseNode):
    name = 'rimis-1465'
    depends = [
        'rimis-1465.add-table',
    ]


class MaternalCertificate(DBToolBaseNode):
    name = 'rimis-1465.add-table'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
            CREATE TABLE MaternalCertificates
            (
                id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
                series VARCHAR(64) COMMENT 'Серия',
                number VARCHAR(64) COMMENT 'Номер',
                date DATETIME COMMENT 'Дата выдачи',
                issuing_LPU_id INT(11) COMMENT 'ЛПУ выдачи_справочник {Organisation}',
                issuing_LPU_free_input VARCHAR(255) COMMENT 'ЛПУ выдачи_вручную',
                event_id INT(11),
                deleted INT(11) DEFAULT '0' NOT NULL );'''
            )