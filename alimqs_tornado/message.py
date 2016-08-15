#!/usr/bin/env python
# coding: utf-8
__author__ = 'wzy'
__date__ = '2015-07-03 19:44'


class Message(object):

    def __init__(self, body, delay=None, priority=None,
                 id=None, receipt=None, md5=None):
        """

        :param body: 消息正文
        :param delay: 指定的秒数延后可被消费，单位为秒。
            0-604800秒（7天）范围内某个整数值，默认值为0
            发送消息时设定
        :param priority: 指定消息的优先级权值。优先级越高的消息，越容易更早被消费。
            取值范围1~16（其中1为最高优先级），默认优先级为8
            发送消息时设定
        :param id: 消息ID，接收消息后自动设置
        :param receipt: 本次获取消息产生的临时句柄，用于删除和修改处于Inactive消息,
            接收消息后自动设置
        :param md5: 消息正文的MD5，接收消息后自动设置
        """
        if body is None:
            raise Exception('Message body must not be None')
        if isinstance(body, basestring) or isinstance(body, unicode):
            self._body = body
        else:
            raise Exception('Message body must be string')
        self._delay = delay
        self._priority = priority

        self._id = id
        self._receipt = receipt
        self._md5 = md5

    @property
    def body(self):
        return self._body

    @property
    def id(self):
        return self._id

    @property
    def receipt(self):
        return self._receipt

    def get_dict(self):
        d = {'MessageBody': self._body}
        if self._delay:
            d['DelaySeconds'] = self._delay
        if self._priority:
            d['Priority'] = self._priority
        return d