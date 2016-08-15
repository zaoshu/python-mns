#!/usr/bin/env python
# coding: utf-8
__author__ = 'wzy'
__date__ = '2015-07-29 12:22'


import logging
from tornado import gen

from push import default_push_client


@gen.coroutine
def test():
    client = default_push_client()

    # send sms
    yield client.send_template_sms(
        'mobile', 'courier_signup_verify_code', {'code': '1234'}
    )

    # push message to ios app (app store)
    yield client.push_message(
        'user', 'bcb03e21c4a8a266018b015e7b99be56',
        '测试', '测试啊啊吖', data_content={'type': 'order'},
        channel='as'
    )

    # push message to ios app (www.pgyer.com)
    yield client.push_message(
        'user', 'bcb03e21c4a8a266018b015e7b99be56',
        '测试', '测试啊啊吖', data_content={'type': 'order'},
        channel='pgy'
    )

    # push message to android app
    yield client.push_message(
        'user', '735126eb7531f01dbecf1a6be67a0aa9',
        '测试', '测试啊啊吖', data_content={'type': 'order'}
    )

    # push transmission message
    yield client.push_transmission_message(
        'user', '735126eb7531f01dbecf1a6be67a0aa9',
        '测试', '测试啊啊吖', data_content={'type': 'order'}
    )

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    from tornado.ioloop import IOLoop
    IOLoop.instance().run_sync(test)