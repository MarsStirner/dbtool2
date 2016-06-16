# coding: utf-8

from deptree. internals.base import DBToolBaseNode


class RsrRadzinskyUpdate(DBToolBaseNode):
    name = 'rimis-682'
    depends = ['rimis-682.1', 'rimis-1110.1']


class RadzinskyRisksCreateTables(DBToolBaseNode):
    name = 'rimis-682.1'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `rbRadzinskyRiskRate` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(16) NOT NULL,
  `name` VARCHAR(64) NOT NULL,
  `value` INT(11) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'Степень риска по шкале Радзинского';
''')

            rrr_data = [
                ('low', 'Низкая', '1'),
                ('medium', 'Средняя', '2'),
                ('high', 'Высокая', '3')
            ]
            c.executemany(u'''
INSERT INTO `rbRadzinskyRiskRate` (`code`, `name`, `value`) VALUES (%s, %s, %s);
''', rrr_data)

            c.execute(u'''
CREATE TABLE `rbRadzRiskFactorGroup` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(32) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'Группа факторов риска по Радзинскому';
''')

            rrfg_data = [
                ('01','Социально-биологические факторы'),
                ('02','Акушерско-гинекологический анамнез'),
                ('03','Экстрагенитальные заболевания матери'),
                ('04','Осложнения беременности'),
                ('05','Скрининг'),
                ('06','Оценка состояния плода'),
                ('07','Интранатальные осложнения')
            ]
            c.executemany(u'''
INSERT INTO `rbRadzRiskFactorGroup` (`code`,`name`) VALUES (%s, %s);
''', rrfg_data)

            c.execute(u'''
CREATE TABLE `rbRadzStage` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(32) NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'Этап определения риска по Радзинскому';
''')

            rs_data = [
                ('anamnestic','Анамнестические факторы'),
                ('before32','Факторы до 32 недель'),
                ('after33','Факторы после 33 недель'),
                ('intranatal','Интранатальные факторы')
            ]
            c.executemany(u'''
INSERT INTO `rbRadzStage` (`code`,`name`) VALUES (%s, %s);
''', rs_data)

            c.execute(u'''
