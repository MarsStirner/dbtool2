# coding: utf-8

from deptree. internals.base import DBToolBaseNode


class ErrandsFiles(DBToolBaseNode):
    name = 'rimis-1101'
    depends = ['rimis-1011.1', 'rimis-1011.2']


class FileMetaUuidChange(DBToolBaseNode):
    name = 'rimis-1011.1'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `FileMeta`
DROP FOREIGN KEY `fk_filemeta_filegroupdocument`;
''')

            c.execute(u'''
ALTER TABLE `FileMeta`
CHANGE COLUMN `name` `name` VARCHAR(255) NOT NULL COMMENT 'отображаемое имя' ,
CHANGE COLUMN `path` `path` VARCHAR(512) NULL DEFAULT NULL COMMENT 'путь до места нахождения, если храннение осуществляется средствами МИС' ,
CHANGE COLUMN `filegroup_id` `filegroup_id` INT(11) NULL DEFAULT NULL COMMENT '{FileGroupDocument}' ,
ADD COLUMN `note` VARCHAR(1024) NULL DEFAULT NULL AFTER `deleted`;
''')

            c.execute(u'''
ALTER TABLE `FileMeta`
ADD COLUMN `createDatetime` DATETIME NOT NULL AFTER `id`,
ADD COLUMN `modifyDatetime` DATETIME NOT NULL AFTER `createDatetime`;
''')

            c.execute(u'''
ALTER TABLE `FileMeta`
ADD COLUMN `uuid` BINARY(16) NULL DEFAULT NULL COMMENT 'UUID' ,
ADD COLUMN `extension` VARCHAR(32) NULL DEFAULT NULL COMMENT 'Изначальное расширение файла' AFTER `name`,
ADD UNIQUE INDEX `uuid_UNIQUE` (`uuid` ASC);
''')

            c.execute(u'''
ALTER TABLE `FileMeta`
ADD CONSTRAINT `fk_filemeta_filegroupdocument`
  FOREIGN KEY (`filegroup_id`)
  REFERENCES `FileGroupDocument` (`id`)
  ON DELETE CASCADE
  ON UPDATE CASCADE;
''')


class ErrandFilesAttachCreateTable(DBToolBaseNode):
    name = 'rimis-1011.2'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE IF NOT EXISTS `ErrandFileAttach` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `errand_id` int(11) NOT NULL COMMENT '{Errand}',
  `filemeta_id` int(11) NOT NULL COMMENT '{FileMeta}',
  `setPerson_id` int(11) NOT NULL COMMENT 'Пользователь, прикрепивший файл {Person}',
  `attachDate` datetime NOT NULL COMMENT 'Дата прикрепления',
  `deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_errandfileattach_errand_idx` (`errand_id`),
  KEY `fk_errandfileattach_filemeta_idx` (`filemeta_id`),
  KEY `fk_errandfileattach_setperson_idx` (`setPerson_id`),
  CONSTRAINT `fk_errandfileattach_errand` FOREIGN KEY (`errand_id`) REFERENCES `Errand` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_errandfileattach_filemeta` FOREIGN KEY (`filemeta_id`) REFERENCES `FileMeta` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_errandfileattach_setperson` FOREIGN KEY (`setPerson_id`) REFERENCES `Person` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Относящиеся к поручению файлы';
''')
