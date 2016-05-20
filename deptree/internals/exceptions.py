# -*- coding: utf-8 -*-

__author__ = 'viruzzz-kun'


class DBToolException(Exception):
    pass


class ConfigException(Exception):
    pass


class DbNotReadyForMigrations(DBToolException):
    pass


class BadUpdate(DBToolException):
    pass
