#!/usr/bin/env python
# coding: utf-8
__author__ = 'wzy'
__date__ = '2015-09-01 15:25'


from tornado import gen
from bson import ObjectId

#
# class MessageHandler(object):
#
#     @gen.coroutine
#     def ConfirmOrder(self, shop_id, order_id, confirm_time, items_price, delivery_price):
#         yield PutToShopAccount().action(
#             ObjectId(shop_id), ObjectId(order_id),
#             confirm_time, items_price, delivery_price
#         )
#
#     @gen.coroutine
#     def new_order(self, order_id, paid_time):
#         yield OnNewOrder().action(ObjectId(order_id), paid_time)


class MessageHandler(object):
    @gen.coroutine
    def handle(self, **kwargs):
        pass