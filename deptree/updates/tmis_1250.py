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


action_property_type_result = {
    'name':u'Ссылка на результат исследования',
    'descr':u'Ссылка на результат исследования',
    'typeName':u'URL',
    'code':u'multivox_result',
    'sex':0,
    'age': '',
    'mandatory':0,
    'readOnly':1
}

action_property_type_send_time = {
    'name':u'Время отправки сообщения в очередь',
    'descr':u'Время отправки сообщения в очередь',
    'typeName':u'Time',
    'code':u'multivox_send_time',
    'sex':0,
    'age': '',
    'mandatory':0,
    'readOnly':1
}

action_property_type_send_date = {
    'name':u'Дата отправки сообщения в очередь',
    'descr':u'Дата отправки сообщения в очередь',
    'typeName':u'Date',
    'code':u'multivox_send_date',
    'sex':0,
    'age': '',
    'mandatory':0,
    'readOnly':1
}

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
AND id IN ({})
'''
query_select_apt_by_aty_and_code=u'''
SELECT apt.id
FROM ActionPropertyType apt
WHERE apt.actionType_id = {}
AND apt.code = '{}'
ORDER BY apt.deleted ASC
LIMIT 1
'''

def modify_diagnostic_action_type_tree(dicom_modality_code, root_action_type_title, c):
    c.execute(query_select_diagnostic_aty_id_by_title.format(root_action_type_title))
    action_type_id, action_type_code, action_type_name = c.fetchone()
    logger.info(u'''[{0}] Root is ActionType[{1}] code='{2}' name='{3}' '''.format(
        dicom_modality_code,
        action_type_id,
        action_type_code,
        action_type_name
    ))
    c.execute(query_update_action_type_mnemonic.format(dicom_modality_code, action_type_id))
    leafs = find_leafs_recursive(action_type_id, 0, c)
    logger.info(u'[{0}] Need to modify ActionTypes: {1}'.format(dicom_modality_code, u','.join(str(x) for x in leafs)))
    c.execute(query_update_action_type_mnemonic.format(dicom_modality_code, u','.join(str(x) for x in leafs)))
    logger.info(u'''[{0}] ActionType.mnem is set to '{0}' '''.format(dicom_modality_code))
    c.execute(query_update_action_type_flat_code.format(u','.join(str(x) for x in leafs)))
    logger.info(u'''[{0}] ActionType.flatCode added prefix 'multivox_' '''.format(dicom_modality_code))
    modify_action_property_types(leafs, c)


def find_leafs_recursive(group_id, level, c):
    if level >= 30:
        logger.info(u'''Reach depth limit''')
        return []
    result = []
    c.execute(query_select_aty_by_group_id.format(group_id))
    for action_type_id, action_type_code, action_type_name in c.fetchall():
        logger.info(u'---->' * level + u'[{0}] \'{1}\''.format(action_type_id, action_type_name) )
        sub_results = find_leafs_recursive(action_type_id, level+1, c)
        if len(sub_results) == 0:
            result.append(action_type_id)
        else:
            result.extend(sub_results)
    return result


def modify_action_property_types(action_type_ids, c):
    for action_type_id in action_type_ids:
        modify_action_property_type(action_type_id, action_property_type_result, c)
        modify_action_property_type(action_type_id, action_property_type_send_date, c)
        modify_action_property_type(action_type_id, action_property_type_send_time, c)


query_insert_apt=u'''
INSERT INTO ActionPropertyType(
    `deleted`, `actionType_id`, `name`, `descr`, `typeName`, `valueDomain`,
    `defaultValue`, `code`, `norm`, `sex`, `age`, `mandatory`, `readOnly`,
    `createDatetime`, `modifyDatetime`
) VALUES (
    0, {}, '{}', '{}', '{}', '',
    '', '{}', '', {}, '{}', {}, {},
    CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()
);
'''
query_update_apt=u'''
UPDATE ActionPropertyType SET
    `deleted` = 0, `actionType_id`= {}, `name`='{}', `descr`='{}', `typeName`='{}', `valueDomain`='',
    `defaultValue`='', `code`='{}', `norm`='', `sex`={}, `age`='{}', `mandatory`={}, `readOnly`={},
    `modifyDatetime`= CURRENT_TIMESTAMP()
WHERE id = {};
'''

def modify_action_property_type(action_type_id, prop, c):
    c.execute(query_select_apt_by_aty_and_code.format(action_type_id, prop['code']))
    query_result = c.fetchone()
    if query_result:
        #TODO typeName check AND fetchAll -> set deleted = 1 to all but one
        c.execute(query_update_apt.format(
            action_type_id, prop['name'], prop['descr'], prop['typeName'],
            prop['code'], prop['sex'], prop['age'], prop['mandatory'], prop['readOnly'], query_result[0]))
        logger.info(u'''ActionType[{0}]: APT['{1}'] updated [{2}]'''.format(action_type_id, prop['code'], query_result[0]))
    else:
        c.execute(query_insert_apt.format(
            action_type_id, prop['name'], prop['descr'], prop['typeName'],
            prop['code'], prop['sex'], prop['age'], prop['mandatory'], prop['readOnly']))
        logger.info(u'''ActionType[{0}]: APT['{1}'] inserted [{2}]'''.format(action_type_id, prop['code'], c.lastrowid))


query_update_apt_set_deleted_by_aty_ids_and_codes = u'''
UPDATE ActionPropertyType SET `deleted` = 1, `modifyDatetime`= CURRENT_TIMESTAMP() WHERE code ='{0}' AND actionType_id IN ({1})
'''

def downgrade(root_action_type_title, c):
    logger.info(u'ActionType.mnem and ActionType.flatCode cannot be recovered')
    c.execute(query_select_diagnostic_aty_id_by_title.format(root_action_type_title))
    action_type_id, action_type_code, action_type_name = c.fetchone()
    logger.info(u'''[{0}] Root is ActionType[{1}] code='{2}' name='{3}' '''.format(
        u'DOWNGRADE',
        action_type_id,
        action_type_code,
        action_type_name
    ))
    leafs = find_leafs_recursive(action_type_id, 0, c)
    aty_ids = u','.join(str(x) for x in leafs)
    logger.info(u'[{0}] Need to modify ActionTypes: {1}'.format(u'DOWNGRADE', aty_ids))
    c.execute(query_update_apt_set_deleted_by_aty_ids_and_codes.format(action_property_type_result['code'], aty_ids))
    c.execute(query_update_apt_set_deleted_by_aty_ids_and_codes.format(action_property_type_send_date['code'], aty_ids))
    c.execute(query_update_apt_set_deleted_by_aty_ids_and_codes.format(action_property_type_send_time['code'], aty_ids))