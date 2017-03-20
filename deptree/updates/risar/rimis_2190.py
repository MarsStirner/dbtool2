# coding: utf-8

from deptree.internals.base import DBToolBaseNode


class RegionalRisksTomskFactorsChanges1(DBToolBaseNode):
    name = 'rimis-2190'  # Region Tomsk
    depends = ['rimis-2190.new_factors_from_tomsk2', 'rimis-2190.tomsk_scale_factor_changes2']


class RegionalNewFactorsFromTomsk2(DBToolBaseNode):
    name = 'rimis-2190.new_factors_from_tomsk2'
    depends = ['rimis-1885.regional_common']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            rrf_data = [
                ("diabetes_tomsk", u"Эндокринопатии: сахарный диабет "),
                ("gestational_diabetes", u"Эндокринопатии: гестационный диабет "),
            ]
            c.executemany(u'''
INSERT IGNORE INTO `rbRadzRiskFactor` (`code`, `name`)
VALUES (%s, %s);
''', rrf_data)


class TomskScaleFactorChanges2(DBToolBaseNode):
    name = 'rimis-2190.tomsk_scale_factor_changes2'  # Region specific
    depends = ['rimis-1885.tomsk_scale_factor_changes1']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            # update regional groups in factors
            sql_update_factor_groups = u'''\
UPDATE rbRadzRiskFactor, rbRadzRiskFactorGroup
SET rbRadzRiskFactor.regional_group_id = rbRadzRiskFactorGroup.id
WHERE rbRadzRiskFactor.code IN ({ins}) AND rbRadzRiskFactorGroup.code = %s'''

            group_code = '03'  # Экстрагенитальные заболевания матери
            factor_codes = [
                'diabetes_tomsk',
                'gestational_diabetes',
            ]
            c.execute(sql_update_factor_groups.format(ins=u', '.join([u'%s'] * len(factor_codes))),
                      factor_codes + [group_code])

            sql_upd_fg_nul = u'''\
UPDATE rbRadzRiskFactor
SET rbRadzRiskFactor.regional_group_id = NULL
WHERE rbRadzRiskFactor.code = %s'''
            c.execute(sql_upd_fg_nul, ('diabetes',))

            # insert factor - regional stage associations
            all_stages = ('initial', 'before21', 'from21to30', 'from31to36')
            factor_stages = [
                ('diabetes_tomsk', all_stages, 15),
                ('gestational_diabetes', all_stages, 10),
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

            # delete factor - regional stage associations
            sql_factor_stage_assoc_del = u'''\
DELETE rbRadzRiskFactor_RegionalStage.*
FROM rbRadzRiskFactor_RegionalStage, rbRadzRiskFactor
WHERE rbRadzRiskFactor_RegionalStage.factor_id = rbRadzRiskFactor.id AND
rbRadzRiskFactor.code = %s'''
            c.execute(sql_factor_stage_assoc_del, ('diabetes',))

            # update factor - regional stage associations
            sql_factor_stage_assoc_del = u'''\
UPDATE rbRadzRiskFactor_RegionalStage, rbRadzRiskFactor
SET rbRadzRiskFactor_RegionalStage.points = %s
WHERE rbRadzRiskFactor_RegionalStage.factor_id = rbRadzRiskFactor.id AND
rbRadzRiskFactor.code = %s'''
            c.execute(sql_factor_stage_assoc_del, (6, 'neurometabolic_endocrine_syndrome'))
