# -*- coding: utf-8 -*-
import logging

from deptree.internals.base import DBToolBaseNode

logger = logging.getLogger('dbtool')


class Rimis1455(DBToolBaseNode):
    name = 'rimis-1455'
    depends = [
        'rimis-1455.person-columns',
        'rimis-1455.tblcert-type',
        'rimis-1455.tblqual',
        'rimis-1455.pcert',
        'rimis-1455.fill-doc-qual',
        'rimis-1455.fill-cert-type'
    ]


class ColumnsQualificationCertificate(DBToolBaseNode):
    name = 'rimis-1455.person-columns'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
              ALTER TABLE Person
              ADD COLUMN `qualification_id` INT(11) NULL   COMMENT 'Квалификация врача {PersonQualification}' AFTER `speciality_id`,
              ADD COLUMN `cert_id` INT NULL   COMMENT 'Сертификат врача {PersonCertificate}' AFTER `qualification_id`;'''
                      )


class rbDoctorCertificateType(DBToolBaseNode):
    name = 'rimis-1455.tblcert-type'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
                    CREATE TABLE rbDoctorCertificateType
                    (
                        id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
                        code VARCHAR(255),
                        name VARCHAR(255)
                    );'''
                      )


class rbDoctorQualification(DBToolBaseNode):
    name = 'rimis-1455.tblqual'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
                    CREATE TABLE rbDoctorQualification
                        (
                            id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
                            code VARCHAR(255),
                            name VARCHAR(255)
                        );'''
                      )


class PersonCertificate(DBToolBaseNode):
    name = 'rimis-1455.pcert'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
                    CREATE TABLE PersonCertificate
                    (
                        id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
                        number VARCHAR(16),
                        created DATETIME,
                        start_date DATETIME,
                        end_date DATETIME,
                        cert_type_id INT(11),
                        deleted INT(11)
                    );
            '''
                      )


class FillrbDoctorQualification(DBToolBaseNode):
    name = 'rimis-1455.fill-doc-qual'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''INSERT INTO rbDoctorQualification (code, name) VALUES
                                            ('first', 'Первая квалификационная категория'),
                                            ('second', 'Вторая квалификационная категория'),
                                            ('highest', 'Высшая квалификационная категория');
            ''')


class FillrbDoctorCertificateType(DBToolBaseNode):
    name = 'rimis-1455.fill-cert-type'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''INSERT INTO rbDoctorCertificateType (code, name) VALUES
                        ('obstetrics_and_gynecology', 'Акушерство и гинекология'),
                        ('genetics', 'Генетика'),
                        ('dietetics', 'Диетология'),
                        ('dermatology', 'Дерматовенерология'),
                        ('immunology', 'Иммунология'),
                        ('inektologiya', 'Инектология'),
                        ('cardiology', 'Кардиология'),
                        ('clinical_and_laboratory_diagnosis', 'Клиническая и лабораторная диагностика'),
                        ('coloproctology', 'Колопроктология'),
                        ('therapeutic_exercise_and_sports_medicine', 'Лечебная физкультура и спортивная медицина'),
                        ('neurology', 'Неврология'),
                        ('general_practice_family_medicine', 'Общая врачебная практика (семейная медицина)'),
                        ('otolaryngology', 'Отоларингология'),
                        ('pediatrics', 'Педиатрия'),
                        ('psychiatry', 'Психиатрия'),
                        ('rheumatology', 'Ревматология'),
                        ('stomatology', 'Стоматология'),
                        ('therapy', 'Терапия'),
                        ('urology', 'Урология'),
                        ('physiotherapy', 'Физиотерапия'),
                        ('functional_diagnostics', 'Функциональная диагностика'),
                        ('surgery', 'Хирургия'),
                        ('endocrinology', 'Эндокринология'),
                        ('obstetrics_and_gynecology', 'Акушерство и гинекология')
            ''')
