# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class rbDocumentTypeAlter(DBToolBaseNode):
    name = 'genya_request.15-32'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u"""
ALTER TABLE rbDocumentType
  CHANGE COLUMN regionalCode regionalCode VARCHAR(32) NOT NULL COMMENT 'Региональный код' AFTER code,
  CHANGE COLUMN name name VARCHAR(128) NOT NULL COMMENT 'Наименование' AFTER regionalCode;
""")