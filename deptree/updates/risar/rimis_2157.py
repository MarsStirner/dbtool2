# coding: utf-8

from deptree.internals.base import DBToolBaseNode


class RegionalRisksSaratovScale(DBToolBaseNode):
    name = 'rimis-2157'
    depends = ['rimis-2157.new_factors_from_saratov', 'rimis-2157.regional_saratov',
               #'rimis-2157.diags_mkb_details_content'
              ]


class RegionalNewFactorsFromSaratov(DBToolBaseNode):
    name = 'rimis-2157.new_factors_from_saratov'
    depends = ['rimis-1885.regional_common']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            gr_data = [("08", u'Ультразвуковой скрининг')]
#             c.executemany(u'''
# INSERT IGNORE INTO `rbRadzRiskFactorGroup` (`code`, `name`)
# VALUES (%s, %s);
# ''', gr_data)

            rrf_data = [
                ("height_less_158", u"Рост 158 см и менее"),
                ("uterine_scar_lower_section", u"Рубец на матке после операции в нижнем сегменте"),
                ("uterine_scar_corporeal", u"Рубец на матке после операции корпоральный"),
                ("gestational_hypertension", u"Гипертензия вызванная беременностью"),
                ("Rh_minus", u"Отрицательный резус-фактор"),
                ("placental_presentation", u"Предлежание плаценты"),
                ("placental_perfusion_disorder_1_saratov", u"Нарушение маточно-плацентарного кровотока 1А или 1Б степени (если ИР маточных артерий равен или более 0,56 или ИР артерии пуповины равен или более 0,68)"),
                ("placental_perfusion_disorder_2_saratov", u"Нарушение маточно-плацентарного кровотока 2 степени (если ИР маточных артерий равен или более 0,56 и ИР артерии пуповины равен или более 0,68)"),
                ("placental_perfusion_disorder_3_saratov", u"Нарушение маточно-плацентарного кровотока 3 степени (если ИР маточных артерий равен или более 0,56, а ИР артерии пуповины имеет отрицательный диастолический компонент)"),
                ("hydramnion_saratov", u"Маловодие (ИАЖ менее 90)"),
                ("oligohydramnios_saratov", u"Многоводие (ИАЖ более 160)"),
                ("placental_maturity_2", u"Степень зрелости плаценты: 2 степень до 32 недель"),
                ("placental_maturity_3", u"Степень зрелости плаценты: 3 степень до 35 недель"),
                ("cardiotocography_between_7_and_8", u"Оценка КТГ по шкале Fisher W.M. (баллы): Меньше 8 до 7 баллов"),
                ("cardiotocography_between_7_and_6", u"Оценка КТГ по шкале Fisher W.M. (баллы): От 7 до 6 баллов"),
                ("cardiotocography_between_6_and_5", u"Оценка КТГ по шкале Fisher W.M. (баллы): От 6 до 5 баллов"),
                ("cardiotocography_between_5_and_4", u"Оценка КТГ по шкале Fisher W.M. (баллы): От 5 до 4 баллов"),
            ]
            c.executemany(u'''
INSERT IGNORE INTO `rbRadzRiskFactor` (`code`, `name`)
VALUES (%s, %s);
''', rrf_data)


