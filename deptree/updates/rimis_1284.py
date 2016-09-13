# coding: utf-8

from deptree. internals.base import DBToolBaseNode


class RbPolicyTypeSerialAndNumberMaxLength(DBToolBaseNode):
    name = 'rimis-1284'

    @classmethod
    def not_actual_upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
                        ALTER TABLE `rbPolicyType`
                        ADD COLUMN `serial_maxlength` INT NULL AFTER `insurance_type`,
                        ADD COLUMN `number_maxlength` INT NULL AFTER `serial_maxlength`;
                        ''')

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
UPDATE hospital1_risar.rbPolicyType SET serial_mask = '?*?*?*?*', number_mask = '?9?9?9?9-?9?9?9?9-?9?9?9?9-?9?9?9?9'  WHERE cmiOld = 'cmiOld';
''')
    @classmethod
    def downgrade(cls):
        with cls.connection as c:
            c.execute(u'''
    ALTER TABLE `rbPolicyType`
  DROP COLUMN `serial_maxlength`,
  DROP COLUMN `number_maxlength`;
    ''')