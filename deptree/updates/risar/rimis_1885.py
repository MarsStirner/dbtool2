# coding: utf-8

from deptree.internals.base import DBToolBaseNode


class RegionalRisksTambov(DBToolBaseNode):
    name = 'rimis-1885'
    depends = ['rimis-1885.regional_common', 'rimis-1885.new_factors_from_tomsk', 'rimis-1885.regional_tomsk']


class RegionalRisksCommonTables(DBToolBaseNode):
    name = 'rimis-1885.regional_common'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `rbRisarRegionalRiskRate` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(16) NOT NULL,
  `name` VARCHAR(64) NOT NULL,
  `value` INT(11) NOT NULL,
  `regionalCode` VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'региональный код',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'Степень риска по региональной шкале';
''')

            c.execute(u'''
CREATE TABLE `rbRegionalRiskStage` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(32) NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'Этап определения регионального риска';
''')

            # regional factor group
            c.execute(u'''
ALTER TABLE `rbRadzRiskFactor`
DROP FOREIGN KEY `fk_rbradzriskfactor_group`;''')

            c.execute(u'''
ALTER TABLE `rbRadzRiskFactor`
CHANGE COLUMN `group_id` `group_id` INT(11) NULL DEFAULT NULL COMMENT '{rbRadzRiskFactorGroup} группа для шкалы Радзинского',
ADD COLUMN `regional_group_id` INT(11) NULL DEFAULT NULL COMMENT '{rbRadzRiskFactorGroup} группа для региональной шкалы' AFTER `group_id`,
COMMENT = 'Факторы риска по Радзинскому и факторы риска для региональных шкал' ;''')

            c.execute(u'''
ALTER TABLE `rbRadzRiskFactor`
ADD CONSTRAINT `fk_rbradzriskfactor_group`
  FOREIGN KEY (`group_id`)
  REFERENCES `rbRadzRiskFactorGroup` (`id`)
  ON UPDATE CASCADE ON DELETE RESTRICT;
''')

            c.execute(u'''
ALTER TABLE `rbRadzRiskFactor`
ADD UNIQUE INDEX `unique_code_idx` (`code` ASC);
''')

            c.execute(u'''
ALTER TABLE `rbRadzRiskFactor`
ADD CONSTRAINT `fk_rbradzriskfactor_regional_group`
  FOREIGN KEY (`regional_group_id`)
  REFERENCES `rbRadzRiskFactorGroup` (`id`)
  ON UPDATE CASCADE ON DELETE RESTRICT;
''')

            # regional factor stage
            c.execute(u'''