CREATE TABLE `rbRadzRiskFactor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(64) NOT NULL,
  `name` varchar(512) NOT NULL,
  `group_id` int(11) NOT NULL COMMENT '{rbRadzRiskFactorGroup}',
  PRIMARY KEY (`id`),
  KEY `fk_rbradzriskfactor_group_idx` (`group_id`),
  CONSTRAINT `fk_rbradzriskfactor_group` FOREIGN KEY (`group_id`) REFERENCES `rbRadzRiskFactorGroup` (`id`) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Фактор риска по Радзинскому';
''')
            rrf_data = [
                ("mother_younger_18", u"Мать моложе 18 лет",1),
                ("mother_older_40", u"Мать 40 лет и старше",1),
                ("father_older_40", u"Возраст отца 40 лет и более",1),
                ("mother_professional_properties", u"Профессиональные вредности у матери",1),
                ("father_professional_properties", u"Профессиональные вредности у отца",1),
                ("mother_smoking", u"Вредные привычки у матери: курение (одна пачка сигарет в день)",1),
                ("mother_alcohol", u"Вредные привычки у матери:  злоупотребление алкоголем",1),
                ("father_alcohol", u"Вредные привычки у отца: злоупотребление алкоголем",1),
                ("emotional_stress", u"Эмоциональная нагрузка у матери",1),
                ("height_less_150", u"Рост матери 150 см и менее",1),
                ("overweight", u"Масса тела матери на 25% выше нормы",1),
                ("not_married", u"Семейное положение: одинокая",1),
                ("parity_under_7", u"Паритет (число предшествующих родов): 4-7",2),
                ("parity_above_8", u"Паритет (число предшествующих родов):  8 и более",2),
                ("abortion_1", u"Аборты перед родами у первородящих: один",2),
                ("abortions_2", u"Аборты перед родами у первородящих: два",2),
                ("abortions_more_3", u"Аборты перед родами у первородящих: три и более",2),
                ("abortion_after_last_delivery_more_3", u"Аборты перед повторными родами или после последних родов: 3 и более",2),
                ("intrauterine_operations", u"Внутриматочные вмешательства",2),
                ("premature_birth_1", u"Преждевременные роды: 1",2),
                ("premature_birth_more_2", u"Преждевременные роды: 2 и более   3",2),
                ("miscarriage_1", u"Мертворождение, невынашивание, неразвивающаяся беременность: 1",2),
                ("miscarriage_more_2", u"Мертворождение, невынашивание, неразвивающаяся беременность: 2 и более",2),
                ("child_death_1", u"Смерть детей в неонатальном периоде: одного ребенка",2),
                ("child_death_more_2", u"Смерть детей в неонатальном периоде: двух и более детей",2),
                ("congenital_disorders", u"Аномалии развития у детей",2),
                ("neurological_disorders", u"Неврологические нарушения у детей",2),
                ("abnormal_child_weight", u"Масса тела доношенных детей менее 2500 г или 4000 г и более",2),
                ("infertility_less_4", u"Бесплодие: 2-4 года",2),
                ("infertility_more_5", u"Бесплодие: 5 лет и более",2),
                ("uterine_scar", u"Рубец на матке после операции",2),
                ("uterus_oophoron_tumor", u"Опухоли матки и яичников",2),
                ("insuficiencia_istmicocervical", u"Истмико-цервикальная недостаточность",2),
                ("uterine_malformations", u"Пороки развития матки",2),
                ("chronic_inflammation", u"Хронические воспалительные процессы, воспаление придатков, осложнения после абортов и родов, внутриматочный контрацептив",2),
                ("tubal_pregnancy", u"Внематочная беременность",2),
                ("extracorporal_fertilization", u"Вспомогательные репродуктивные технологии: ЭКО",2),
                ("intracytoplasmic_sperm_injection", u"Вспомогательные репродуктивные технологии:  ИКСИ",2),
                ("heart_disease", u"Пороки сердца без нарушения кровообращения",3),
                ("heart_disease_circulatory_embarrassment", u"Пороки сердца с нарушением кровообращения",3),
                ("hypertensive_disease_1", u"Гипертоническая болезнь I стадий",3),
                ("hypertensive_disease_2", u"Гипертоническая болезнь II стадий",3),
                ("hypertensive_disease_3", u"Гипертоническая болезнь III стадий",3),
                ("varicose", u"Варикозная болезнь",3),
                ("hypotensive_syndrome", u"Гипотензивный синдром",3),
                ("renal_disease", u"Заболевания почек",3),
                ("adrenal_disorders", u"Заболевания надпочечников",3),
                ("neurometabolic_endocrine_syndrome", u"НОЭС",3),
                ("diabetes", u"Сахарный диабет",3),
                ("thyroid_disorders", u"Заболевания щитовидной железы",3),
                ("obesity", u"Ожирение",3),
                ("anemia_90", u"Анемия: содержание гемоглобина 90 г/л",3),
                ("anemia_100", u"Анемия: содержание гемоглобина 100 г/л",3),
                ("anemia_110", u"Анемия: содержание гемоглобина 110 г/л",3),
                ("coagulopathy",  u"Коагулопатии",3),
                ("myopia", u"Миопия и другие заболевания глаз",3),
                ("persistent_infection", u"Хронические инфекции (туберкулез, бруцеллез, сифилис, токсоплазмоз и др.)",3),
                ("lupus_anticoagulant_positive", u"Положительная реакция на волчаночный антикоагулянт",3),
                ("antiphospholipid_antibodies_IgG", u"Антитела к фосфолипидам: IgG от 9,99 и выше",3),
                ("antiphospholipid_antibodies_IgM", u"Антитела к фосфолипидам:  IgM от 9,99 и выше",3),
                ("early_pregnancy_toxemia", u"Выраженный ранний токсикоз беременных",4),
                ("recurrent_threatened_miscarriage", u"Рецидивирующая угроза прерывания",4),
                ("edema_disease", u"Отёки беременных",4),
                ("gestosis_mild_case", u"Гестоз легкой степени",4),
                ("gestosis_moderately_severe", u"Гестоз средней степени",4),
                ("gestosis_severe", u"Гестоз тяжелой степени",4),
                ("preeclampsia", u"Преэклампсия",4),
                ("eclampsia", u"Эклампсия",4),
                ("renal_disease_exacerbation", u"Обострение заболевания почек при беременности",4),
                ("emerging_infection_diseases", u"Острые инфекции при беременности, в т.ч. острые респираторно-вирусные",4),
                ("bleeding_1", u"Кровотечение: в первой половине беременности",4),
                ("bleeding_2", u"Кровотечение: во второй половине беременности",4),
                ("Rh_hypersusceptibility", u"Резус-изосенсибилизация",4),
                ("ABO_hypersusceptibility", u"АВO-изосенсибилизация",4),
                ("hydramnion", u"Многоводие",4),
                ("oligohydramnios", u"Маловодие",4),
                ("pelvic_station", u"Тазовое предлежание плода, крупный плод, узкий таз",4),
                ("multiple_pregnancy", u"Многоплодие",4),
                ("prolonged_pregnancy", u"Переношенная беременность",4),
                ("abnormal_fetus_position", u"Неправильное положение плода (поперечное, косое)",4),
                ("maternal_passages_immaturity", u"Биологическая незрелость родовых путей в 40 недель беременности",4),
                ("beta_HCG_increase", u"Бета-ХГЧ: повышение содержания",5),
                ("beta_HCG_decrease", u"Бета-ХГЧ: снижение содержания",5),
                ("alpha_fetoprotein_increase", u"АФП: повышение содержания",5),
                ("alpha_fetoprotein_decrease", u"АФП: снижение содержания",5),
                ("PAPP_A_increase", u"PAPP-A: повышение содержания",5),
                ("PAPP_A_decrease", u"PAPP-A: снижение содержания",5),
                ("small_gestational_age_fetus_1", u"Гипотрофия плода: 1 степени",6),
                ("small_gestational_age_fetus_2", u"Гипотрофия плода: 2 степени",6),
                ("small_gestational_age_fetus_3", u"Гипотрофия плода: 3 степени",6),
                ("chronical_placental_insufficiency", u"Хроническая плацентарная недостаточность",6),
                ("cardiotocography_more_7", u"Оценка КТГ по шкале Fisher W.M. (баллы):  >7",6),
                ("cardiotocography_6", u"Оценка КТГ по шкале Fisher W.M. (баллы): 6",6),
                ("cardiotocography_5", u"Оценка КТГ по шкале Fisher W.M. (баллы): 5",6),
                ("cardiotocography_4", u"Оценка КТГ по шкале Fisher W.M. (баллы): 4",6),
                ("cardiotocography_less_4", u"Оценка КТГ по шкале Fisher W.M. (баллы):  <4",6),
                ("meconium_amniotic_fluid", u"Мекониальная окраска амниотических вод",7),
                ("predelivery_amniorrhea_before_labour", u"Дородовое излитие вод (при отсутствии родовой деятельности в течение 6 ч)",7),
                ("pathological_preliminary_period", u"Патологический прелиминарный период",7),
                ("labour_anomaly", u"Аномалии родовой деятельности",7),
                ("chorioamnionitis", u"Хориоамнионит",7)
            ]
            c.executemany(u'''
INSERT INTO `rbRadzRiskFactor` (`code`, `name`, `group_id`)
VALUES (%s, %s, %s);
''', rrf_data)

            c.execute(u'''
CREATE TABLE `rbRadzRiskFactor_Stage` (
  `factor_id` int(11) NOT NULL COMMENT '{rbRadzRiskFactor}',
  `stage_id` int(11) NOT NULL COMMENT '{rbRadzStage}',
  `points` int(11) NOT NULL COMMENT 'Число баллов',
  PRIMARY KEY (`factor_id`,`stage_id`),
  KEY `fk_rbradzriskfactor_stage_factor_idx` (`factor_id`),
  KEY `fk_rbradzriskfactor_stage_stage_idx` (`stage_id`),
  CONSTRAINT `fk_rbradzriskfactor_stage_factor` FOREIGN KEY (`factor_id`) REFERENCES `rbRadzRiskFactor` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_rbradzriskfactor_stage_stage` FOREIGN KEY (`stage_id`) REFERENCES `rbRadzStage` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Связь фактора риска с этапами по Радзинскому';
