# coding: utf-8
from deptree.internals.base import DBToolBaseNode


class ReceivedAPTCodeUpdate(DBToolBaseNode):
    name = 'tmis-1406'
    depends = []

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
SELECT id FROM ActionPropertyType WHERE
name = "Клиническое описание диагноза" AND actionType_id = 112;
''')
            apt_id = c.fetchone()[0]
            c.execute(u'''
UPDATE `ActionPropertyType` SET `code`='diag_text' WHERE `id`='{0}';
'''.format(apt_id))
