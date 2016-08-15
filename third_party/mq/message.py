#!/usr/bin/env python
# coding: utf-8
__author__ = 'wzy'
__date__ = '2015-07-31 15:16'


import time
import json

from tornado import gen
from alimqs_tornado import *

from default import Default


def cache_queue(func):
    cache = {}

    @gen.coroutine
    def wrapper(queue, *args, **kwargs):
        if isinstance(queue, basestring):
            obj = cache.get(queue)
            if obj is None:
                obj = Queue(queue, Default.default_client())
                yield obj.create()
                cache[queue] = obj
            queue = obj
        elif isinstance(queue, Client):
            pass
        else:
            raise Exception('queue must be str or Queue')

        yield func(queue, *args, **kwargs)
    return wrapper


@cache_queue
@gen.coroutine
def send(queue, action, ttl=0, delay=0, **kwargs):
    data = {
        'action': action,
        'request_time': int(time.time()) + delay,
        'ttl': ttl,
        'arguments': kwargs
    }
    yield queue.send_message(Message(json.dumps(data), delay=delay))