#!/usr/bin/env python
# coding: utf-8
__author__ = 'wzy'
__date__ = '2015-09-01 15:25'


from tornado import gen


class MessageHandler(object):
    @gen.coroutine
    def handle(self, **kwargs):
        pass