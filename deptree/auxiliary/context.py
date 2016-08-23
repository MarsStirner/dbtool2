# -*- coding: utf-8 -*-

__author__ = 'viruzzz-kun'


class Context(object):
    current_context = None

    def __init__(self, parent=None):
        object.__setattr__(self, 'parent', parent)
        object.__setattr__(self, 'dict', {})

    def __getattr__(self, item):
        self_dict = object.__getattribute__(self, 'dict')
        self_parent = object.__getattribute__(self, 'parent')
        if item in self_dict:
            return item
        if self_parent:
            return getattr(self_parent, item)
        raise AttributeError(item)

    def __setattr__(self, key, value):
        self_dict = object.__getattribute__(self, 'dict')
        self_dict[key] = value

    def __delattr__(self, item):
        self_dict = object.__getattribute__(self, 'dict')
        if item in self_dict:
            del self_dict[item]

    def __enter__(self):
        new = Context(self)
        Context.current_context = new
        return new

    def __exit__(self, exc_type, exc_val, exc_tb):
        Context.current_context = object.__getattribute__(Context.current_context, 'parent')


