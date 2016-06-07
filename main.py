#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import logging
import sys

from deptree.internals.dbtool import DBTool


__author__ = 'viruzzz-kun'

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='dbtool.conf',
                        help='Use other config file')
    parser.add_argument('--debug', action='store_const', const=True, default=False,
                        help='Make it very verbose')
    parser.add_argument('--dry-run', action='store_const', const=True, default=False,
                        help='Do not actually perform any actions')
    parser.add_argument('--deep', action='store_const', const=True, default=False,
                        help='Process dependencies even if update is salready installed')
    subparsers = parser.add_subparsers(title=u'Команды', help=u'Доступные команды')

    sp_upgrade = subparsers.add_parser('upgrade', help=u'Выполнить установку обновлений БД')
    sp_upgrade.add_argument('targets', metavar='target', nargs='+',
                            help='Устанавливаемые обновления')
    sp_upgrade.set_defaults(mode='upgrade')

    # sp_downgrade = subparsers.add_parser('downgrade', help=u'Выполнить удаление обновлений БД')
    # sp_downgrade.add_argument('targets', metavar='target', nargs='+',
    #                           help='Удаляемые обновления')
    # sp_downgrade.set_defaults(mode='downgrade')

    sp_fix_definers = subparsers.add_parser('fix-definers', help=u'Починить DEFINER\'ов в БД')
    sp_fix_definers.set_defaults(mode='fix-definers')

    sp_rls_import = subparsers.add_parser('rls-import', help=u'Импортировать справочник РЛС')
    sp_rls_import.add_argument('path', nargs='?')
    sp_rls_import.set_defaults(mode='rls-import')

    sp_depers = subparsers.add_parser('depersonalize', help=u'Деперсонализировать БД')
    sp_depers.set_defaults(mode='depersonalize')


    args = parser.parse_args(sys.argv[1:])

    db_tool = DBTool(args.config)
    db_tool.dry_run = args.dry_run
    db_tool.debug = args.debug
    db_tool.deep = args.deep
    logger = logging.getLogger('dbtool')

    if args.debug:
        logger.setLevel(logging.DEBUG)
    # noinspection PyBroadException
    try:
        with db_tool:
            if args.mode == 'upgrade':
                db_tool.perform_updates(args.targets)
            elif args.mode == 'downgrade':
                db_tool.perform_downgrades(args.targets)
            elif args.mode == 'fix-definers':
                db_tool.change_definers()
            elif args.mode == 'rls-import':
                db_tool.user_rls_import(args.path)
            elif args.mode == 'depersonalize':
                db_tool.perform_depersonalize()
    except:
        logger.exception('Whoops...')

