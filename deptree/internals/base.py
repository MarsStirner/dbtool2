# -*- coding: utf-8 -*-
import functools
import logging
from ConfigParser import ConfigParser

import sys

import MySQLdb
import blinker
import codecs
from deptree.internals.models import BaseNode


logger = logging.getLogger('dbtool')

__author__ = 'viruzzz-kun'


class _DBToolSignalHandler(logging.Handler):
    def __init__(self, signal):
        logging.Handler.__init__(self)
        self.signal = signal

    def emit(self, record):
        text = self.format(record)
        self.signal.send(self, text=text)


# noinspection SqlResolve
class _DBToolBase(object):
    notify_user = blinker.Signal()
    installed_updates = []
    connection = None
    config = None
    dry_run = False
    debug = False
    deep = False
    fake = False
    interactive = True

    def __init__(self, config_filename):
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)

        handler = _DBToolSignalHandler(self.notify_user)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)

        self.config = conf = get_config(config_filename)

        formatter = logging.Formatter(u'%(asctime)s [%(levelname)s] %(message)s')
        try:
            handler = logging.StreamHandler(open(conf['log_filename'], 'at'))
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        except OSError:
            logger.exception()

        self.connection = None

    def __enter__(self):
        logger.info('  --------  Starting... --------')

        self.connection = connection = get_connection(self.config)
        self.installed_updates = []
        try:
            with connection as cursor:
                cursor.execute('SELECT `name` FROM `InstalledDbUpdates`')
                self.installed_updates = [name for (name,) in cursor]
        except MySQLdb.ProgrammingError:
            logger.error(u"В базе данных не найдена таблица `InstalledDbUpdates`. "
                         u"БД не готова к миграциям dbTool2.")
        DBToolBaseNode.connection = self.connection
        DBToolBaseNode.config = self.config

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        self.connection = None
        self.installed_updates = []

        logger.info('  --------  Finished --------')

    def _proceed(self):
        if self.interactive:
            sys.stdout.write(u'Продолжить? [y/N] ')
            return raw_input().lower() == 'y'
        return True

    def _format_db_name(self):
        return u'mysql://%(host)s:%(port)s/%(dbname)s' % self.config


class DBToolBaseNode(BaseNode):
    __root__ = True
    depends = []

    connection = None
    config = None


def db_transactional(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
        except:
            logger.exception('perform update exc')
            if self.connection:
                self.connection.rollback()
            raise
        else:
            if self.connection:
                self.connection.commit()
            return result
    return wrapper


def get_config(filename):
    p = ConfigParser(defaults={
        'port': '3306',
        'develop_version': False,
        'update_dir': '.'
    })
    with codecs.open(filename, 'r', 'utf-8-sig') as f:
        p.readfp(f)
    return {
        'host': p.get('database', 'host'),
        'port': p.get('database', 'port'),
        'username': p.get('database', 'username'),
        'password': p.get('database', 'password'),
        'dbname': p.get('database', 'dbname'),
        'definer': p.get('database', 'definer'),
        'content': p.get('content', 'content_type'),
        'log_filename': p.get('misc', 'log_filename'),
        'develop_version': p.get('misc', 'develop_version'),
        'update_dir': p.get('misc', 'update_dir')
    }


def get_connection(config):
    c = MySQLdb.connect(
        host=config['host'],
        port=int(config['port']),
        user=config['username'],
        passwd=config['password'],
        db=config['dbname'],
        charset='utf8',
        use_unicode=True
    )
    c.autocommit(False)
    return c
