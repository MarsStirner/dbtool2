# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class Rimis1348InfisWillBeNULL(DBToolBaseNode):
    name = 'rimis-1348'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u"""
            ALTER TABLE Organisation
            CHANGE `infisCode` `infisCode` VARCHAR(12) CHARSET utf8 COLLATE utf8_general_ci NULL COMMENT 'код по ИНФИС (тер.фонд)'
            """)