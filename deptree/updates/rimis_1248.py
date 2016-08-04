# -*- coding: utf-8 -*-
from deptree.internals.base import DBToolBaseNode

__author__ = 'viruzzz-kun'


class RIMIS1248(DBToolBaseNode):
    name = 'rimis-1248'
    depends = ['rimis-1248.1', 'rimis-1248.2']


class RIMIS1248a(DBToolBaseNode):
    name = 'rimis-1248.1'
    depends = []

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute('''
ALTER TABLE `MKB`
    ADD COLUMN `ParentDiagID` VARCHAR(8) NULL DEFAULT NULL AFTER `DiagName`,
    ADD INDEX `ParentDiagID` (`ParentDiagID`),
    ADD CONSTRAINT `FK_MKB_MKB` FOREIGN KEY (`ParentDiagID`) REFERENCES `MKB` (`DiagID`);
''')

    @classmethod
    def downgrade(cls):
        with cls.connection as c:
            c.execute('''ALTER TABLE `MKB` DROP COLUMN `ParentDiagID`''')


class RIMIS1248b(DBToolBaseNode):
    name = 'rimis-1248.2'
    depends = ['rimis-1248.1']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute('''UPDATE `MKB` SET `MKB`.ParentDiagID = LEFT(`MKB`.DiagID, 3) WHERE LENGTH(`MKB`.DiagID) > 3''')

    @classmethod
    def downgrade(cls):
        with cls.connection as c:
            c.execute('''UPDATE `MKB` SET `MKB`.ParentDiagID = NULL''')