# coding: utf-8
from deptree.internals.base import DBToolBaseNode


class Main(DBToolBaseNode):
    name = 'tmis-1403'
    depends = ['tmis-1403a', 'tmis-1403b', 'tmis-1403c', 'tmis-1403d', 'tmis-1403e']


class TalonVmpEndDate(DBToolBaseNode):
    name = 'tmis-1403a'
    depends = []

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''ALTER TABLE `VMPCoupon` ADD `endDate` DATETIME;''')


class TalonVmpBegDate(DBToolBaseNode):
    name = 'tmis-1403b'
    depends = []

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''ALTER TABLE `VMPCoupon` ADD COLUMN `begDate` DATETIME;''')


class QuotaTypeAddColumnd(DBToolBaseNode):
    name = 'tmis-1403c'
    depends = []

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''ALTER TABLE `QuotaType` ADD COLUMN `amount_of_days` INT(11) NOT NULL;''')


class QuotaTypeThirtyDays(DBToolBaseNode):
    name = 'tmis-1403d'
    depends = ['tmis-1403c']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''UPDATE `QuotaType` set amount_of_days = 30;''')


class QuotaTypeFortyDays(DBToolBaseNode):
    name = 'tmis-1403e'
    depends = ['tmis-1403c']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u"""UPDATE `QuotaType` set amount_of_days = 45 WHERE profile_code='17.00';""")
