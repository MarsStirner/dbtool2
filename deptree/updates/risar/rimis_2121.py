# coding: utf-8
from deptree.internals.base import DBToolBaseNode


class RemoveNonNullProperty(DBToolBaseNode):
    name = 'rimis-2121'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
                UPDATE `ActionType`
                SET `defaultPersonInEvent`='4'
                WHERE `flatCode`='gynecological_visit_general_checkUp' AND `deleted`='0';
            ''')
