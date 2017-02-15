# coding: utf-8

from deptree.internals.base import DBToolBaseNode


class RPTMetaModufyEnum(DBToolBaseNode):
    name = 'rimis-1244'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE rbRisarPrintTemplateMeta MODIFY type ENUM('Integer', 'Float', 'String', 'Boolean', 'Date', 'Time', 'List', 'Multilist', 'RefBook', 'RefBook.name', 'Organisation', 'OrgStructure', 'Person', 'Service', 'SpecialVariable', 'MKB', 'Area', 'MultiRefBook', 'MultiOrganisation', 'MultiOrgStructure', 'MultiPerson', 'MultiService', 'MultiMKB', 'MultiArea') NOT NULL;
''')
