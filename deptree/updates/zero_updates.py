# -*- coding: utf-8 -*-
from deptree.internals.base import DBToolBaseNode

__author__ = 'viruzzz-kun'


class ZeroUpdate1(DBToolBaseNode):
    name = 'zero.1'
    depends = []

    @classmethod
    def upgrade(cls):
        pass

    @classmethod
    def downgrade(cls):
        pass


class ZeroUpdate2(DBToolBaseNode):
    name = 'zero.2'
    depends = ['zero.1']

    @classmethod
    def upgrade(cls):
        pass

    @classmethod
    def downgrade(cls):
        pass


class ZeroUpdate3(DBToolBaseNode):
    name = 'zero.3'
    depends = ['zero.2', 'zero.1']

    @classmethod
    def upgrade(cls):
        pass

    @classmethod
    def downgrade(cls):
        pass


class ZeroUpdate4(DBToolBaseNode):
    name = 'zero.4'
    depends = ['zero.1', 'zero.2']

    @classmethod
    def upgrade(cls):
        pass

    @classmethod
    def downgrade(cls):
        pass


class ZeroUpdate5(DBToolBaseNode):
    name = 'zero.5'
    depends = ['zero.4']

    @classmethod
    def upgrade(cls):
        pass

    @classmethod
    def downgrade(cls):
        pass

