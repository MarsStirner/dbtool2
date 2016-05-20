# -*- coding: utf-8 -*-

from deptree.capabilities.definers import _DBToolDefinerChanger
from deptree.capabilities.depersonalize import _DBToolDepersonalize
from deptree.capabilities.downgrade import _DBToolDowngrader
from deptree.capabilities.rls import _DBToolRlsImport
from deptree.capabilities.upgrade import _DBToolUpgrader

# noinspection PyUnresolvedReferences
from deptree import updates


__author__ = 'viruzzz-kun'


class DBTool(_DBToolUpgrader, _DBToolDowngrader, _DBToolDefinerChanger, _DBToolRlsImport, _DBToolDepersonalize):
    pass

