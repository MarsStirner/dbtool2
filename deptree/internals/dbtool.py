# -*- coding: utf-8 -*-

from deptree.capabilities.definers import _DBToolDefinerChanger
from deptree.capabilities.depersonalize import _DBToolDepersonalize
from deptree.capabilities.downgrade import _DBToolDowngrader
from deptree.capabilities.rls import _DBToolRlsImport
from deptree.capabilities.upgrade import _DBToolUpgrader
from deptree.capabilities.init_db import _DBToolInitDB

# noinspection PyUnresolvedReferences
from deptree import updates


__author__ = 'viruzzz-kun'


class DBTool(_DBToolUpgrader, _DBToolDowngrader, _DBToolDefinerChanger, _DBToolRlsImport,
             _DBToolDepersonalize, _DBToolInitDB):
    pass

