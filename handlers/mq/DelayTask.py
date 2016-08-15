#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'paincompiler'
__date__ = '11/18/15'


from tornado import gen
from bson import ObjectId
# from behaviors import ProcessTimeout, PreorderUtil, RedPacketUtil
#
#
# class DelayTask(object):
#
#     @gen.coroutine
#     def notify_user_to_process_by_sms(self, user_id, order_id):
#         yield ProcessTimeout().action(
#             ObjectId(user_id), ObjectId(order_id)
#         )
#
#     @gen.coroutine
#     def notify_user_to_ship_preorder_by_push_notification(self, user_id, order_id):
#         yield PreorderUtil().notify_user_of_preorder_shipping(ObjectId(user_id), ObjectId(order_id))
#
#
#     @gen.coroutine
#     def recycle_unclaimed_red_packet_money(self, shop_id, red_packet_id):
#         yield RedPacketUtil(ObjectId(shop_id)).check_and_recycle_remaining(ObjectId(red_packet_id))
