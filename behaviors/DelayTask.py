#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'paincompiler'
__date__ = '11/18/15'

from tornado import gen

from settings.mq import MQ_DELAY_TASK
from third_party.mq import message


class DelayTask(object):

    @gen.coroutine
    def notify_user_to_process_by_sms(self, user_id, order_id, delay):
        yield message.send(
            MQ_DELAY_TASK,
            'notify_user_to_process_by_sms',
            delay=delay,
            user_id=str(user_id),
            order_id=str(order_id)
        )

    @gen.coroutine
    def notify_user_to_ship_preorder_by_push_notification(self, user_id, order_id, delay):
        yield message.send(
            MQ_DELAY_TASK,
            'notify_user_to_ship_preorder_by_push_notification',
            delay=delay,
            user_id=str(user_id),
            order_id=str(order_id)
        )

    @gen.coroutine
    def recycle_unclaimed_red_packet_money(self, shop_id, red_packet_id, delay):
        yield message.send(
            MQ_DELAY_TASK,
            'recycle_unclaimed_red_packet_money',
            delay=delay,
            shop_id=str(shop_id),
            red_packet_id=str(red_packet_id)
        )
