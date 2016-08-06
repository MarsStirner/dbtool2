# coding: utf-8

from deptree. internals.base import DBToolBaseNode


class MeasuresNonPreg(DBToolBaseNode):
    name = 'rimis-1210'
    depends = ['rimis-1210.1']


class MeasureProtocolFilters(DBToolBaseNode):
    name = 'rimis-1210.1'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `ExpertProtocol`
ADD COLUMN `age` VARCHAR(9) NULL DEFAULT '' COMMENT 'Применимо для указанного интервала возрастов пусто-нет ограничения, \"{NNN{д|н|м|г}-{MMM{д|н|м|г}}\" - с NNN дней/недель/месяцев/лет по MMM дней/недель/месяцев/лет; пустая нижняя или верхняя граница - нет ограничения снизу или сверху' AFTER `deleted`,
ADD COLUMN `sex` TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'Применимо для указанного пола (0-любой, 1-М, 2-Ж)' AFTER `age`;
''')

            c.ececute(u'''
CREATE TABLE `ExpertProtocol_ActionType` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `protocol_id` int(11) NOT NULL COMMENT '{ExpertProtocol}',
  `actionType_id` int(11) NOT NULL COMMENT '{ActionType}',
  PRIMARY KEY (`id`),
  KEY `fk_expertprotocol_actiontype_protocol_idx` (`protocol_id`),
  KEY `fk_expertprotocol_actiontype_protocol_idx1` (`actionType_id`),
  CONSTRAINT `fk_expertprotocol_actiontype_at` FOREIGN KEY (`actionType_id`) REFERENCES `ActionType` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_expertprotocol_actiontype_protocol` FOREIGN KEY (`protocol_id`) REFERENCES `ExpertProtocol` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Ограничения по выбору протокола. Применяется только при работе с указанным AT';
''')
