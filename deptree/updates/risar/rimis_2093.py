# coding: utf-8

from deptree.internals.base import DBToolBaseNode


class RadzinskyRisksScaleUpdate1(DBToolBaseNode):
    name = 'rimis-2093'
    depends = ['rimis-2093.radz_and_regional_factor_deletion', 'rimis-2093.radz_scale_factor_changes1']


class RadzRiskFactorAddColDeleted(DBToolBaseNode):
    name = 'rimis-2093.radz_and_regional_factor_deletion'
    depends = ['rimis-1885.regional_common']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `rbRadzRiskFactor_Stage`
ADD COLUMN `deleted` TINYINT(1) NOT NULL DEFAULT 0 AFTER `points`;''')

            c.execute(u'''
ALTER TABLE `rbRadzRiskFactor_RegionalStage`
ADD COLUMN `deleted` TINYINT(1) NOT NULL DEFAULT 0 AFTER `points`;''')


class RadzRiskScaleFactorChanges1(DBToolBaseNode):
    name = 'rimis-2093.radz_scale_factor_changes1'
    depends = ['rimis-2093.radz_and_regional_factor_deletion',
               'rimis-1885.new_factors_from_tomsk', 'rimis-2157.new_factors_from_saratov']

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            # 1) delete factors
            to_del = [
                'height_less_150',
                'gestosis_mild_case',
                'preeclampsia',
                'Rh_hypersusceptibility'
            ]
            sql_del = u'''
UPDATE rbRadzRiskFactor_Stage, rbRadzRiskFactor
SET rbRadzRiskFactor_Stage.deleted = 1
WHERE rbRadzRiskFactor_Stage.factor_id = rbRadzRiskFactor.id AND
rbRadzRiskFactor.code IN ({ins})'''
            c.execute(sql_del.format(ins=u', '.join([u'%s'] * len(to_del))), to_del)

            # 2) add new factors
            new_data = [
                ("height_less_158", u"Рост 158 см и менее"),
                ("Rh_minus", u"Отрицательный резус-фактор"),
            ]
            c.executemany(u'''
INSERT IGNORE INTO `rbRadzRiskFactor` (`code`, `name`)
VALUES (%s, %s);
''', new_data)

            # 2.1) set group
            sql_update_factor_groups = u'''\
UPDATE rbRadzRiskFactor, rbRadzRiskFactorGroup
SET rbRadzRiskFactor.group_id = rbRadzRiskFactorGroup.id
WHERE rbRadzRiskFactor.code IN ({ins}) AND rbRadzRiskFactorGroup.code = %s'''

            group_code = '01'  # Социально-биологические факторы
            factor_codes = [
                'height_less_158',
            ]
            c.execute(sql_update_factor_groups.format(ins=u', '.join([u'%s'] * len(factor_codes))),
                      factor_codes + [group_code])
            group_code = '04'  # Осложнения беременности
            factor_codes = [
                'Rh_minus',
            ]
            c.execute(sql_update_factor_groups.format(ins=u', '.join([u'%s'] * len(factor_codes))),
                      factor_codes + [group_code])

            # 2.2) add stage assoc
            # stages: ('anamnestic', 'before32', 'after33', 'intranatal')
            factor_stages = [
                ('height_less_158', ('anamnestic', ), 2),
                ('Rh_minus', ('before32', 'after33'), 5),
            ]
            sql_factor_stage_assoc = u'''\
INSERT IGNORE INTO rbRadzRiskFactor_Stage (factor_id, stage_id, points)
{unions}'''
            c.execute(sql_factor_stage_assoc.format(
                unions=u' UNION '.join(
                    u'SELECT rbRadzRiskFactor.id, rbRadzStage.id, {2} '
                    u'FROM rbRadzRiskFactor, rbRadzStage '
                    u'WHERE rbRadzRiskFactor.code = "{0}" AND rbRadzStage.code = "{1}" '
                    .format(factor_code, stage_code, points)
                    for factor_code, stage_list, points in factor_stages
                    for stage_code in stage_list
                )
            ))
