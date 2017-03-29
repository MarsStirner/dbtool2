# -*- coding: utf-8 -*-
from deptree.internals.base import DBToolBaseNode


class InvoiceAccessAllPermission(DBToolBaseNode):
    name = 'tmis-1259'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
INSERT INTO `rbUserRight` (`code`, `name`) VALUES
('evtInvoiceAccessAll', 'Имеет доступ к любым операциям со счетами в обращениях');
''')
