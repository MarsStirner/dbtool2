# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')

class DiagnositcActionTypeModification(DBToolBaseNode):
    name = 'tmis-1250'
    depends = ['tmis-1250.CT', 'tmis-1250.MR', 'tmis-1250.US', 'tmis-1250.CR']
    #, 'tmis-1250.XA', 'tmis-1250.MG', 'tmis-1250.ES']


#КОМПЬЮТЕРНАЯ ТОМОГРАФИЯ
class CT(DBToolBaseNode):
    name = 'tmis-1250.CT'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            modify_diagnostic_action_type_tree(u'CT', u'КОМПЬЮТЕРНАЯ ТОМОГРАФИЯ', c)

    @classmethod
    def downgrade(cls):
        with cls.connection as c:
            downgrade(u'КОМПЬЮТЕРНАЯ ТОМОГРАФИЯ', c)

#МАГНИТНО-РЕЗОНАНСНАЯ ТОМОГРАФИЯ
class MRT(DBToolBaseNode):
    name = 'tmis-1250.MR'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            modify_diagnostic_action_type_tree(u'MR', u'МАГНИТНО-РЕЗОНАНСНАЯ ТОМОГРАФИЯ', c)

    @classmethod
    def downgrade(cls):
        with cls.connection as c:
            downgrade(u'МАГНИТНО-РЕЗОНАНСНАЯ ТОМОГРАФИЯ', c)


#УЛЬТРАЗВУКОВЫЕ ДИАГНОСТИЧЕСКИЕ ИССЛЕДОВАНИЯ
class US(DBToolBaseNode):
    name = 'tmis-1250.US'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            modify_diagnostic_action_type_tree(u'US', u'УЛЬТРАЗВУКОВЫЕ ДИАГНОСТИЧЕСКИЕ ИССЛЕДОВАНИЯ', c)

    @classmethod
    def downgrade(cls):
        with cls.connection as c:
            downgrade(u'УЛЬТРАЗВУКОВЫЕ ДИАГНОСТИЧЕСКИЕ ИССЛЕДОВАНИЯ', c)


#РЕНТГЕНОЛОГИЧЕСКИЕ ИССЛЕДОВАНИЯ
class CR(DBToolBaseNode):
    name = 'tmis-1250.CR'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            modify_diagnostic_action_type_tree(u'CR', u'РЕНТГЕНОЛОГИЧЕСКИЕ ИССЛЕДОВАНИЯ', c)

    @classmethod
    def downgrade(cls):
        with cls.connection as c:
            downgrade(u'РЕНТГЕНОЛОГИЧЕСКИЕ ИССЛЕДОВАНИЯ', c)


query_select_diagnostic_aty_id_by_title = u'''
SELECT aty.id, aty.code, aty.name
FROM ActionType aty
WHERE aty.deleted = 0
AND aty.title = '{}'
ORDER BY aty.id DESC
LIMIT 1;
'''
query_select_aty_by_group_id = u'''
SELECT aty.id, aty.code, aty.name
FROM ActionType aty
WHERE aty.deleted = 0
AND aty.group_id = {}
ORDER BY aty.id DESC
'''
query_update_action_type_mnemonic = u'''
UPDATE ActionType
SET mnem = '{}',
modifyDatetime = CURRENT_TIMESTAMP()
WHERE id IN ({});
'''
query_update_action_type_flat_code = u'''
UPDATE ActionType
SET flatCode = CONCAT('multivox_', IF(LENGTH(TRIM(flatCode)) > 0, TRIM(flatCode), TRIM(code)))
WHERE flatCode NOT LIKE 'multivox_%'
AND id IN ({})'''


def modify_diagnostic_action_type_tree(dicom_modality_code, root_action_type_code, c):
    c.execute(query_select_diagnostic_aty_id_by_title.format(root_action_type_code))
    action_type_id, action_type_code, action_type_name = c.fetchone()
    logger.info(u'''[{}] Root is ActionType[{}] code='{}' name='{}' '''.format(
        dicom_modality_code,
        action_type_id,
        action_type_code,
        action_type_name
    ))
    leafs = find_leafs_recursive(action_type_id, 0, c)
    logger.info(u'[{}] Need to modify ActionTypes: {}'.format(dicom_modality_code, u','.join(str(x) for x in leafs)))
    c.execute(query_update_action_type_mnemonic.format(dicom_modality_code, u','.join(str(x) for x in leafs)))
    logger.info(u'''[{0}] ActionType.mnem is set to '{0}' '''.format(dicom_modality_code))
    c.execute(query_update_action_type_flat_code.format(u','.join(str(x) for x in leafs)))
    logger.info(u'''[{}] ActionType.flatCode added prefix 'multivox_' '''.format(dicom_modality_code))


def find_leafs_recursive(group_id, level, c):
    if level >= 30:
        logger.info(u'''Reach depth limit''')
        return list()
    result = list()
    c.execute(query_select_aty_by_group_id.format(group_id))
    for action_type_id, action_type_code, action_type_name in c.fetchall():
        logger.info(u'---->' * level + u'[{}] \'{}\''.format(action_type_id, action_type_name) )
        sub_results = find_leafs_recursive(action_type_id, level+1, c)
        if len(sub_results) == 0:
            result.append(action_type_id)
        else:
            result.extend(sub_results)
    return result


def downgrade(root_action_type_code, c):
    pass