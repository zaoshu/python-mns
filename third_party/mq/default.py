#!/usr/bin/env python
# coding: utf-8
__author__ = 'wzy'
__date__ = '2015-07-31 15:08'


from alimqs_tornado import Client

MQS_HOST = '*'

MQS_ACCESS_ID = '*'
MQS_ACCESS_KEY = '*'

PUSH_QUEUE_NAME = 'MyQueue'
PUSH_QUEUE_NAME_DEBUG = 'MyQueue'


class Default(object):

    debug = True

    client = Client(MQS_HOST, MQS_ACCESS_ID, MQS_ACCESS_KEY)

    @staticmethod
    def default_client():
        return Default.client

    @staticmethod
    def default_push_queue_name():
        if Default.debug:
            return PUSH_QUEUE_NAME_DEBUG
        else:
            return PUSH_QUEUE_NAME
