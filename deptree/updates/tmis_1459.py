# coding: utf-8


from deptree.internals.base import DBToolBaseNode


class DBUpdate(DBToolBaseNode):
    name = 'tmis-1459'
    depends = ['tmis-1459.update_flat_code', 'tmis-1459.add_user_right', ]


class UpdateFlatCode(DBToolBaseNode):
    name = 'tmis-1459.update_flat_code'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''UPDATE `ActionType` SET `flatCode`='leaved' WHERE `name`='Выписной эпикриз';''')


class AddUserRight(DBToolBaseNode):
    name = 'tmis-1459.add_user_right'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            new_rights = [
                ('evtClinicCreate', u'Имеет возможность создавать обращения в дневной стационар'),
                ('evtClinicClose', u'Имеет возможность закрывать обращения в дневной стационар'),
                ('evtHospitalCreate', u'Имеет возможность создавать обращения в круглосуточный стационар'),
                ('evtHospitalClose', u'Имеет возможность закрывать обращения в круглосуточный стационар'),
            ]
            c.executemany(u'''INSERT INTO `rbUserRight` (`code`, `name`) VALUES (%s, %s);''', new_rights)
