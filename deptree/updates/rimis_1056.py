# -*- coding: utf-8 -*-
from deptree.internals.base import DBToolBaseNode

__author__ = 'viruzzz-kun'


class RIMIS1056(DBToolBaseNode):
    name = 'rimis-1056.1'
    depends = []

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute('''
ALTER TABLE `Person`
    ADD CONSTRAINT `FK_Person_Person` FOREIGN KEY (`createPerson_id`) REFERENCES `Person` (`id`),
    ADD CONSTRAINT `FK_Person_Person_2` FOREIGN KEY (`modifyPerson_id`) REFERENCES `Person` (`id`),
    ADD CONSTRAINT `FK_Person_rbPost` FOREIGN KEY (`post_id`) REFERENCES `rbPost` (`id`),
    ADD CONSTRAINT `FK_Person_rbSpeciality` FOREIGN KEY (`speciality_id`) REFERENCES `rbSpeciality` (`id`),
    ADD CONSTRAINT `FK_Person_Organisation` FOREIGN KEY (`org_id`) REFERENCES `Organisation` (`id`),
    ADD CONSTRAINT `FK_Person_OrgStructure` FOREIGN KEY (`orgStructure_id`) REFERENCES `OrgStructure` (`id`),
    ADD CONSTRAINT `FK_Person_rbTariffCategory` FOREIGN KEY (`tariffCategory_id`) REFERENCES `rbTariffCategory` (`id`),
    ADD CONSTRAINT `FK_Person_rbFinance` FOREIGN KEY (`finance_id`) REFERENCES `rbFinance` (`id`),
    ADD CONSTRAINT `FK_Person_rbUserProfile` FOREIGN KEY (`userProfile_id`) REFERENCES `rbUserProfile` (`id`),
    ADD CONSTRAINT `FK_Person_rbAcademicDegree` FOREIGN KEY (`academicdegree_id`) REFERENCES `rbAcademicDegree` (`id`),
    ADD CONSTRAINT `FK_Person_rbAcademicTitle` FOREIGN KEY (`academicTitle_id`) REFERENCES `rbAcademicTitle` (`id`);
''')

    @classmethod
    def downgrade(cls):
        with cls.connection as c:
            c.execute('''
ALTER TABLE `Person`
    DROP FOREIGN KEY `FK_Person_rbAcademicTitle`,
    DROP FOREIGN KEY `FK_Person_rbAcademicDegree`,
    DROP FOREIGN KEY `FK_Person_rbUserProfile`,
    DROP FOREIGN KEY `FK_Person_rbFinance`,
    DROP FOREIGN KEY `FK_Person_rbTariffCategory`,
    DROP FOREIGN KEY `FK_Person_OrgStructure`,
    DROP FOREIGN KEY `FK_Person_Organisation`,
    DROP FOREIGN KEY `FK_Person_rbSpeciality`,
    DROP FOREIGN KEY `FK_Person_rbPost`,
    DROP FOREIGN KEY `FK_Person_Person_2`,
    DROP FOREIGN KEY `FK_Person_Person`;
''')
