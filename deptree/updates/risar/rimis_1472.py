# coding: utf-8

from deptree.internals.base import DBToolBaseNode


class AddTableActionFileAttach(DBToolBaseNode):
    name = 'rimis-1472'
    depends = ['rimis-1011.1']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `ActionFileAttach` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_id` int(11) NOT NULL COMMENT '{Action}',
  `filemeta_id` int(11) NOT NULL COMMENT '{FileMeta}',
  `setPerson_id` int(11) NOT NULL COMMENT 'Пользователь, прикрепивший файл {Person}',
  `attachDate` datetime NOT NULL COMMENT 'Дата прикрепления',
  `deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_actionfileattach_action_idx` (`action_id`),
  KEY `fk_actionfileattach_filemeta_idx` (`filemeta_id`),
  KEY `fk_actionfileattach_setperson_idx` (`setPerson_id`),
  CONSTRAINT `fk_actionfileattach_errand` FOREIGN KEY (`action_id`) REFERENCES `Action` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_actionfileattach_filemeta` FOREIGN KEY (`filemeta_id`) REFERENCES `FileMeta` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_actionfileattach_setperson` FOREIGN KEY (`setPerson_id`) REFERENCES `Person` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Относящиеся к action файлы';
''')
