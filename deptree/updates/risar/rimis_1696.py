# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class Rimis1696a(DBToolBaseNode):
    name = 'rimis-1696a'
    depends = [
        'rimis-1696.drop_profmed',
        'rimis-1696.profmed',
    ]


class Rimis1696(DBToolBaseNode):
    name = 'rimis-1696'
    depends = [
        'rimis-1696.drop_profmed',
        'rimis-1696.profmed',
        'rimis-1696.conditionmed',
    ]


class Spravochnik_rbProfMedHelpCleaner(DBToolBaseNode):
    name = 'rimis-1696.drop_profmed'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''drop table if exists rbProfMedHelp;''')


class Spravochnik_rbProfMedHelp(DBToolBaseNode):
    name = 'rimis-1696.profmed'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `rbProfMedHelp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(32) NOT NULL COMMENT 'Код',
  `name` varchar(255) NOT NULL COMMENT 'Наименование',
  `regionalCode` varchar(64) NOT NULL COMMENT 'Региональный код',
  `pr_det` int(11),
  `deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `code` (`code`),
  KEY `name` (`name`),
  KEY `regionalCode` (`regionalCode`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COMMENT='Справочник профессиональной медицинской помощи';
''')

            c.execute(u'''INSERT INTO rbProfMedHelp (code, name, regionalCode, pr_det) VALUES
('1', 'хирургии (абдоминальной)', '1', '2'),
('3', 'акушерскому делу', '3', '2'),
('4', 'аллергологии и иммунологии', '4', '2'),
('5', 'анестезиологии и реаниматологии', '5', '2'),
('6', 'бактериологии', '6', '2'),
('7', 'вирусологии', '7', '2'),
('8', 'военно-врачебной экспертизе', '8', '0'),
('10', 'врачебно-летной экспертизе', '10', '0'),
('11', 'гастроэнтерологии', '11', '2'),
('12', 'гематологии', '12', '2'),
('13', 'генетике', '13', '2'),
('14', 'гериатрии', '14', '0'),
('15', 'гистологии', '15', '2'),
('16', 'дерматовенерологии', '16', '2'),
('17', 'детской кардиологии', '17', '1'),
('18', 'детской онкологии', '18', '1'),
('19', 'детской урологии-андрологии', '19', '1'),
('20', 'детской хирургии', '20', '1'),
('21', 'детской эндокринологии', '21', '1'),
('22', 'диабетологии', '22', '2'),
('23', 'диетологии', '23', '2'),
('27', 'забору гемопоэтических стволовых клеток', '27', '2'),
('28', 'инфекционным болезням', '28', '2'),
('29', 'кардиологии', '29', '0'),
('30', 'колопроктологии', '30', '2'),
('34', 'клинической лабораторной диагностике', '34', '2'),
('35', 'клинической микологии', '35', '2'),
('36', 'клинической фармакологии', '36', '2'),
('37', 'лабораторному делу', '37', '2'),
('38', 'лабораторной диагностике', '38', '2'),
('39', 'лабораторной микологии', '39', '2'),
('40', 'лабораторной генетике', '40', '2'),
('41', 'лечебной физкультуре и спортивной медицине', '41', '2'),
('42', 'лечебному делу', '42', '2'),
('43', 'мануальной терапии', '43', '2'),
('45', 'медицинской генетике', '45', '2'),
('46', 'медицинскому массажу', '46', '2'),
('47', 'медицинской оптике', '47', '2'),
('48', 'медицинским осмотрам (предварительным, периодическим)', '48', '2'),
('49', 'медицинским осмотрам (предрейсовым, послерейсовым)', '49', '2'),
('50', 'медицинским осмотрам (предполетным, послеполетным)', '50', '2'),
('51', 'медицинской статистике', '51', '2'),
('53', 'неврологии', '53', '2'),
('54', 'нейрохирургии', '54', '2'),
('55', 'неонатологии', '55', '1'),
('56', 'нефрологии', '56', '2'),
('57', 'общей врачебной практике (семейной медицине)', '57', '2'),
('58', 'общей практике', '58', '2'),
('60', 'онкологии', '60', '0'),
('61', 'операционному делу', '61', '2'),
('62', 'организации сестринского дела', '62', '2'),
('63', 'ортодонтии', '63', '2'),
('65', 'офтальмологии', '65', '2'),
('66', 'паразитологии', '66', '2'),
('67', 'патологической анатомии', '67', '2'),
('68', 'педиатрии', '68', '1'),
('71', 'профпатологии', '71', '0'),
('72', 'психиатрии', '72', '2'),
('73', 'психиатрии-наркологии', '73', '2'),
('74', 'психотерапии', '74', '2'),
('75', 'пульмонологии', '75', '2'),
('76', 'радиологии', '76', '2'),
('77', 'ревматологии', '77', '2'),
('78', 'рентгенологии', '78', '2'),
('79', 'рефлексотерапии', '79', '2'),
('80', 'сексологии', '80', '2'),
('81', 'сердечно-сосудистой хирургии', '81', '2'),
('82', 'сестринскому делу', '82', '0'),
('83', 'сестринскому делу в педиатрии', '83', '1'),
('84', 'скорой медицинской помощи', '84', '2'),
('85', 'стоматологии', '85', '2'),
('86', 'стоматологии детской', '86', '1'),
('87', 'стоматологии профилактической', '87', '2'),
('88', 'стоматологии ортопедической', '88', '2'),
('89', 'стоматологии терапевтической', '89', '2'),
('90', 'стоматологии хирургической', '90', '2'),
('91', 'судебно-медицинской экспертизе', '91', '2'),
('93', 'судебно-медицинской экспертизе и исследованию трупа', '93', '2'),
('94', 'судебно-медицинской экспертизе и обследованию потерпевших, обвиняемых и других лиц', '94', '2'),
('95', 'судебно-психиатрической экспертизе', '95', '2'),
('96', 'сурдологии-оториноларингологии', '96', '2'),
('97', 'терапии', '97', '0'),
('98', 'токсикологии', '98', '2'),
('99', 'торакальной хирургии', '99', '2'),
('100', 'травматологии и ортопедии', '100', '2'),
('103', 'транспортировке гемопоэтических стволовых клеток и костного мозга', '103', '2'),
('104', 'транспортировке органов и (или) тканей человека для трансплантации', '104', '2'),
('105', 'трансфузиологии', '105', '2'),
('106', 'ультразвуковой диагностике', '106', '2'),
('107', 'управлению сестринской деятельностью', '107', '2'),
('108', 'урологии', '108', '2'),
('109', 'физиотерапии', '109', '2'),
('110', 'фтизиатрии', '110', '2'),
('111', 'функциональной диагностике', '111', '2'),
('112', 'хирургии', '112', '0'),
('113', 'хирургии (трансплантации органов и (или) тканей)', '113', '2'),
('114', 'хирургии (комбустиологии)', '114', '2'),
('115', 'хранению гемопоэтических стволовых клеток', '115', '2'),
('116', 'челюстно-лицевой хирургии', '116', '2'),
('117', 'экспертизе временной нетрудоспособности', '117', '2'),
('120', 'экспертизе профессиональной пригодности', '120', '0'),
('121', 'экспертизе связи заболеваний с профессией', '121', '0'),
('122', 'эндокринологии', '122', '0'),
('123', 'эндоскопии', '123', '2'),
('135', 'авиационной и космической медицине', '135', '2'),
('136', 'акушерству и гинекологии (за исключением использования вспомогательных репродуктивных технологий)', '136', '2'),
('137', 'акушерству и гинекологии (использованию вспомогательных репродуктивных технологий)', '137', '2'),
('138', 'вакцинации (проведению профилактических прививок)', '138', '2'),
('139', 'водолазной медицине', '139', '2'),
('140', 'гигиене в стоматологии', '140', '2'),
('141', 'гигиеническому воспитанию', '141', '2'),
('142', 'дезинфектологии', '142', '2'),
('143', 'забору, криоконсервации и хранению половых клеток и тканей репродуктивных органов', '143', '2'),
('144', 'заготовке, хранению донорской крови и (или) ее компонентов', '144', '2'),
('145', 'изъятию и хранению органов и (или) тканей человека для трансплантации', '145', '2'),
('146', 'косметологии', '146', '2'),
('147', 'лечебной физкультуре', '147', '2'),
('148', 'медико-социальной экспертизе', '148', '2'),
('149', 'медико-социальной помощи', '149', '2'),
('150', 'медицинским осмотрам (предсменным, послесменным)', '150', '2'),
('151', 'медицинским осмотрам профилактическим', '151', '2'),
('152', 'медицинскому освидетельствованию кандидатов в усыновители, опекуны (попечители) или приемные родители', '152', '2'),
('153', 'медицинскому освидетельствованию на выявление ВИЧ-инфекции', '153', '2'),
('154', 'медицинскому освидетельствованию на наличие инфекционных заболеваний, представляющих опасность для окружающих и являющихся основанием для отказа иностранным гражданам и лицам без гражданства в выдаче либо аннулировании разрешения на временное проживание,', '154', '2'),
('155', 'медицинскому освидетельствованию на наличие медицинских противопоказаний к управлению транспортным средством', '155', '2'),
('156', 'медицинскому освидетельствованию на наличие медицинских противопоказаний к владению оружием', '156', '2'),
('157', 'медицинскому освидетельствованию на состояние опьянения (алкогольного, наркотического или иного токсического)', '157', '2'),
('158', 'медицинской реабилитации', '158', '2'),
('159', 'наркологии', '159', '2'),
('160', 'неотложной медицинской помощи', '160', '2'),
('161', 'организации здравоохранения и общественному здоровью', '161', '2'),
('162', 'оториноларингологии (за исключением кохлеарной имплантации)', '162', '2'),
('163', 'оториноларингологии (кохлеарной имплантации)', '163', '2'),
('164', 'пластической хирургии', '164', '2'),
('165', 'психиатрическому освидетельствованию', '165', '2'),
('166', 'радиотерапии', '166', '2'),
('167', 'реаниматологии', '167', '2'),
('168', 'рентгенэндоваскулярной диагностике и лечению', '168', '2'),
('169', 'санитарно-гигиеническим лабораторным исследованиям', '169', '2'),
('170', 'сестринскому делу в косметологии', '170', '2'),
('171', 'стоматологии общей практики', '171', '2'),
('172', 'судебно-медицинской экспертизе вещественных доказательств и исследованию биологических объектов (биохимической, генетической, медико-криминалистической, спектрографической, судебно-биологической, судебно-гистологической, судебно-химической, судебно-цитол', '172', '2'),
('173', 'однородной амбулаторной судебно-психиатрической экспертизе', '173', '2'),
('174', 'комплексной амбулаторной судебно-психиатрической экспертизе', '174', '2'),
('175', 'однородной стационарной судебно-психиатрической экспертизе', '175', '2'),
('176', 'комплексной стационарной судебно-психиатрической экспертизе (психолого-психиатрической, сексолого-психиатрической)', '176', '2'),
('177', 'трансплантации костного мозга и гемопоэтических стволовых клеток', '177', '2'),
('178', 'транспортировке половых клеток и (или) тканей репродуктивных органов', '178', '2'),
('179', 'хирургии (трансплантации органов и (или) тканей)', '179', '2'),
('180', 'экспертизе качества медицинской помощи', '180', '2'),
('181', 'энтомологии', '181', '2'),
('182', 'эпидемиологии', '182', '2'),
('2', 'акушерству и гинекологии', '2', '2'),
('9', 'восстановительной медицине', '9', '2'),
('24', 'забору, хранению донорской спермы', '24', '0'),
('25', 'забору, хранению органов и тканей человека для трансплантации', '25', '2'),
('26', 'забору, заготовке, хранению донорской крови и ее компонентов', '26', '2'),
('31', 'контролю качества медицинской помощи', '31', '2'),
('32', 'косметологии (терапевтической)', '32', '2'),
('33', 'косметологии (хирургической)', '33', '2'),
('44', 'медицинской биохимии', '44', '2'),
('52', 'медицинскому (наркологическому) освидетельствованию', '52', '2'),
('59', 'общественному здоровью и организации здравоохранения', '59', '2'),
('64', 'оториноларингологии', '64', '2'),
('69', 'применению клеточных технологий', '69', '2'),
('70', 'применению методов традиционной медицины', '70', '2'),
('92', 'судебно-медицинской экспертизе вещественных доказательств и исследованию биологических объектов', '92', '2'),
('101', 'транспортировке донорской крови и ее компонентов', '101', '2'),
('102', 'транспортировке донорской спермы', '102', '0'),
('118', 'экспертизе на право владения оружием', '118', '0'),
('119', 'экспертизе наркологической', '119', '2'),
('124', 'гнойной хирургии', '124', '2'),
('125', 'гемодиализа', '125', '2'),
('126', 'химеотерапии', '126', '2'),
('127', 'патологии беременности', '127', '2'),
('128', 'для беременных и рожениц', '128', '2'),
('129', 'для производства абортов', '129', '2'),
('130', 'травматологии', '130', '2'),
('131', 'ортопедии', '131', '2'),
('132', 'посещения среднего медицинского персонала, ведущего самостоятельный прием', '132', '2'),
('133', 'сосудистой хирургии', '133', '2'),
('134', 'приёмного отделения', '134', '2')
''')


class rbConditionMedHelp(DBToolBaseNode):
    name = 'rimis-1696.conditionmed'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `rbConditionMedHelp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(32) NOT NULL COMMENT 'Код',
  `name` varchar(64) NOT NULL COMMENT 'Наименование',
  `deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `code` (`code`),
  KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8 COMMENT='Условия оказания медицинской помощи '
''')
            c.execute(u''' INSERT INTO rbConditionMedHelp (code, name) VALUES
            ('stationary', 'Стационарно'),
            ('day_stationary', 'В дневном стационаре'),
            ('ambulatorno', 'Амбулаторно'),
            ('outof_medhelp', 'Вне медицинской организации')
            ''')