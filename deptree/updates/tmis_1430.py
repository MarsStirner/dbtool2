# coding: utf-8
import csv
import os

from deptree.internals.base import DBToolBaseNode


class ClientDocumentUpdate(DBToolBaseNode):
    name = 'tmis-1430'
    depends = ['tmis-1430.client_document_add_country', 'tmis-1430.client_document_fill_country',
               'tmis-1430.client_document_add_region', 'tmis-1430.client_document_fill_region',
               'tmis-1430.client_document_add_country_region']


class ClientDocumentAddCountry(DBToolBaseNode):
    name = 'tmis-1430.client_document_add_country'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `rbCountry` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(8) NOT NULL COMMENT 'Код',
  `name` varchar(64) NOT NULL COMMENT 'Название',
  `idx` int(11) NOT NULL DEFAULT '0' COMMENT 'Индекс для сортировки в списке',
  PRIMARY KEY (`id`),
  KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Справочник cтран';
''')


class ClientDocumentFillCountry(DBToolBaseNode):
    name = 'tmis-1430.client_document_fill_country'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            cwd = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(cwd, 'data', 'tmis_1430_countries.csv')
            with open(file_path, 'r') as csv_file:
                c.executemany(u'''
INSERT INTO `rbCountry` (`code`,`name`,`idx`) VALUES (%s, %s, %s);
''', csv.reader(csv_file))


class ClientDocumentAddRegion(DBToolBaseNode):
    name = 'tmis-1430.client_document_add_region'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `rbRegion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(8) NOT NULL COMMENT 'Код',
  `name` varchar(64) NOT NULL COMMENT 'Название',
  `country_id` int(11) NOT NULL COMMENT 'Страна {rbCountry}',
  `idx` int(11) NOT NULL DEFAULT '0' COMMENT 'Индекс для сортировки в списке',
  PRIMARY KEY (`id`),
  KEY `code` (`code`),
  KEY `fk_country` (`country_id`),
  CONSTRAINT `fk_country` FOREIGN KEY (`country_id`) REFERENCES `rbCountry` (`id`) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Справочник регионов';
''')


class ClientDocumentFillRegion(DBToolBaseNode):
    name = 'tmis-1430.client_document_fill_region'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            cwd = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(cwd, 'data', 'tmis_1430_regions.csv')
            with open(file_path, 'r') as csv_file:
                c.execute(u'SELECT id FROM rbCountry WHERE code = "643";')
                id_russia = c.fetchone()[0]
                data = []
                for row in csv.reader(csv_file):
                    row.append(id_russia)
                    data.append(row)

                c.executemany(u'''
INSERT INTO `rbRegion` (`code`,`name`,`idx`,`country_id`) VALUES (%s, %s, %s, %s);
''', data)


class ClientDocumentAddCountryRegion(DBToolBaseNode):
    name = 'tmis-1430.client_document_add_country_region'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `ClientDocument`
    ADD COLUMN `country_id` INT(11) NULL DEFAULT NULL COMMENT 'Страна выдачи документа {rbCountry}',
    ADD COLUMN `region_id` INT(11) NULL DEFAULT NULL COMMENT 'Регион выдачи документа {rbRegion}';
''')
