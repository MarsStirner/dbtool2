# -*- coding: utf-8 -*-
import logging
from copy import copy

__author__ = 'viruzzz-kun'


logger = logging.getLogger('deptoolmodels')


class DependencyException(Exception):
    def __init__(self, node_name, stack):
        self.__node_name = node_name
        self.__stack = stack

    def __unicode__(self):
        return u'<%s (%s, ["%s"])>' % (
            self.__class__.__name__,
            self.__node_name,
            u'", "'.join(self.__stack),
        )

    def __str__(self):
        return '<%s (%s, ["%s"])>' % (
            self.__class__.__name__,
            self.__node_name,
            '", "'.join(self.__stack),
        )

    @property
    def node_name(self):
        return self.__node_name


class DependencyNotFound(DependencyException):
    pass


class CircularDependency(DependencyException):
    pass


class NodeMeta(type):
    name = None

    def __new__(mcs, class_name, bases, kwargs):
        registry_name = kwargs.get('name', class_name)
        kwargs['name'] = registry_name
        logger.debug('Registering class %s (%s)...', class_name, registry_name)

        is_root = kwargs.pop('__root__', False)
        is_abstract = kwargs.pop('__abstract__', False)

        cls = type.__new__(mcs, class_name, bases, kwargs)
        if is_root:
            logger.debug('class %s (%s) is __root__', class_name, registry_name)
            cls._registry = {}
        else:
            if registry_name in cls._registry:
                raise RuntimeError(u'Class %s (%s) already registered' % (class_name, registry_name))
            if not is_abstract:
                cls._registry[registry_name] = cls
            else:
                logger.debug('class %s (%s) is __abstract__', class_name, registry_name)
        return cls

    def get(cls, name):
        if name not in cls._registry:
            raise DependencyNotFound(name, [])
        return cls._registry[name]

    def get_all_nodes(cls):
        return copy(cls._registry)

    def dependents(cls, targets, whitelist):
        class Restart():
            pass
        retargets = set(targets)
        result = []
        pool = set(whitelist) - retargets
        max_iterations = len(pool)
        for _ in xrange(max_iterations):
            try:
                for name in copy(pool):
                    if name not in retargets:
                        node = cls._registry[name]
                        for test in node.depends:
                            if test in retargets:
                                pool.remove(name)
                                retargets.add(name)
                                result.append(name)
                                raise Restart
            except Restart:
                continue
            else:
                break
        result.reverse()
        return result

    def resolve(cls, *stops):
        stops = set(stops)
        result = []
        stack = []

        def resolve_aux(node_name):
            if node_name in stack:
                raise CircularDependency(node_name, stack)
            if node_name in stops:
                return
            if node_name in result:
                return

            stack.append(node_name)

            kls = cls._registry.get(node_name)
            if kls is None:
                raise DependencyNotFound(node_name, stack)

            for name in kls.depends:
                resolve_aux(name)

            if node_name not in result:
                result.append(node_name)

            stack.pop()

        resolve_aux(cls.name)
        return result


class BaseNode(object):
    __metaclass__ = NodeMeta
    __root__ = True
    depends = []


logger.setLevel(logging.ERROR)
logger.addHandler(logging.StreamHandler())
