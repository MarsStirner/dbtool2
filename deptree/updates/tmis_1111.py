# -*- coding: utf-8 -*-
import math
import logging

from decimal import Decimal

from deptree.internals.base import DBToolBaseNode


logger = logging.getLogger('dbtool')


class ServiceTotalSumOptimisation(DBToolBaseNode):
    name = 'tmis-1111'
    depends = ['tmis-1111.1', 'tmis-1111.2']


class ServiceTotalSumColumn(DBToolBaseNode):
    name = 'tmis-1111.1'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''
ALTER TABLE `Service`
ADD COLUMN `sum` DECIMAL(15,2) NOT NULL DEFAULT 0 AFTER `external_id`;
''')


class ServiceTotalSumMigration(DBToolBaseNode):
    name = 'tmis-1111.2'
    depends = ['tmis-1111.1']

    @classmethod
    def upgrade(cls):
        logger.info(u'Миграция данных по стоимостям услуг')
        with cls.connection as c:
            offset = 100
            cur_offset = 0
            c.execute(u'select count(*) from Service where parent_id is null;')
            num_of_services = c.fetchone()[0]
            logger.info(u'Количество корневых услуг: {0}'.format(num_of_services))
            num_of_iterations = int(math.ceil(float(num_of_services) / offset))
            for i in xrange(num_of_iterations):
                c.execute(u'''
select
    Service.id, Service.serviceKind_id, Service.amount, PriceListItem.serviceNameOW,
    PriceListItem.price, ServiceDiscount.valuePct, PriceListItem.isAccumulativePrice
from
    Service
    inner join PriceListItem on Service.priceListItem_id = PriceListItem.id
    left join ServiceDiscount on Service.discount_id = ServiceDiscount.id
where
    parent_id is null
limit {0}, {1};
'''.format(cur_offset, offset))
                for service_id, service_kind_id, amount, name, price,\
                        discount_val, is_acc_price in c.fetchall():
                    if service_kind_id == ServiceKind.lab_action:
                        # has subservices
                        subservice_list = get_subservices(cls.connection, service_id)
                        if is_acc_price:
                            # sum from subservices
                            service_sum = 0
                            logger.info(u'\ Услуга {0} id = {1} ...'.format(name, service_id))
                            for _service_id, _service_kind_id, _amount, _name, _deleted,\
                                    _price, _discount_val in subservice_list:
                                sum_ = calc_item_sum(_price, _amount, _discount_val)
                                logger.info(u' - Подуслуга {0} id = {1}, цена = {2}'.format(_name, _service_id, sum_))
                                update_service_sum(cls.connection, _service_id, sum_)
                                if _deleted == 0:
                                    service_sum += sum_
                            logger.info(u'/ ... стоимостью {0}'.format(service_sum))
                            update_service_sum(cls.connection, service_id, service_sum)
                        else:
                            # sum is fixed, subservices have 0 sum
                            sum_ = calc_item_sum(price, amount, discount_val)
                            logger.info(u'\ Услуга {0} id = {1}, цена = {2}'.format(name, service_id, sum_))
                            update_service_sum(cls.connection, service_id, sum_)
                            for _service_id, _service_kind_id, _amount, _name, _deleted,\
                                    _price, _discount_val in subservice_list:
                                sum_ = 0
                                logger.info(u' - Подуслуга {0} id = {1}, цена = {2}'.format(_name, _service_id, sum_))
                                update_service_sum(cls.connection, _service_id, sum_)
                    else:
                        # simple service
                        sum_ = calc_item_sum(price, amount, discount_val)
                        logger.info(u'+ Услуга {0} id = {1}, цена = {2}'.format(name, service_id, sum_))
                        update_service_sum(cls.connection, service_id, sum_)

                cur_offset += offset


def update_service_sum(conn, service_id, sum_):
    cursor = conn.cursor()
    cursor.execute(u'update Service set sum = {0} where id = {1}'.format(sum_, service_id))
    cursor.close()


def get_subservices(conn, service_id):
    cursor = conn.cursor()
    cursor.execute(u'''
select
    Service.id, Service.serviceKind_id, Service.amount, PriceListItem.serviceNameOW,
    Service.deleted, PriceListItem.price, ServiceDiscount.valuePct
from
    Service
    inner join PriceListItem on Service.priceListItem_id = PriceListItem.id
    left join ServiceDiscount on Service.discount_id = ServiceDiscount.id
where
    parent_id = {0};
'''.format(service_id))
    subservice_list = cursor.fetchall()
    cursor.close()
    return subservice_list


def calc_item_sum(price, amount, discount_val):
    if discount_val is not None:
        discounted_value = price * safe_decimal(discount_val) / safe_decimal('100')
        price -= discounted_value
    amount = safe_decimal(amount)
    return price * amount


def safe_decimal(val):
    if val is None:
        return None
    val = Decimal(str(val))
    return val


class ServiceKind(object):
    simple_action = 1  # u'Простая услуга'
    group = 2  # u'Набор услуг'
    lab_action = 3  # u'Лабораторное исследование с показателями'
    lab_test = 4  # u'Показатель лабораторного исследования'
