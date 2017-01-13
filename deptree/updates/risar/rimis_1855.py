# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class RIMIS1855(DBToolBaseNode):
    name = 'rimis-1855'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `rbObservationPhase` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`code` varchar(16) NOT NULL COMMENT 'код',
`name` varchar(64) NOT NULL COMMENT 'название',
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='Этапы наблюдения(коды из ExpertProtocol)';
''')

