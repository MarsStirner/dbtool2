# -*- coding: utf-8 -*-
from deptree.internals.base import DBToolBaseNode


class EvtDelWithInvoicesRight(DBToolBaseNode):
    name = 'tmis-1224'
    depends = []

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
INSERT INTO `rbUserRight` (`code`, `name`) VALUES
('evtDelWithInvoices', 'Имеет возможность удалять обращения с выставленными счетами');
''')
