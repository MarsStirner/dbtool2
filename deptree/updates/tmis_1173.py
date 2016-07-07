# -*- coding: utf-8 -*-
from deptree.internals.base import DBToolBaseNode


class FinanceTransactionPersonAdd(DBToolBaseNode):
    name = 'tmis-1173'
    depends = []

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `FinanceTransaction`
ADD COLUMN `createPerson_id` INT(11) NULL DEFAULT NULL COMMENT '{Person}' AFTER `id`,
ADD INDEX `fk_financetransaction_create_person_idx` (`createPerson_id` ASC);
''')

            c.execute(u'''
ALTER TABLE `FinanceTransaction`
ADD CONSTRAINT `fk_financetransaction_create_person`
  FOREIGN KEY (`createPerson_id`)
  REFERENCES `Person` (`id`)
  ON DELETE RESTRICT
  ON UPDATE CASCADE;
''')