# coding: utf-8


from deptree.internals.base import DBToolBaseNode


class Main(DBToolBaseNode):
    name = 'tmis-1487'
    depends = ['tmis-1487.add_short_name']


class AddColumnOrgStructure(DBToolBaseNode):
    name = 'tmis-1487.add_short_name'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''ALTER TABLE `OrgStructure` ADD COLUMN (`shortName` varchar(255) NOT NULL COMMENT 'Сокращенное наименование');''')
            c.execute(u"""update OrgStructure set shortName=name where shortName='';""")