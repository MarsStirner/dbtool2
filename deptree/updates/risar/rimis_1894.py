# coding: utf-8
from deptree.internals.base import DBToolBaseNode


class CreateTableActionType_Service_Risar(DBToolBaseNode):
    name = 'rimis-1894'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `ActionType_Service_Risar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `master_id` int(11) NOT NULL COMMENT 'тип действия {ActionType}',
  `idx` int(11) NOT NULL DEFAULT '0' COMMENT 'индекс для сортировки при показе таблицы',
  `service_code` varchar(250) NOT NULL COMMENT 'услуга {rbService}',
  `begDate` date NOT NULL COMMENT 'Дата начала действия',
  `endDate` date DEFAULT NULL COMMENT 'Дата окончания действия',
  PRIMARY KEY (`id`),
  KEY `master_id` (`master_id`),
  CONSTRAINT `fk_actiontype_service_risar_actiontype` FOREIGN KEY (`master_id`) REFERENCES `ActionType` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Выставляемая в счёте услуга за произведённое действие в зави';
''')
