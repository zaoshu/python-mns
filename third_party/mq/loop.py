#!/usr/bin/env python
# coding: utf-8
__author__ = 'wzy'
__date__ = '2015-07-31 15:16'


import logging
import json
import time

from tornado import gen
from tornado.httpclient import HTTPError
from alimqs_tornado import Client, Queue

from default import Default


class MQLoop(object):

    def __init__(self, queue, ioloop, handler):
        self._queue = queue
        self._ioloop = ioloop
        self._handler = handler

    @gen.coroutine
    def _loop(self):
        try:
            msg = yield self._queue.receive_message()
            if msg:
                logging.info(msg.body)
                task = self._parse_task(msg.body)
                if task is not None:
                    func = self._get_function(task['action'])
                    if func is not None:
                        try:
                            yield self._handle(func, **task)
                        except Exception as e:
                            logging.exception('ERROR when handle message %s', msg.body)
                        finally:
                            # delete message, no matter success or exception
                            yield self._queue.delete_message(msg)
                    else:
                        logging.error('there is no function to handle message %s, do not delete it', msg.body)
                        # do not delete message
                else:
                    # parse message error, delete it
                    yield self._queue.delete_message(msg)

            # start next loop now
            self._ioloop.add_callback(self._loop)
            return
        except HTTPError as e:
            logging.error(e)
        except Exception:
            logging.exception('ERROR in MessageQueue Loop')

        # error happens, start next loop 3 seconds later
        self._ioloop.add_timeout(time.time() + 3, self._loop)

    def _parse_task(self, body):
        try:
            return json.loads(body)
        except:
            logging.exception('ERROR when parse message %s', body)
        return None

    def _get_function(self, action):
        if not action.startswith('_'):
            func = getattr(self._handler, action)
            if func and callable(func):
                return func

        return None

    @gen.coroutine
    def _handle(self, func, action, request_time, ttl, arguments):
        if arguments is None:
            arguments = {}

        if ttl > 0:
            passed = int(time.time()) - request_time
            if passed > ttl:
                raise Exception('message expire, action %s, arguments: %s' % (action, arguments))

        yield func(**arguments)

    def start(self):
        if isinstance(self._queue, basestring):
            obj = Queue(self._queue, Default.default_client())
            self._ioloop.run_sync(obj.create)
            self._queue = obj
        elif isinstance(self._queue, Client):
            pass
        else:
            raise Exception('queue must be str or Queue')

        self._ioloop.add_callback(self._loop)