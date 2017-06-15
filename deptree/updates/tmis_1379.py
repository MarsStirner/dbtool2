# coding: utf-8


from deptree.internals.base import DBToolBaseNode


class ActionFilesAttachesAddTable(DBToolBaseNode):
    name = 'tmis-1379'
    depends = ['rimis-1472', 'tmis-1379.add_atp_field']


class AddActionTypeField(DBToolBaseNode):
    name = 'tmis-1379.add_atp_field'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `ActionType` ADD COLUMN ( `canHaveAttaches` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'Возможность цеплять файлы к Action' );''')
