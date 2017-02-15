# coding: utf-8

from deptree.internals.base import DBToolBaseNode


class RsrSaratovReportsSettings(DBToolBaseNode):
    name = 'rimis-1241'
    depends = ['rimis-1241.1', 'rimis-1241.2']


class RsrJasperReportsSettings(DBToolBaseNode):
    name = 'rimis-1241.1'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
CREATE TABLE `RisarReports` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `template_uri` VARCHAR(255) NOT NULL COMMENT 'код шаблона, определенный в JasperReports',
  `redirect_url` VARCHAR(512) NULL DEFAULT NULL COMMENT 'url внешней системы, куда будет совершен редирект, и где будет происходить работа с отчетом (содержит части path и query)',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = 'Дополнительные настройки по отчетам Jasper';
''')


class RsrSaratovReportsRedirects(DBToolBaseNode):
    name = 'rimis-1241.2'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            data = [
                (u'/reports/Hippocrates/Analytics/Social_analytics', u'/ws/cas_risar?page=ANALYSIS_SOCIAL_PREG_CALL'),
                (u'/reports/Hippocrates/Analytics/RIMIS_1022', u'/ws/cas_risar?page=INF_PREG_REFUSED_CALL'),
                (u'/reports/Hippocrates/Analytics/report_diseases', u'/ws/cas_risar?page=PATIENTS_BY_DISEASE_CALL'),
                (u'/reports/Hippocrates/Analytics/inducpregnan', u'/ws/cas_risar?page=PREG_MONIT_CALL'),
                (u'/reports/Hippocrates/Analytics/report_med_interrupts', u'/ws/cas_risar?page=ANALYSIS_PREG_ABORTS_CALL'),
                (u'/reports/Hippocrates/Analytics/REPORT_PREG_POROK_CALL', u'/ws/cas_risar?page=REPORT_PREG_POROK_CALL'),
                (u'/reports/Hippocrates/Analytics/CERT_MONITORING_CALL', u'/ws/cas_risar?page=CERT_MONITORING_CALL'),
                (u'/reports/Hippocrates/Analytics/NEONATAL_OPER_DATA_CALL', u'/ws/cas_risar?page=NEONATAL_OPER_DATA_CALL'),
                (u'/reports/Hippocrates/Analytics/predicated_delivery_date.pdf', u'/ws/cas_risar?page=EXPECTED_BIRTHDATE_CALL'),
                (u'/reports/Hippocrates/Analytics/PREGNACY_VPR_CALL', u'/ws/cas_risar?page=PREGNACY_VPR_CALL'),
                (u'/reports/Hippocrates/Analytics/trimester', u'/ws/cas_risar?page=PREG_TRIMESTERS_CALL'),
                (u'/reports/Hippocrates/Analytics/COUNT_CHILDBIRTH_CALL', u'/ws/cas_risar?page=COUNT_CHILDBIRTH_CALL'),
                (u'/reports/Hippocrates/Analytics/COUNT_PREG_EVENT_CALL', u'/ws/cas_risar?page=COUNT_PREG_EVENT_CALL'),
                (u'/reports/Hippocrates/Analytics/REPORT_DETAIL_CALL', u'/ws/cas_risar?page=REPORT_DETAIL_CALL'),
                (u'/reports/Hippocrates/Analytics/JOURNAL_STAT_REPORTS_CALL', u'/ws/cas_risar?page=JOURNAL_STAT_REPORTS_CALL')
            ]
            c.executemany(u'''
INSERT INTO `RisarReports` (`template_uri`, `redirect_url`) VALUES (%s, %s);
''', data)
