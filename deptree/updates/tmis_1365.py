# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class PrintTemplateCETable(DBToolBaseNode):
    name = 'tmis-1365'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `rbPrintTemplateCE` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `context` varchar(64) NOT NULL COMMENT '{rbPrintTemplate.context} - родительский контекст печати, к которому будет добавляться шаблон',
  `template_id` int(11) NOT NULL COMMENT '{rbPrintTemplate.id} - дополнительный шаблон печати (с контекстом free), который добавляется к выбранному контексту',
  PRIMARY KEY (`id`),
  KEY `fk_rbprinttemplatece_rbprinttemplate_idx` (`template_id`),
  KEY `context_idx` (`context`),
  CONSTRAINT `fk_rbprinttemplatece_rbprinttemplate` FOREIGN KEY (`template_id`) REFERENCES `rbPrintTemplate` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Список шаблонов печати (свободных), которые дополнительно добавляются к выбранному контексту';
''')