class RegionalRisksSaratov(DBToolBaseNode):
    name = 'rimis-2157.regional_saratov'  # Region specific
    depends = ['rimis-1885.regional_common', 'rimis-2157.new_factors_from_saratov']

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
#                 ('anamnestic', 'Анамнестические факторы'),
#                 ('before35', 'Факторы до 35 недель'),
#                 ('after36', 'Факторы после 36 недель'),
#                 ('intranatal', 'Интранатальные факторы')
#             ]
#             c.executemany(u'''
# INSERT INTO `rbRegionalRiskStage` (`code`,`name`) VALUES (%s, %s);
# ''', rs_data)

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
                'mother_professional_properties',
                'father_professional_properties',
                'mother_smoking',
                'mother_alcohol',
                'father_alcohol',
                'emotional_stress',
                'height_less_158',
                'overweight',
                'not_married'
            ]
            c.execute(sql_update_factor_groups.format(ins=u', '.join([u'%s'] * len(factor_codes))),
                      factor_codes + [group_code])
            group_code = '02'  # Акушерско-гинекологический анамнез
            factor_codes = [
                'parity_under_7',
                'parity_above_8',
                'abortion_1',
                'abortions_2',
                'abortions_more_3',
                'abortion_after_last_delivery_more_3',
                'intrauterine_operations',
                'premature_birth_1',
                'premature_birth_more_2',
                'miscarriage_1',
                'miscarriage_more_2',
                'child_death_1',
                'child_death_more_2',
                'congenital_disorders',
                'neurological_disorders',
                'abnormal_child_weight',
                'infertility_less_4',
                'infertility_more_5',
                'uterine_scar_lower_section',
                'uterine_scar_corporeal',
                'uterus_oophoron_tumor',
                'insuficiencia_istmicocervical',
                'uterine_malformations',
                'chronic_inflammation',
                'tubal_pregnancy',
                'extracorporal_fertilization',
                'intracytoplasmic_sperm_injection',
            ]
            c.execute(sql_update_factor_groups.format(ins=u', '.join([u'%s'] * len(factor_codes))),
                      factor_codes + [group_code])
            group_code = '03'  # Экстрагенитальные заболевания матери
            factor_codes = [
                'heart_disease',
                'heart_disease_circulatory_embarrassment',
                'hypertensive_disease_1',
                'hypertensive_disease_2',
                'hypertensive_disease_3',
                'varicose',
                'hypotensive_syndrome',
                'renal_disease',
                'adrenal_disorders',
                'neurometabolic_endocrine_syndrome',
                'diabetes',
                'thyroid_disorders',
                'obesity',
                'anemia_90',
                'anemia_100',
                'anemia_110',
                'coagulopathy',
                'myopia',
                'persistent_infection',
                'lupus_anticoagulant_positive',
                'antiphospholipid_antibodies_IgG',
                'antiphospholipid_antibodies_IgM',
            ]
            c.execute(sql_update_factor_groups.format(ins=u', '.join([u'%s'] * len(factor_codes))),
                      factor_codes + [group_code])
            group_code = '04'  # Осложнения беременности
            factor_codes = [
                'early_pregnancy_toxemia',
                'recurrent_threatened_miscarriage',
                'edema_disease',
                'gestational_hypertension',
                'preeclampsia',
                'eclampsia',
                'renal_disease_exacerbation',
                'emerging_infection_diseases',
                'Rh_minus',
                'ABO_hypersusceptibility',
                'pelvic_station',
                'multiple_pregnancy',
                'placental_presentation',
                'prolonged_pregnancy',
                'abnormal_fetus_position',
                'maternal_passages_immaturity',
            ]
            c.execute(sql_update_factor_groups.format(ins=u', '.join([u'%s'] * len(factor_codes))),
                      factor_codes + [group_code])

            group_code = '05'  # Скрининг
            factor_codes = [
                'beta_HCG_increase',
                'beta_HCG_decrease',
                'alpha_fetoprotein_increase',
                'alpha_fetoprotein_decrease',
                'PAPP_A_increase',
                'PAPP_A_decrease',
            ]
            c.execute(sql_update_factor_groups.format(ins=u', '.join([u'%s'] * len(factor_codes))),
                      factor_codes + [group_code])

            group_code = '08'  # Ультразвуковой скрининг
            factor_codes = [
                'placental_perfusion_disorder_1_saratov',
                'placental_perfusion_disorder_2_saratov',
                'placental_perfusion_disorder_3_saratov',
                'hydramnion_saratov',
                'oligohydramnios_saratov',
                'placental_maturity_2',
                'placental_maturity_3',
                'small_gestational_age_fetus_1',
                'small_gestational_age_fetus_2',
                'small_gestational_age_fetus_3',
            ]
            c.execute(sql_update_factor_groups.format(ins=u', '.join([u'%s'] * len(factor_codes))),
                      factor_codes + [group_code])
            group_code = '06'  # Оценка состояния плода
            factor_codes = [
                'chronical_placental_insufficiency',
                'cardiotocography_between_7_and_8',
                'cardiotocography_between_7_and_6',
                'cardiotocography_between_6_and_5',
                'cardiotocography_between_5_and_4',
                'cardiotocography_less_4',
            ]
            c.execute(sql_update_factor_groups.format(ins=u', '.join([u'%s'] * len(factor_codes))),
                      factor_codes + [group_code])
            group_code = '07'  # Интранатальные осложнения
            factor_codes = [
                'meconium_amniotic_fluid',
                'predelivery_amniorrhea_before_labour',
                'pathological_preliminary_period',
                'labour_anomaly',
                'chorioamnionitis',
            ]
            c.execute(sql_update_factor_groups.format(ins=u', '.join([u'%s'] * len(factor_codes))),
                      factor_codes + [group_code])

            # insert factor - regional stage associations
            # stages: ('anamnestic', 'before35', 'after36', 'intranatal')
            factor_stages = [
                ('mother_younger_18', ('anamnestic', ), 2),
                ('mother_older_40', ('anamnestic', ), 4),
                ('father_older_40', ('anamnestic', ), 2),
                ('mother_professional_properties', ('anamnestic', ), 3),
                ('father_professional_properties', ('anamnestic', ), 2),
                ('mother_smoking', ('anamnestic', ), 2),
                ('mother_alcohol', ('anamnestic', ), 4),
                ('father_alcohol', ('anamnestic', ), 2),
                ('emotional_stress', ('anamnestic', ), 1),
                ('height_less_158', ('anamnestic', ), 2),
                ('overweight', ('anamnestic', ), 2),
                ('not_married', ('anamnestic', ), 1),

                ('parity_under_7', ('anamnestic', ), 1),
                ('parity_above_8', ('anamnestic',), 2),
                ('abortion_1', ('anamnestic',), 2),
                ('abortions_2', ('anamnestic',), 3),
                ('abortions_more_3', ('anamnestic',), 4),
                ('abortion_after_last_delivery_more_3', ('anamnestic',), 2),
                ('intrauterine_operations', ('anamnestic',), 2),
                ('premature_birth_1', ('anamnestic',), 2),
                ('premature_birth_more_2', ('anamnestic',), 3),
                ('miscarriage_1', ('anamnestic',), 3),
                ('miscarriage_more_2', ('anamnestic',), 8),
                ('child_death_1', ('anamnestic',), 2),
                ('child_death_more_2', ('anamnestic',), 7),
                ('congenital_disorders', ('anamnestic',), 3),
                ('neurological_disorders', ('anamnestic',), 2),
                ('abnormal_child_weight', ('anamnestic',), 2),
                ('infertility_less_4', ('anamnestic',), 2),
                ('infertility_more_5', ('anamnestic',), 4),
                ('uterine_scar_lower_section', ('anamnestic',), 4),
                ('uterine_scar_corporeal', ('anamnestic',), 10),
                ('uterus_oophoron_tumor', ('anamnestic',), 4),
                ('insuficiencia_istmicocervical', ('anamnestic',), 2),
                ('uterine_malformations', ('anamnestic',), 3),
                ('chronic_inflammation', ('anamnestic',), 3),
                ('tubal_pregnancy', ('anamnestic',), 3),
                ('extracorporal_fertilization', ('anamnestic',), 10),
                ('intracytoplasmic_sperm_injection', ('anamnestic',), 4),

                ('heart_disease', ('anamnestic',), 3),
                ('heart_disease_circulatory_embarrassment', ('anamnestic',), 10),
                ('hypertensive_disease_1', ('anamnestic',), 10),
                ('hypertensive_disease_2', ('anamnestic',), 11),
                ('hypertensive_disease_3', ('anamnestic',), 12),
                ('varicose', ('anamnestic',), 5),
                ('hypotensive_syndrome', ('anamnestic',), 2),
                ('renal_disease', ('anamnestic',), 4),
                ('adrenal_disorders', ('anamnestic',), 5),
                ('neurometabolic_endocrine_syndrome', ('anamnestic',), 10),
                ('diabetes', ('anamnestic',), 10),
                ('thyroid_disorders', ('anamnestic',), 7),
                ('obesity', ('anamnestic',), 2),
                ('anemia_90', ('anamnestic',), 4),
                ('anemia_100', ('anamnestic',), 2),
                ('anemia_110', ('anamnestic',), 1),
                ('coagulopathy', ('anamnestic',), 5),
                ('myopia', ('anamnestic',), 2),
                ('persistent_infection', ('anamnestic',), 3),
                ('lupus_anticoagulant_positive', ('anamnestic',), 4),
                ('antiphospholipid_antibodies_IgG', ('anamnestic',), 2),
                ('antiphospholipid_antibodies_IgM', ('anamnestic',), 3),

                ('early_pregnancy_toxemia', ('before35', 'after36'), 2),
                ('recurrent_threatened_miscarriage', ('before35', 'after36'), 2),
                ('edema_disease', ('before35', 'after36'), 2),
                ('gestational_hypertension', ('before35', 'after36'), 10),
                ('preeclampsia', ('before35', 'after36'), 11),
                ('eclampsia', ('before35', 'after36'), 12),
                ('renal_disease_exacerbation', ('before35', 'after36'), 4),
                ('emerging_infection_diseases', ('before35', 'after36'), 4),
                ('Rh_minus', ('before35', 'after36'), 5),
                ('ABO_hypersusceptibility', ('before35', 'after36'), 10),
                ('pelvic_station', ('before35', 'after36'), 3),
                ('multiple_pregnancy', ('before35', 'after36'), 10),
                ('placental_presentation', ('before35', 'after36'), 15),
                ('prolonged_pregnancy', ('before35', 'after36'), 3),
                ('abnormal_fetus_position', ('before35', 'after36'), 3),
                ('maternal_passages_immaturity', ('before35', 'after36'), 4),

                ('beta_HCG_increase', ('before35', 'after36'), 3),
                ('beta_HCG_decrease', ('before35', 'after36'), 4),
                ('alpha_fetoprotein_increase', ('before35', 'after36'), 6),
                ('alpha_fetoprotein_decrease', ('before35', 'after36'), 8),
                ('PAPP_A_increase', ('before35', 'after36'), 2),
                ('PAPP_A_decrease', ('before35', 'after36'), 3),

                ('placental_perfusion_disorder_1_saratov', ('before35', 'after36'), 20),
                ('placental_perfusion_disorder_2_saratov', ('before35', 'after36'), 22),
                ('placental_perfusion_disorder_3_saratov', ('before35', 'after36'), 25),
                ('hydramnion_saratov', ('before35', 'after36'), 15),
                ('oligohydramnios_saratov', ('before35', 'after36'), 10),
                ('placental_maturity_2', ('before35', 'after36'), 18),
                ('placental_maturity_3', ('before35', 'after36'), 15),
                ('small_gestational_age_fetus_1', ('before35', 'after36'), 10),
                ('small_gestational_age_fetus_2', ('before35', 'after36'), 15),
                ('small_gestational_age_fetus_3', ('before35', 'after36'), 20),

                ('chronical_placental_insufficiency', ('before35', 'after36'), 4),
                ('cardiotocography_between_7_and_8', ('before35', 'after36'), 4),
                ('cardiotocography_between_7_and_6', ('before35', 'after36'), 8),
                ('cardiotocography_between_6_and_5', ('before35', 'after36'), 12),
                ('cardiotocography_between_5_and_4', ('before35', 'after36'), 16),
                ('cardiotocography_less_4', ('before35', 'after36'), 20),

                ('meconium_amniotic_fluid', ('intranatal',), 8),
                ('predelivery_amniorrhea_before_labour', ('intranatal',), 6),
                ('pathological_preliminary_period', ('intranatal',), 4),
                ('labour_anomaly', ('intranatal',), 10),
                ('chorioamnionitis', ('intranatal',), 4),
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

#             # region risks tables
#             c.execute(u'''
# CREATE TABLE `RisarSaratovRegionalRisks` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `createDatetime` datetime NOT NULL,
#   `createPerson_id` int(11) DEFAULT NULL,
#   `modifyDatetime` datetime NOT NULL,
#   `modifyPerson_id` int(11) DEFAULT NULL,
#   `event_id` int(11) NOT NULL,
#   `anamnestic_points` int(11) DEFAULT NULL COMMENT 'Сумма баллов анамнестических факторов',
#   `before35week_points` int(11) DEFAULT NULL COMMENT 'Сумма баллов до 35 недель <=',
#   `after36week_points` int(11) DEFAULT NULL COMMENT 'Сумма баллов после 36 недель >=',
#   `intranatal_points` int(11) DEFAULT NULL COMMENT 'Сумма баллов интранатальных факторов',
#   `before35week_totalpoints` int(11) DEFAULT NULL COMMENT 'Общая сумма баллов факторов до 35 недель',
#   `after36week_totalpoints` int(11) DEFAULT NULL COMMENT 'Общая сумма баллов факторов после 36 недель',
#   `intranatal_totalpoints` int(11) DEFAULT NULL COMMENT 'Общая сумма баллов с учётом интранатальных факторов',
#   `intranatal_growth` double DEFAULT NULL COMMENT 'Интранатальный прирост, %',
#   PRIMARY KEY (`id`),
#   KEY `fk_risarsaratovregrisks_event_idx` (`event_id`),
#   KEY `fk_risarsaratovregrisks_createperson_idx` (`createPerson_id`),
#   KEY `fk_risarradzinskyrisks_modifyperson_idx` (`modifyPerson_id`),
#   CONSTRAINT `fk_risarsaratovregrisks_createperson` FOREIGN KEY (`createPerson_id`) REFERENCES `Person` (`id`) ON UPDATE CASCADE,
#   CONSTRAINT `fk_risarsaratovregrisks_event` FOREIGN KEY (`event_id`) REFERENCES `Event` (`id`) ON UPDATE CASCADE,
#   CONSTRAINT `fk_risarsaratovregrisks_modifyperson` FOREIGN KEY (`modifyPerson_id`) REFERENCES `Person` (`id`) ON UPDATE CASCADE
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Рассчитанные риски по региональной шкале для случая';
# ''')
#
#             c.execute(u'''
# CREATE TABLE `RisarSaratovRegionalRisks_Factors` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `risk_id` int(11) NOT NULL COMMENT '{RisarSaratovRegionalRisks}',
#   `risk_factor_id` int(11) NOT NULL COMMENT '{rbRadzRiskFactor}',
#   `stage_id` int(11) NOT NULL COMMENT '{rbRegionalRiskStage}',
#   PRIMARY KEY (`id`),
#   KEY `fk_risarsaratovregrisks_factors_risk_idx` (`risk_id`),
#   KEY `fk_risarsaratovregrisks_factors_factor_code_idx` (`risk_factor_id`),
#   KEY `fk_risarsaratovregrisks_factors_stage_idx` (`stage_id`),
#   CONSTRAINT `fk_risarsaratovregrisks_factors_factor` FOREIGN KEY (`risk_factor_id`) REFERENCES `rbRadzRiskFactor` (`id`) ON UPDATE CASCADE,
#   CONSTRAINT `fk_risarsaratovregrisks_factors_risk` FOREIGN KEY (`risk_id`) REFERENCES `RisarSaratovRegionalRisks` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
#   CONSTRAINT `fk_risarsaratovregrisks_factors_stage` FOREIGN KEY (`stage_id`) REFERENCES `rbRegionalRiskStage` (`id`) ON UPDATE CASCADE
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Сработавшие факторы риска по региональной шкале для случая';
# ''')


class DiagsMKBDetailsContent2(DBToolBaseNode):
    name = 'rimis-2157.diags_mkb_details_content'
    depends = ['rimis-1885.diags_mkb_details_content']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            return
            details_data = [
                ('O40%', 'rbRisarHydramnionStage', u'Уточнение МКБ'),
                ('O41.0%', 'rbRisarOligohydramnionStage', u'Уточнение МКБ'),
                ('I11%', 'rbRisarHypertensiveDiseaseStage', u'Уточнение МКБ'),
                ('I12%', 'rbRisarHypertensiveDiseaseStage', u'Уточнение МКБ'),
                ('I13%', 'rbRisarHypertensiveDiseaseStage', u'Уточнение МКБ'),
                ('I14%', 'rbRisarHypertensiveDiseaseStage', u'Уточнение МКБ'),
                ('I15%', 'rbRisarHypertensiveDiseaseStage', u'Уточнение МКБ'),
                ('O10%', 'rbRisarHypertensiveDiseaseStage', u'Уточнение МКБ'),
                ('O11%', 'rbRisarHypertensiveDiseaseStage', u'Уточнение МКБ'),
                ('O44.0', 'rbRisarPlacentalPresentationStage', u'Уточнение МКБ'),
                ('O44.1', 'rbRisarPlacentalPresentationStage', u'Уточнение МКБ'),
                ('O43.8', 'rbRisarPlacentalPerfusionDisorderStage', u'Уточнение МКБ'),
                ('O43.9', 'rbRisarPlacentalPerfusionDisorderStage', u'Уточнение МКБ'),
            ]
            sql_insert = u'''INSERT IGNORE INTO `MKB_details` (`mkb_id`, `refbookName`, `refbookText`) {unions}'''
            c.execute(sql_insert.format(
                unions=u' UNION '.join(
                    u'SELECT MKB.id, "{1}", "{2}" '
                    u'FROM MKB '
                    u'WHERE MKB.DiagID LIKE "{0}" AND deleted = 0 '
                    .format(mkb_like, rb_name, rb_text)
                    for mkb_like, rb_name, rb_text in details_data
                )
            ))
