#!/usr/bin/env python
# coding: utf-8
__author__ = 'wzy'
__date__ = '2015-07-29 13:27'

import json

from tornado import gen

from default import Default
from message import send


class PushClient(object):

    default_client = None

    def __init__(self, queue):
        self._queue = queue

    @gen.coroutine
    def _send(self, action, ttl=0, **kwargs):
        yield send(self._queue, action, ttl=ttl, **kwargs)

    @gen.coroutine
    def send_template_sms(self, mobile, template, template_args=None, ttl=0):
        if template_args:
            template_args = json.dumps(template_args)
        else:
            template_args = ''

        yield self._send(
            'SendSMS', ttl,
            mobile=mobile, type='template',
            template=template, template_args=template_args
        )

    @gen.coroutine
    def _push(self, type, app_name, client_ids, title, content,
              logo=None, logo_url=None, data_content=None, ttl=0, **kwargs):
        if isinstance(client_ids, list) or isinstance(client_ids, tuple):
            pass
        else:
            client_ids = [client_ids]

        if data_content is None:
            data_content = {}

        yield self._send(
            'Push', ttl,
            app_name=app_name, client_ids=client_ids, type=type,
            title=title, content=content, logo=logo,
            logo_url=logo_url, data_content=data_content,
            **kwargs
        )

    @gen.coroutine
    def push_transmission_message(
            self, app_name, client_ids, title, content,
            logo=None, logo_url=None, data_content=None,
            ttl=0, channel='android', **kwargs):
        yield self._push(
            'transmission', self._format_app_name(app_name, channel),
            client_ids, title, content,
            logo, logo_url, data_content, ttl,
            **kwargs
        )

    @gen.coroutine
    def push_message(
            self, app_name, client_ids, title, content,
            logo=None, logo_url=None, data_content=None,
            ttl=0, channel='android', **kwargs):
        type = 'notification' if channel == 'android' else 'transmission'

        yield self._push(
            type, self._format_app_name(app_name, channel),
            client_ids, title, content,
            logo, logo_url, data_content, ttl,
            **kwargs
        )

    def _format_app_name(self, app_name, channel):
        if channel == 'as':
            app_name += '-app-store'
        return app_name


def default_push_client():
    if PushClient.default_client is None:
        PushClient.default_client = PushClient(Default.default_push_queue_name())
    return PushClient.default_client