# coding: utf-8


from deptree.internals.base import DBToolBaseNode


class Main(DBToolBaseNode):
    name = 'tmis-1189'
    depends = ['tmis-1189.amb-card', 'tmis-1189.ca-addcolumns', 'tmis-1189.rbattach_chage', 'tmis-1189.ca-addindexes']


class addAmbCard(DBToolBaseNode):
    name = 'tmis-1189.amb-card'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
                CREATE TABLE `AmbulanceCard` (
                  `id` int(11) NOT NULL AUTO_INCREMENT,
                  `client_id` int(11) NOT NULL COMMENT 'Прикреплённое лицо {Client}',
                  `generatedId` varchar(30) NOT NULL COMMENT 'видимый номер ',
                  `createDatetime` datetime NOT NULL COMMENT 'Дата создания амб. карты',
                  `modifyDatetime` datetime NOT NULL COMMENT 'Дата изменения амб. карты',
                  `createPerson_id` int(11) DEFAULT NULL COMMENT 'Автор записи {Person}',
                  `modifyPerson_id` int(11) DEFAULT NULL COMMENT 'Автор изменения амб. карты {Person}',
                  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'Отметка удаления записи',
                  PRIMARY KEY (`id`),
                  KEY `client_id` (`client_id`),
                  KEY `createPerson_id` (`createPerson_id`),
                  KEY `modifyPerson_id` (`modifyPerson_id`)
                ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='Амбулаторная карта';
          ''')


class ClientAttachPersonId(DBToolBaseNode):
    name = 'tmis-1189.ca-addcolumns'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(
                u''' ALTER TABLE `ClientAttach` ADD COLUMN ( `amb_card_id` int(11) NULL COMMENT 'Амбулаторная карта (если есть)' );''')
            c.execute(
                u''' ALTER TABLE `ClientAttach` ADD COLUMN ( `person_id` int(11) NULL COMMENT 'Прикреплённый врач' );''')


class ClientAttachIndexes(DBToolBaseNode):
    name = 'tmis-1189.ca-addindexes'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(
                u'''ALTER TABLE `ClientAttach` ADD INDEX `person_id` (`person_id` ASC), ADD INDEX `amb_card_id` (`amb_card_id` ASC)''')


class changerbAttachType(DBToolBaseNode):
    name = 'tmis-1189.rbattach_chage'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(
                u'''ALTER TABLE `rbAttachType` CHANGE COLUMN `finance_id` `finance_id` INT(11) NULL COMMENT 'Тип финансирования {rbFinance}'  ; ''');
