# coding: utf-8
from deptree.internals.base import DBToolBaseNode


class UserPermissionsUpdate(DBToolBaseNode):
    name = 'tmis-1382'
    depends = ['tmis-1382.rbFinance_update', 'tmis-1382.rb_user_profile_right_update']


class RbFinanceUpdate(DBToolBaseNode):
    name = 'tmis-1382.rbFinance_update'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
INSERT INTO `rbUserRight` (`code`, `name`) VALUES ('evtPoliclinicOmsMoCreate', 'Имеет возможность создавать поликлинические обращения ОМС МО');
''')
            c.execute(u'''
INSERT INTO `rbUserRight` (`code`, `name`) VALUES ('evtPoliclinicOmsMoClose', 'Имеет возможность закрывать поликлинические обращения ОМС МО');
''')


class RbUserProfileRightUpdate(DBToolBaseNode):
    name = 'tmis-1382.rb_user_profile_right_update'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'SELECT id FROM rbUserProfile WHERE code in ("clinicDoctor", "strDoctor") ORDER BY code;')
            id_clinic_doc = c.fetchone()[0]     # Врач поликлиники
            id_str_doc = c.fetchone()[0]        # Врач отделения

            c.execute(u'SELECT id FROM rbUserRight WHERE code in ("evtPoliclinicOmsMoClose", "evtPoliclinicOmsMoCreate") ORDER BY code;')
            id_close = c.fetchone()[0]          # Возможность закрывать поликлинические обращения ОМС МО
            id_create = c.fetchone()[0]         # Возможность создавать поликлинические обращения ОМС МО

            data = []
            for doc_id in (id_clinic_doc, id_str_doc):
                for permission_id in (id_close, id_create):
                    data.append((doc_id, permission_id))

            c.executemany(u'''
INSERT INTO `rbUserProfile_Right` (`master_id`, `userRight_id`) VALUES (%s, %s);
''', data)