''')
            rrfs_data = [
                (1,1,2),
                (2,1,4),
                (3,1,2),
                (4,1,3),
                (5,1,3),
                (6,1,2),
                (7,1,4),
                (8,1,2),
                (9,1,1),
                (10,1,2),
                (11,1,2),
                (12,1,1),
                (13,1,1),
                (14,1,2),
                (15,1,2),
                (16,1,3),
                (17,1,4),
                (18,1,2),
                (19,1,2),
                (20,1,2),
                (21,1,3),
                (22,1,3),
                (23,1,8),
                (24,1,2),
                (25,1,7),
                (26,1,3),
                (27,1,2),
                (28,1,2),
                (29,1,2),
                (30,1,4),
                (31,1,4),
                (32,1,4),
                (33,1,2),
                (34,1,3),
                (35,1,3),
                (36,1,3),
                (37,1,1),
                (38,1,2),
                (39,1,3),
                (40,1,10),
                (41,1,2),
                (42,1,8),
                (43,1,12),
                (44,1,2),
                (45,1,2),
                (46,1,4),
                (47,1,5),
                (48,1,10),
                (49,1,10),
                (50,1,7),
                (51,1,2),
                (52,1,4),
                (53,1,2),
                (54,1,1),
                (55,1,2),
                (56,1,2),
                (57,1,3),
                (58,1,4),
                (59,1,2),
                (60,1,3),
                (61,2,2),
                (61,3,2),
                (62,2,2),
                (62,3,2),
                (63,2,2),
                (63,3,2),
                (64,2,3),
                (64,3,3),
                (65,2,5),
                (65,3,5),
                (66,2,10),
                (66,3,10),
                (67,2,11),
                (67,3,11),
                (68,2,12),
                (68,3,12),
                (69,2,4),
                (69,3,4),
                (70,2,2),
                (70,3,2),
                (71,2,3),
                (71,3,3),
                (72,2,5),
                (72,3,5),
                (73,2,5),
                (73,3,5),
                (74,2,10),
                (74,3,10),
                (75,2,3),
                (75,3,3),
                (76,2,4),
                (76,3,4),
                (77,2,3),
                (77,3,3),
                (78,2,3),
                (78,3,3),
                (79,2,3),
                (79,3,3),
                (80,2,3),
                (80,3,3),
                (81,3,4),
                (82,2,3),
                (82,3,3),
                (83,2,3),
                (83,3,3),
                (84,2,6),
                (84,3,6),
                (85,2,8),
                (85,3,8),
                (86,2,2),
                (86,3,2),
                (87,2,3),
                (87,3,3),
                (88,2,10),
                (88,3,10),
                (89,2,15),
                (89,3,15),
                (90,2,20),
                (90,3,20),
                (91,2,4),
                (91,3,4),
                (92,2,4),
                (92,3,4),
                (93,2,8),
                (93,3,8),
                (94,2,12),
                (94,3,12),
                (95,2,16),
                (95,3,16),
                (96,2,20),
                (96,3,20),
                (97,4,8),
                (98,4,6),
                (99,4,4),
                (100,4,10),
                (101,4,4)
            ]
            c.executemany(u'''
