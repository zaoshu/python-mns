#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import json
import time

from tornado.ioloop import IOLoop

import handlers.mq
from third_party import mq

# from settings.base import LOG_LEVEL, LOG_FORMAT
# from settings.switch import DEBUG
from settings.mq import MQ_SPIDER_SERVICE
from alimqs_tornado.message import Message


def main():
    # logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

    loop = IOLoop.instance()
    # mq.set_debug(debug=DEBUG)
    mq_loop = mq.MQLoop(MQ_SPIDER_SERVICE, loop, handlers.mq.MessageHandler())
    mq_loop.start()

    # message_body = {
    #     "action": "handle",
    #     "request_time": time.time(),
    #     "ttl": "3600",
    #     "arguments": {
    #         "spider": "lagou",
    #         "urls": "http://www.lagou.com/zhaopin"
    #     }
    # }
    # json_encode = json.dumps(message_body)
    #
    # message = Message(json_encode, delay=0, priority=8)
    # mq_loop._queue.send_message(message)

    logging.info('[SpiderService-MQ-LOOPER] Mq loop start')
    loop.start()


if __name__ == "__main__":
    main()
