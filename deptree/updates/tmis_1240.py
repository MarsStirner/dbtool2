# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')

class UUIDFix(DBToolBaseNode):
    name = 'tmis-1240'
    depends = ['tmis-1240.Action', 'tmis-1240.Client', 'tmis-1240.DrugChart',
               'tmis-1240.Event', 'tmis-1240.Organisation', 'tmis-1240.OrgStructure',
               'tmis-1240.Person', 'tmis-1240.Pharmacy', 'tmis-1240.PrescriptionSendingRes',
               'tmis-1240.rbStorage',
               # fixes
               'tmis-1297']


class UUIDFixAction(DBToolBaseNode):
    name = 'tmis-1240.Action'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            fix_uuid_for_table(u'Action', c)

    @classmethod
    def downgrade(cls):
        with cls.connection as c:
            downgrade(u'Action', c)


class UUIDFixClient(DBToolBaseNode):
    name = 'tmis-1240.Client'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            fix_uuid_for_table(u'Client', c)

    @classmethod
    def downgrade(cls):
        with cls.connection as c:
            downgrade(u'Client', c)


class UUIDFixDrugChart(DBToolBaseNode):
    name = 'tmis-1240.DrugChart'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            fix_uuid_for_table_already_exists_string(u'DrugChart', c)

    @classmethod
    def downgrade(cls):
        with cls.connection as c:
            downgrade_already_exists(u'DrugChart', c)


class UUIDFixEvent(DBToolBaseNode):
    name = 'tmis-1240.Event'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            fix_uuid_for_table(u'Event', c)

    @classmethod
    def downgrade(cls):
        with cls.connection as c:
            downgrade(u'Event', c)


class UUIDFixOrganisation(DBToolBaseNode):
    name = 'tmis-1240.Organisation'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            fix_uuid_for_table(u'Organisation', c)

    @classmethod
    def downgrade(cls):
        with cls.connection as c:
            downgrade(u'Organisation', c)


class UUIDFixOrgStructure(DBToolBaseNode):
    name = 'tmis-1240.OrgStructure'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            fix_uuid_for_table(u'OrgStructure', c)

    @classmethod
    def downgrade(cls):
        with cls.connection as c:
            downgrade(u'OrgStructure', c)


class UUIDFixPerson(DBToolBaseNode):
    name = 'tmis-1240.Person'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            fix_uuid_for_table(u'Person', c)

    @classmethod
    def downgrade(cls):
        with cls.connection as c:
            downgrade(u'Person', c)


class UUIDFixPharmacy(DBToolBaseNode):
    name = 'tmis-1240.Pharmacy'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            fix_uuid_for_table_already_exists_string(u'Pharmacy', c)

    @classmethod
    def downgrade(cls):
        with cls.connection as c:
            downgrade_already_exists(u'Pharmacy', c)



class UUIDFixPrescriptionSendingRes(DBToolBaseNode):
    name = 'tmis-1240.PrescriptionSendingRes'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            fix_uuid_for_table_already_exists_string(u'PrescriptionSendingRes', c)

    @classmethod
    def downgrade(cls):
        with cls.connection as c:
            downgrade_already_exists(u'PrescriptionSendingRes', c)



class UUIDFixStorage(DBToolBaseNode):
    name = 'tmis-1240.rbStorage'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            fix_uuid_for_table_already_exists_string(u'rbStorage', c)

    @classmethod
    def downgrade(cls):
        with cls.connection as c:
            downgrade_already_exists(u'rbStorage', c)


query_add_uuid_column = u'''ALTER TABLE `{0}` ADD COLUMN `uuid` binary(16) NOT NULL;'''
query_add_uuid_column_already_exists = u'''ALTER TABLE `{0}` ADD COLUMN `uuid_new` BINARY(16) NOT NULL AFTER `uuid`;'''

query_rename_columns = u'''ALTER TABLE `{0}` CHANGE COLUMN `uuid` `uuid_old` VARCHAR(36), CHANGE COLUMN `uuid_new` `uuid` BINARY(16);'''

query_fill_data_already_exists = u'''UPDATE `{0}` SET `uuid_new` = UNHEX(REPLACE(IF(`uuid` IS NULL OR `uuid` = '', UUID(), `uuid`), '-',''));'''
query_fill_data_with_join = u'''UPDATE `{0}` t LEFT JOIN `UUID` u ON u.id = t.`uuid_id` SET t.`uuid` = UNHEX(REPLACE(IF(u.id IS NOT NULL, u.`uuid`, UUID()), '-',''));'''

query_drop_uuid_column = u'''ALTER TABLE `{0}` DROP COLUMN `uuid`;'''
query_rename_for_downgrade = u'''ALTER TABLE `{0}` CHANGE COLUMN `uuid_old` `uuid` VARCHAR(36);'''


def fix_uuid_for_table(table_name, connection):
    connection.execute(query_add_uuid_column.format(table_name))
    logger.info(u'''Table[{}]: UUID column added'''.format(table_name))
    connection.execute(query_fill_data_with_join.format(table_name))
    logger.info(u'''Table[{}]: Old UUID migrated, empty filled with values'''.format(table_name))


def fix_uuid_for_table_already_exists_string(table_name, connection):
    connection.execute(query_add_uuid_column_already_exists.format(table_name))
    logger.info(u'''Table[{}]: UUID column added'''.format(table_name))
    connection.execute(query_fill_data_already_exists.format(table_name))
    logger.info(u'''Table[{}]: Old UUID migrated, empty filled with values'''.format(table_name))
    connection.execute(query_rename_columns.format(table_name))
    logger.info(u'''Table[{}]: UUID columns renamed'''.format(table_name))


def downgrade(table_name, connection):
    connection.execute(query_drop_uuid_column.format(table_name))
    logger.info(u'''Table[{}]: UUID column dropped'''.format(table_name))

def downgrade_already_exists(table_name, connection):
    connection.execute(query_drop_uuid_column.format(table_name))
    logger.info(u'''Table[{}]: Binary UUID column dropped'''.format(table_name))
    connection.execute(query_rename_for_downgrade.format(table_name))
    logger.info(u'''Table[{}]: Varchar UUID column in use'''.format(table_name))

