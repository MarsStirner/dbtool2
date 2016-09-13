# coding: utf-8

from deptree. internals.base import DBToolBaseNode

siql=u'''update ActionPropertyType apt set deleted=1 where apt.code in ('duration', 'period_duration')
                                                          and apt.actionType_id in
                                           (select id from ActionType at where at.flatCode= "gynecological_visit_general_anamnesis");
          INSERT INTO ActionPropertyType (deleted, actionType_id, idx, template_id, name, descr, unit_id, typeName, valueDomain, defaultValue, code, isVector, norm, sex, age, age_bu, age_bc, age_eu, age_ec, penalty, visibleInJobTicket, isAssignable, test_id, defaultEvaluation, toEpicrisis, mandatory, readOnly, createDatetime, createPerson_id, modifyDatetime, modifyPerson_id) VALUES (0, 4563, 1, null, 'Длительность', '', null, 'String', '', '', 'duration', 0, '', 0, '', null, null, null, null, 0, 0, 0, null, 0, 0, 0, 0, now(), 181, now(), 181);
          INSERT INTO ActionPropertyType (deleted, actionType_id, idx, template_id, name, descr, unit_id, typeName, valueDomain, defaultValue, code, isVector, norm, sex, age, age_bu, age_bc, age_eu, age_ec, penalty, visibleInJobTicket, isAssignable, test_id, defaultEvaluation, toEpicrisis, mandatory, readOnly, createDatetime, createPerson_id, modifyDatetime, modifyPerson_id) VALUES (0, 4563, 2, null, 'Продолжительность цикла', '', null, 'String', '', '', 'period_duration', 0, '', 0, '', null, null, null, null, 0, 0, 0, null, 0, 0, 0, 0, now(), 181, now(), 181);
                                           '''

class GynecologicalAnamnesisDurationPeriod(DBToolBaseNode):
    name = 'rimis-1309'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(siql)