CREATE TABLE `rbRadzRiskFactor_RegionalStage` (
  `factor_id` int(11) NOT NULL COMMENT '{rbRadzRiskFactor}',
  `stage_id` int(11) NOT NULL COMMENT '{rbRegionalRiskStage}',
  `points` int(11) NOT NULL COMMENT 'Число баллов',
  PRIMARY KEY (`factor_id`,`stage_id`),
  KEY `fk_rbradzriskfactor_regstage_factor_idx` (`factor_id`),
  KEY `fk_rbradzriskfactor_regstage_stage_idx` (`stage_id`),
  CONSTRAINT `fk_rbradzriskfactor_regstage_factor` FOREIGN KEY (`factor_id`) REFERENCES `rbRadzRiskFactor` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_rbradzriskfactor_regstage_stage` FOREIGN KEY (`stage_id`) REFERENCES `rbRegionalRiskStage` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Связь фактора риска с этапами по региональной шкале';
''')

            # regional risk rate
            c.execute(u'''
CREATE TABLE `RisarRegionalRiskRate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) NOT NULL,
  `risk_rate_id` int(11) DEFAULT NULL COMMENT 'Итоговая степень риска {rbRisarRegionalRiskRate}',
  PRIMARY KEY (`id`),
  KEY `fk_risarregriskrate_event_idx` (`event_id`),
  KEY `fk_risarregriskrate_riskrate_idx` (`risk_rate_id`),
  CONSTRAINT `fk_risarregriskrate_event` FOREIGN KEY (`event_id`) REFERENCES `Event` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_risarregriskrate_riskrate` FOREIGN KEY (`risk_rate_id`) REFERENCES `rbRisarRegionalRiskRate` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Степень риска по региональной шкале для случая';
''')


class RegionalNewFactorsFromTomsk(DBToolBaseNode):
    name = 'rimis-1885.new_factors_from_tomsk'
    depends = ['rimis-1885.regional_common']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            rrf_data = [
                ("mother_drugs", u"Вредные привычки у матери: приём наркотиков"),
                ("father_drugs", u"Вредные привычки у отца: приём наркотиков"),
                ("height_less_155", u"Рост 155 см и менее"),
                ("parity_above_4", u"Паритет: 4 родов и более"),
                ("abortion_first_trimester", u"Аборты, выкидыши в 1 триместре беременности"),
                ("premature_birth_second_trimester", u"Преждевременные роды, выкидыши во II триместре беременности"),
                ("preeclampsia_anamnesis", u"Преэклампсия в анамнезе"),
                ("miscarriage", u"Мертворождение"),
                ("child_death", u"Смерть детей в неонатальном периоде"),
                ("infertility", u"Бесплодие"),
                ("assisted_reproductive_technology", u"Беременность после ВРТ"),
                ("uterine_scar_1", u"Один рубец на матке после операции"),
                ("uterine_scar_more_2", u"Два и более рубца на матке после операции"),
                ("chronic_inflammation_tomsk", u"Хронические воспалительные процессы"),
                ("adnexal_affection", u"Воспаление придатков"),
                ("birth_complications", u"Осложнения после абортов и родов"),
                ("intrauterine_contraception", u"Внутриматочный контрацептив"),
                ("threatened_miscarriage", u"Угроза прерывания беременности"),
                ("cervix_uteri_length_less_25", u"Длина шейки матки менее 25 мм"),
                ("hellp", u"HELLP-синдром"),
                ("hydramnion_moderate", u"Многоводие умеренное"),
                ("hydramnion_hard", u"Многоводие тяжелое"),
                ("oligohydramnios_moderate", u"Маловодие умеренное"),
                ("oligohydramnios_hard", u"Маловодие тяжелое"),
                ("multiple_pregnancy_2", u"Многоплодие. Беременность двойней"),
                ("multiple_pregnancy_3", u"Многоплодие. Беременность тройней"),
                ("fetal", u"Фето-фетальный синдром"),
                ("central_placental_presentation", u"Центральное предлежание плаценты"),
                ("low_insertion_of_placenta", u"Низкое расположение плаценты, подтвержденное УЗИ в сроке гестации 34-36 недель"),
                ("pregnancy_after_corrective_surgery", u"Беременность после реконструктивно-пластических операций на половых органах, разрывах промежности III-IV степени"),
                ("pneumology", u"Заболевания органов дыхания без дыхательной недостаточности"),
                ("respiratory_disturbance", u"Заболевания органов дыхания с дыхательной недостаточностью"),
                ("thrombosis", u"тромбозы, тромбоэмболии и тромбофлебиты в анамнезе и при настоящей беременности"),
                ("glomerulonephritis", u"гломерулонефрит"),
                ("solitary_paired", u"единственная почка"),
                ("weight_deficit", u"Эндокринопатии: дефицит массы тела"),
                ("anemia_70", u"Анемия: содержание гемоглобина 70 г/л"),
                ("thrombocytopenia", u"Тромбоцитопения"),
                ("nervous_disorder", u"Заболевания нервной системы (эпилепсия, рассеяный склероз, нарушения мозгового кровообращения) в анамнезе"),
                ("malignant_tumor", u"Злокачественные новообразования в анамнезе либо выявленные во время беременности"),
                ("aneurysm", u"Сосудистые мальформации, аневризмы сосудов"),
                ("trauma", u"Перенесенные в анамнезе травмы позвоночника, таза"),
                ("small_gestational_age_fetus_2plus", u"Задержка внутриутробного роста плода 2-3 степени"),
                ("developmental_defect", u"Выявленные пороки развития плода"),
                ("placental_perfusion_disorder_1", u"Нарушение маточно-плацентарного кровотока I степени"),
                ("placental_perfusion_disorder_2", u"Нарушение маточно-плацентарного кровотока II степени"),
                ("placental_perfusion_disorder_3", u"Нарушение маточно-плацентарного кровотока III степени"),
                ("pelvic_station_common", u"Тазовое предлежание плода"),
            ]
            c.executemany(u'''
INSERT INTO `rbRadzRiskFactor` (`code`, `name`)
VALUES (%s, %s);
''', rrf_data)

            # some renames
            sql_rename = u'''UPDATE rbRadzRiskFactor SET name = %s WHERE code = %s '''
            for code, name in (
                    ('hypertensive_disease_1', u'хроническая артериальная гипертензия I стадии'),
                    ('hypertensive_disease_2', u'хроническая артериальная гипертензия II стадии'),
                    ('hypertensive_disease_3', u'хроническая артериальная гипертензия III стадии'),
                    ('small_gestational_age_fetus_1', u'Задержка внутриутробного роста плода 1 степени'),
                    ('small_gestational_age_fetus_2', u'Задержка внутриутробного роста плода 2 степени'),
                    ('small_gestational_age_fetus_3', u'Задержка внутриутробного роста плода 3 степени')):
                c.execute(sql_rename, (name, code))


class RegionalRisksTomsk(DBToolBaseNode):
    name = 'rimis-1885.regional_tomsk'
    depends = ['rimis-1885.regional_common', 'rimis-1885.new_factors_from_tomsk']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
#             rrr_data = [
#                 ('low', 'Низкая', '1'),
#                 ('medium', 'Средняя', '2'),
#                 ('high', 'Высокая', '3')
#             ]
#             c.executemany(u'''
# INSERT INTO `rbRisarRegionalRiskRate` (`code`, `name`, `value`) VALUES (%s, %s, %s);
# ''', rrr_data)
#
#             rs_data = [
#                 ('initial', 'Факторы при постановке на учет'),
#                 ('before21', 'Факторы в 20 недель'),
#                 ('from21to30', 'Факторы в 30 недель'),
#                 ('from31to36', 'Факторы в 36 недель')
#             ]
#             c.executemany(u'''
# INSERT INTO `rbRegionalRiskStage` (`code`,`name`) VALUES (%s, %s);
# ''', rs_data)

            # update regional_group_id
#             c.execute(u'''
# CREATE TABLE `rbRadzRiskFactor` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `code` varchar(64) NOT NULL,
#   `name` varchar(512) NOT NULL,
#   `group_id` int(11) NOT NULL COMMENT '{rbRadzRiskFactorGroup}',
#   PRIMARY KEY (`id`),
#   KEY `fk_rbradzriskfactor_group_idx` (`group_id`),
#   CONSTRAINT `fk_rbradzriskfactor_group` FOREIGN KEY (`group_id`) REFERENCES `rbRadzRiskFactorGroup` (`id`) ON UPDATE CASCADE ON DELETE RESTRICT
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Фактор риска по Радзинскому';
# ''')

            # update regional groups in factors
            sql_update_factor_groups = u'''\
UPDATE rbRadzRiskFactor, rbRadzRiskFactorGroup
SET rbRadzRiskFactor.regional_group_id = rbRadzRiskFactorGroup.id
WHERE rbRadzRiskFactor.code IN ({ins}) AND rbRadzRiskFactorGroup.code = %s'''

            group_code = '01'  # Социально-биологические факторы
            factor_codes = [
                'mother_younger_18',
                'mother_older_40',
                'father_older_40',
                'mother_smoking',
                'mother_alcohol',
                'mother_drugs',
                'father_alcohol',
                'father_drugs',
                'height_less_155',
            ]
            c.execute(sql_update_factor_groups.format(ins=u', '.join([u'%s'] * len(factor_codes))),
                      factor_codes + [group_code])
            group_code = '02'  # Акушерско-гинекологический анамнез
            factor_codes = [
                'parity_above_4',
                'abortion_first_trimester',
                'premature_birth_second_trimester',
                'preeclampsia_anamnesis',
                'miscarriage',
                'child_death',
                'neurological_disorders',
                'abnormal_child_weight',
                'infertility',
                'assisted_reproductive_technology',
                'uterine_scar_1',
                'uterine_scar_more_2',
                'uterus_oophoron_tumor',
                'uterine_malformations',
                'chronic_inflammation_tomsk',
                'adnexal_affection',
                'birth_complications',
                'intrauterine_contraception',
                'tubal_pregnancy',
            ]
            c.execute(sql_update_factor_groups.format(ins=u', '.join([u'%s'] * len(factor_codes))),
                      factor_codes + [group_code])
            group_code = '04'  # Осложнения беременности
            factor_codes = [
                'early_pregnancy_toxemia',
                'threatened_miscarriage',
                'cervix_uteri_length_less_25',
                'preeclampsia_moderate',
                'preeclampsia_hard',
                'eclampsia',
                'hellp',
                'Rh_hypersusceptibility',
                'ABO_hypersusceptibility',
                'hydramnion_moderate',
                'hydramnion_hard',
                'oligohydramnios_moderate',
                'oligohydramnios_hard',
                'pelvic_station_common',
                'abnormal_fetus_position',
                'multiple_pregnancy_2',
                'multiple_pregnancy_3',
                'fetal',
                'central_placental_presentation',
                'low_insertion_of_placenta',
                'pregnancy_after_corrective_surgery',
            ]
            c.execute(sql_update_factor_groups.format(ins=u', '.join([u'%s'] * len(factor_codes))),
                      factor_codes + [group_code])
            group_code = '03'  # Экстрагенитальные заболевания матери
            factor_codes = [
                'pneumology',
                'respiratory_disturbance',
                'vegetovascular_dystonia',
                'heart_disease',
                'heart_disease_circulatory_embarrassment',
                'hypertensive_disease_1',
                'hypertensive_disease_2',
                'hypertensive_disease_3',
                'thrombosis',
                'varicose',
                'renal_disease',
                'renal_disease_exacerbation',
                'glomerulonephritis',
                'solitary_paired',
                'adrenopathy',
                'neurometabolic_endocrine_syndrome',
                'diabetes',
                'thyroid_disorders',
                'obesity',
                'weight_deficit',
                'anemia_70',
                'anemia_110',
                'coagulopathy',
                'thrombocytopenia',
                'emerging_infection_diseases',
                'persistent_infection',
                'nervous_disorder',
                'malignant_tumor',
                'aneurysm',
                'trauma',
            ]
            c.execute(sql_update_factor_groups.format(ins=u', '.join([u'%s'] * len(factor_codes))),
                      factor_codes + [group_code])
            group_code = '06'  # Оценка состояния плода
            factor_codes = [
                'small_gestational_age_fetus_1',
                'small_gestational_age_fetus_2plus',
                'developmental_defect',
                'placental_perfusion_disorder_1',
                'placental_perfusion_disorder_2',
                'placental_perfusion_disorder_3',
            ]
            c.execute(sql_update_factor_groups.format(ins=u', '.join([u'%s'] * len(factor_codes))),
                      factor_codes + [group_code])

            # insert factor - regional stage associations
            all_stages = ('initial', 'before21', 'from21to30', 'from31to36')
            factor_stages = [
                ('mother_younger_18', all_stages, 3),
                ('mother_older_40', all_stages, 3),
                ('father_older_40', all_stages, 2),
                ('mother_smoking', all_stages, 3),
                ('mother_alcohol', all_stages, 5),
                ('mother_drugs', all_stages, 15),
                ('father_alcohol', all_stages, 2),
                ('father_drugs', all_stages, 15),
                ('height_less_155', all_stages, 2),

                ('parity_above_4', all_stages, 5),
                ('abortion_first_trimester', all_stages, 2),
                ('premature_birth_second_trimester', all_stages, 15),
                ('preeclampsia_anamnesis', all_stages, 10),
                ('miscarriage', all_stages, 10),
                ('child_death', all_stages, 10),
                ('neurological_disorders', all_stages, 2),
                ('abnormal_child_weight', all_stages, 2),
                ('infertility', all_stages, 5),
                ('assisted_reproductive_technology', all_stages, 15),
                ('uterine_scar_1', all_stages, 10),
                ('uterine_scar_more_2', all_stages, 15),
                ('uterus_oophoron_tumor', all_stages, 2),
                ('uterine_malformations', all_stages, 2),
                ('chronic_inflammation_tomsk', all_stages, 1),
                ('adnexal_affection', all_stages, 1),
                ('birth_complications', all_stages, 1),
                ('intrauterine_contraception', all_stages, 1),
                ('tubal_pregnancy', all_stages, 1),

                ('early_pregnancy_toxemia', all_stages, 1),
                ('threatened_miscarriage', all_stages, 2),
                ('cervix_uteri_length_less_25', all_stages, 15),
                ('preeclampsia_moderate', all_stages, 10),
                ('preeclampsia_hard', all_stages, 15),
                ('eclampsia', all_stages, 15),
                ('hellp', all_stages, 15),
                ('Rh_hypersusceptibility', all_stages, 1),
                ('ABO_hypersusceptibility', all_stages, 15),
                ('hydramnion_moderate', all_stages, 10),
                ('hydramnion_hard', all_stages, 15),
                ('oligohydramnios_moderate', all_stages, 10),
                ('oligohydramnios_hard', all_stages, 15),
                ('pelvic_station_common', all_stages, 10),
                ('abnormal_fetus_position', all_stages, 10),
                ('multiple_pregnancy_2', all_stages, 10),
                ('multiple_pregnancy_3', all_stages, 15),
                ('fetal', all_stages, 15),
                ('central_placental_presentation', all_stages, 10),
                ('low_insertion_of_placenta', all_stages, 15),
                ('pregnancy_after_corrective_surgery', all_stages, 10),

                ('pneumology', all_stages, 2),
                ('respiratory_disturbance', all_stages, 15),
                ('vegetovascular_dystonia', all_stages, 2),
                ('heart_disease', all_stages, 15),
                ('heart_disease_circulatory_embarrassment', all_stages, 15),
                ('hypertensive_disease_1', all_stages, 2),
                ('hypertensive_disease_2', all_stages, 10),
                ('hypertensive_disease_3', all_stages, 15),
                ('thrombosis', all_stages, 15),
                ('varicose', all_stages, 2),
                ('renal_disease', all_stages, 1),
                ('renal_disease_exacerbation', all_stages, 5),
                ('glomerulonephritis', all_stages, 15),
                ('solitary_paired', all_stages, 15),
                ('adrenopathy', all_stages, 6),
                ('neurometabolic_endocrine_syndrome', all_stages, 15),
                ('diabetes', all_stages, 10),
                ('thyroid_disorders', all_stages, 2),
                ('obesity', all_stages, 3),
                ('weight_deficit', all_stages, 3),
                ('anemia_70', all_stages, 2),
                ('anemia_110', all_stages, 15),
                ('coagulopathy', all_stages, 15),
                ('thrombocytopenia', all_stages, 15),
                ('emerging_infection_diseases', all_stages, 2),
                ('persistent_infection', all_stages, 10),
                ('nervous_disorder', all_stages, 15),
                ('malignant_tumor', all_stages, 15),
                ('aneurysm', all_stages, 15),
                ('trauma', all_stages, 5),

                ('small_gestational_age_fetus_1', all_stages, 10),
                ('small_gestational_age_fetus_2plus', all_stages, 15),
                ('developmental_defect', all_stages, 15),
                ('placental_perfusion_disorder_1', all_stages, 2),
                ('placental_perfusion_disorder_2', all_stages, 10),
                ('placental_perfusion_disorder_3', all_stages, 15),
            ]
            sql_factor_stage_assoc = u'''\
INSERT IGNORE INTO rbRadzRiskFactor_RegionalStage (factor_id, stage_id, points)
{unions}'''
            c.execute(sql_factor_stage_assoc.format(
                unions=u' UNION '.join(
                    u'SELECT rbRadzRiskFactor.id, rbRegionalRiskStage.id, {2} '
                    u'FROM rbRadzRiskFactor, rbRegionalRiskStage '
                    u'WHERE rbRadzRiskFactor.code = "{0}" AND rbRegionalRiskStage.code = "{1}" '
                    .format(factor_code, stage_code, points)
                    for factor_code, stage_list, points in factor_stages
                    for stage_code in stage_list
                )
            ))

            # region risks tables
#             c.execute(u'''
# CREATE TABLE `RisarTomskRegionalRisks` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `createDatetime` datetime NOT NULL,
#   `createPerson_id` int(11) DEFAULT NULL,
#   `modifyDatetime` datetime NOT NULL,
#   `modifyPerson_id` int(11) DEFAULT NULL,
#   `event_id` int(11) NOT NULL,
#   `initial_points` int(11) DEFAULT NULL COMMENT 'Сумма баллов факторов при постановке на учет',
#   `before21week_points` int(11) DEFAULT NULL COMMENT 'Сумма баллов до 21 недели',
#   `from21to30week_points` int(11) DEFAULT NULL COMMENT 'Сумма баллов с 21 по 30 неделю',
#   `from31to36week_points` int(11) DEFAULT NULL COMMENT 'Сумма баллов с 31 по 36 неделю',
#   PRIMARY KEY (`id`),
#   KEY `fk_risartomskregrisks_event_idx` (`event_id`),
#   KEY `fk_risartomskregrisks_createperson_idx` (`createPerson_id`),
#   KEY `fk_risartomskregrisks_modifyperson_idx` (`modifyPerson_id`),
#   CONSTRAINT `fk_risartomskregrisks_createperson` FOREIGN KEY (`createPerson_id`) REFERENCES `Person` (`id`) ON UPDATE CASCADE,
#   CONSTRAINT `fk_risartomskregrisks_event` FOREIGN KEY (`event_id`) REFERENCES `Event` (`id`) ON UPDATE CASCADE,
#   CONSTRAINT `fk_risartomskregrisks_modifyperson` FOREIGN KEY (`modifyPerson_id`) REFERENCES `Person` (`id`) ON UPDATE CASCADE,
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Рассчитанные риски по региональной шкале для случая';
# ''')
#
#             c.execute(u'''
# CREATE TABLE `RisarTomskRegionalRisks_Factors` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `risk_id` int(11) NOT NULL COMMENT '{RisarTomskRegionalRisks}',
#   `risk_factor_id` int(11) NOT NULL COMMENT '{rbRadzRiskFactor}',
#   `stage_id` int(11) NOT NULL COMMENT '{rbRegionalRiskStage}',
#   PRIMARY KEY (`id`),
#   KEY `fk_risartomskregrisks_factors_risk_idx` (`risk_id`),
#   KEY `fk_risartomskregrisks_factors_factor_code_idx` (`risk_factor_id`),
#   KEY `fk_risartomskregrisks_factors_stage_idx` (`stage_id`),
#   CONSTRAINT `fk_risartomskregrisks_factors_factor` FOREIGN KEY (`risk_factor_id`) REFERENCES `rbRadzRiskFactor` (`id`) ON UPDATE CASCADE,
#   CONSTRAINT `fk_risartomskregrisks_factors_risk` FOREIGN KEY (`risk_id`) REFERENCES `RisarTomskRegionalRisks` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
#   CONSTRAINT `fk_risartomskregrisks_factors_stage` FOREIGN KEY (`stage_id`) REFERENCES `rbRegionalRiskStage` (`id`) ON UPDATE CASCADE
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Сработавшие факторы риска по региональной шкале для случая';
# ''')