INSERT INTO `rbRadzRiskFactor_Stage` (`factor_id`, `stage_id`, `points`)
VALUES (%s, %s, %s);
''', rrfs_data)

            c.execute(u'''
CREATE TABLE `RisarRadzinskyRisks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `createDatetime` datetime NOT NULL,
  `createPerson_id` int(11) DEFAULT NULL,
  `modifyDatetime` datetime NOT NULL,
  `modifyPerson_id` int(11) DEFAULT NULL,
  `event_id` int(11) NOT NULL,
  `anamnestic_points` int(11) DEFAULT NULL COMMENT 'Сумма баллов анамнестических факторов',
  `before32week_points` int(11) DEFAULT NULL COMMENT 'Сумма баллов до 32 недель <=',
  `after33week_points` int(11) DEFAULT NULL COMMENT 'Сумма баллов после 33 недель >=',
  `intranatal_points` int(11) DEFAULT NULL COMMENT 'Сумма баллов интранатальных факторов',
  `before32week_totalpoints` int(11) DEFAULT NULL COMMENT 'Общая сумма баллов факторов до 32 недель',
  `after33week_totalpoints` int(11) DEFAULT NULL COMMENT 'Общая сумма баллов факторов после 33 недель',
  `intranatal_totalpoints` int(11) DEFAULT NULL COMMENT 'Общая сумма баллов с учётом интранатальных факторов',
  `intranatal_growth` double DEFAULT NULL COMMENT 'Интранатальный прирост, %',
  `risk_rate_id` int(11) DEFAULT NULL COMMENT 'Итоговая степень риска {rbRadzinskyRiskRate}',
  PRIMARY KEY (`id`),
  KEY `fk_risarradzinskyrisks_event_idx` (`event_id`),
  KEY `fk_risarradzinskyrisks_createperson_idx` (`createPerson_id`),
  KEY `fk_risarradzinskyrisks_modifyperson_idx` (`modifyPerson_id`),
  KEY `fk_risarradzinskyrisks_riskrate_idx` (`risk_rate_id`),
  CONSTRAINT `fk_risarradzinskyrisks_createperson` FOREIGN KEY (`createPerson_id`) REFERENCES `Person` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_risarradzinskyrisks_event` FOREIGN KEY (`event_id`) REFERENCES `Event` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_risarradzinskyrisks_modifyperson` FOREIGN KEY (`modifyPerson_id`) REFERENCES `Person` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_risarradzinskyrisks_riskrate` FOREIGN KEY (`risk_rate_id`) REFERENCES `rbRadzinskyRiskRate` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Рассчитанные риски по шкале Радзинского для случая';
