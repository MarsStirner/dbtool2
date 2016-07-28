# -*- coding: utf-8 -*-
from deptree.internals.base import DBToolBaseNode


class AdministrativePermissionFinanceChanges(DBToolBaseNode):
    name = 'tmis-1179'
    depends = []

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
UPDATE `rbFinance` SET `code`='admperm1' WHERE `name`='Административное разрешение (сотрудник)';
''')
            c.execute(u'''
UPDATE `rbFinance` SET `code`='admperm2' WHERE `name`='Административное разрешение (родственник)';
''')
            c.execute(u'''
INSERT INTO `rbUserRight` (`code`, `name`) VALUES ('evtAllAdmPermCreate', 'Имеет возможность создавать все обращения с финансированием \"Административное разрешение\"');
''')
            c.execute(u'''
INSERT INTO `rbUserRight` (`code`, `name`) VALUES ('evtAllAdmPermSetExecDate', 'Имеет возможность устанавливать дату завершения в обращениях с финансированием \"Административное разрешение\"');
''')
