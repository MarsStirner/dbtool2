# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class AptGroupsTable(DBToolBaseNode):
    name = 'tmis-1385'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''CREATE TABLE `APT_Groups` (
`master_apt_id` int(11) NOT NULL COMMENT 'Родительский {ActionPropertyType}',
`apt_id` int(11) NOT NULL COMMENT 'Зависимый {ActionPropertyType}',
PRIMARY KEY (`master_apt_id`,`apt_id`),
CONSTRAINT `fk_apt_group_master_apt` FOREIGN KEY (`master_apt_id`) REFERENCES `ActionPropertyType` (`id`) ON UPDATE CASCADE ON DELETE CASCADE,
CONSTRAINT `fk_apt_group_apt` FOREIGN KEY (`apt_id`) REFERENCES `ActionPropertyType` (`id`) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Группы зависимых типов свойств';
''')