''')

            c.execute(u'''
CREATE TABLE `RisarRadzinskyRisks_Factors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `risk_id` int(11) NOT NULL COMMENT '{RisarRadzinskyRisks}',
  `risk_factor_id` int(11) NOT NULL COMMENT '{rbRadzRiskFactor}',
  `stage_id` int(11) NOT NULL COMMENT '{rbRadzStage}',
  PRIMARY KEY (`id`),
  KEY `fk_risarradzinskyrisks_factors_risk_idx` (`risk_id`),
  KEY `fk_risarradzinskyrisks_factors_factor_code_idx` (`risk_factor_id`),
  KEY `fk_risarradzinskyrisks_factors_stage_idx` (`stage_id`),
  CONSTRAINT `fk_risarradzinskyrisks_factors_factor` FOREIGN KEY (`risk_factor_id`) REFERENCES `rbRadzRiskFactor` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_risarradzinskyrisks_factors_risk` FOREIGN KEY (`risk_id`) REFERENCES `RisarRadzinskyRisks` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_risarradzinskyrisks_factors_stage` FOREIGN KEY (`stage_id`) REFERENCES `rbRadzStage` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Сработавшие факторы риска по шкале Радзинского для случая';
''')


class FetusFisherKtgFields(DBToolBaseNode):
    name = 'rimis-1110.1'
    depends = ['rimis-797.2']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `rbFisherKTGRate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(32) NOT NULL,
  `name` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Оценка КТГ по Фишеру';
''')

            fr_data = [
                ('normality', u'Состояние в норме'),
                ('prepathological', u'Предпатологическое состояние'),
                ('attention_required', u'Состояние требует повышенного внимания')
            ]
            c.executemany(u'''
INSERT INTO `rbFisherKTGRate` (`code`,`name`) VALUES (%s, %s);
''', fr_data)

            c.execute(u'''
ALTER TABLE `RisarFetusState`
  ADD COLUMN `fisher_ktg_points` INT(11) NULL DEFAULT NULL COMMENT 'сумма баллов по значениям атрибутов раздела КТГ' AFTER `deleted`,
  ADD COLUMN `fisher_ktg_rate_id` INT(11) NULL DEFAULT NULL COMMENT 'сумма баллов по значениям атрибутов раздела КТГ' AFTER `fisher_ktg_points`
''')

            c.execute(u'''
ALTER TABLE `RisarFetusState`
  ADD CONSTRAINT `fk_risarfetusstate_rbfisherktgrate` FOREIGN KEY (`fisher_ktg_rate_id`) REFERENCES `rbFisherKTGRate` (`id`)
    ON UPDATE CASCADE ON DELETE RESTRICT;
''')