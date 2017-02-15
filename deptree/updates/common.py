# coding: utf-8

from deptree.internals.base import DBToolBaseNode


class ClientFIOChanges(DBToolBaseNode):
    name = 'rimis-643'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `Client`
    ALTER `lastName` DROP DEFAULT,
    ALTER `firstName` DROP DEFAULT,
    ALTER `patrName` DROP DEFAULT;
ALTER TABLE `Client`
    CHANGE COLUMN `lastName` `lastName` VARCHAR(255) NOT NULL COMMENT 'Фамилия' AFTER `deleted`,
    CHANGE COLUMN `firstName` `firstName` VARCHAR(255) NOT NULL COMMENT 'Имя' AFTER `lastName`,
    CHANGE COLUMN `patrName` `patrName` VARCHAR(255) NOT NULL COMMENT 'Отчество' AFTER `firstName`;
''')


class OrgTfomsCode(DBToolBaseNode):
    name = 'rimis-814'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `Organisation`
  ADD COLUMN `TFOMSCode` VARCHAR(50) NULL DEFAULT NULL COMMENT 'Код ТФОМС' AFTER `isStationary`;
ALTER TABLE `Organisation`
  ADD INDEX `TFOMSCode` (`TFOMSCode`);
''')


class PersonContactsAdd(DBToolBaseNode):
    name = 'rimis-1076.1'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `PersonContact` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modifyDatetime` datetime NOT NULL COMMENT 'Дата изменения записи',
  `modifyPerson_id` int(11) DEFAULT NULL COMMENT 'Автор изменения записи {Person}',
  `deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'Отметка удаления записи',
  `person_id` int(11) DEFAULT NULL,
  `contactType_id` int(11) NOT NULL COMMENT 'Тип контакта телефон/e-mail {rbContactType}',
  `value` varchar(255) NOT NULL COMMENT 'Контакт',
  PRIMARY KEY (`id`,`modifyDatetime`),
  KEY `modifyPerson_id` (`modifyPerson_id`),
  KEY `contactType_id` (`contactType_id`),
  KEY `client_id_deleted_contactType` (`deleted`,`contactType_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Способы связи';
''')

            data = [
                ('12', 'skype'),
                ('13', 'Телефон')
            ]
            c.executemany(u'''
INSERT INTO `rbContactType` (`code`, `name`) VALUES (%s, %s);
''', data)
