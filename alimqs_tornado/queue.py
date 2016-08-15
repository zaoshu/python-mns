#!/usr/bin/env python
# coding: utf-8
__author__ = 'wzy'
__date__ = '2015-07-03 19:41'


import re
import logging
from tornado import gen
from tornado.httpclient import HTTPError
from client import Client
from message import Message

from collections import defaultdict
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class Queue(object):
    """
    API doc: http://docs.aliyun.com/?spm=5176.7393424.9.4.6JiYLH#/pub/mqs/api_reference/api_spec&message_operation
    see main()
    """

    _NAME_PATTERN = re.compile(r'^[a-zA-Z][a-zA-Z0-9\-]{0,255}$')

    def __init__(self, name, client):
        """

        :param name: queue name
        :param client: mqs client
        """
        if self._NAME_PATTERN.match(name):
            self._name = name
        else:
            raise Exception('queue name illegal')

        if client is None:
            raise Exception('client must not be None')
        if not isinstance(client, Client):
            raise Exception('client must be instance of Client')
        self._client = client

    @gen.coroutine
    def create(self,
               DelaySeconds=None,
               MaximumMessageSize=None,
               MessageRetentionPeriod=None,
               VisibilityTimeout=None,
               PollingWaitSeconds=None):
        """

        :param DelaySeconds: 发送到该Queue的所有消息默认将以DelaySeconds参数指定的
            秒数延后可被消费，单位为秒，0-604800秒（7天）范围内某个整数值，默认值为0
        :param MaximumMessageSize: 发送到该Queue的消息体的最大长度，单位为byte。
            1024(1K)-65536（64K）范围内的某个整数值，默认值为65536（64K）
        :param MessageRetentionPeriod: 消息在该Queue中最长的存活时间，从发送到该队列
            开始经过此参数指定的时间后，不论消息是否被取出过都将被删除，单位为秒。
            60 (1分钟)-1296000 (15 天)范围内某个整数值，默认值345600 (4 天)
        :param VisibilityTimeout: 消息从该Queue中取出后从Active状态变成
            Inactive状态后的持续时间，单位为秒。
            1-43200(12小时)范围内的某个值整数值，默认为30（秒）
        :param PollingWaitSeconds: 当Queue消息量为空时，针对该Queue的ReceiveMessage
            请求最长的等待时间，单位为秒。0-30秒范围内的某个整数值，默认为0（秒）
        """
        attributes = {}
        if DelaySeconds:
            attributes['DelaySeconds'] = DelaySeconds
        if MaximumMessageSize:
            attributes['MaximumMessageSize'] = MaximumMessageSize
        if MessageRetentionPeriod:
            attributes['MessageRetentionPeriod'] = MessageRetentionPeriod
        if VisibilityTimeout:
            attributes['VisibilityTimeout'] = VisibilityTimeout
        if PollingWaitSeconds:
            attributes['PollingWaitSeconds'] = PollingWaitSeconds

        logging.info('create queue %s' % self._name)
        yield self._client.send_request(
            'PUT', '/queues/' + self._name,
            self.encode_body('Queue', attributes)
        )

    @gen.coroutine
    def delete(self):
        yield self._client.send_request('DELETE', '/queues/' + self._name)

    @gen.coroutine
    def send_message(self, msg):
        """ send message to queue

        :param msg: Message
        """
        yield self._client.send_request(
            'POST', '/queues/%s/messages' % self._name,
            self.encode_body('Message', msg.get_dict())
        )

    @gen.coroutine
    def receive_message(self, waitseconds=3):
        """ receive message from queue

        :param waitseconds: see PollingWaitSeconds in __init__, this should be
            little than socket timeout
        """
        try:
            resp = yield self._client.send_request(
                'GET', '/queues/%s/messages?waitseconds=%d' % (self._name, waitseconds)
            )
        except HTTPError as e:
            if e.code == 404:
                # no message in queue or other error
                # treat it as no message, because I can't get error code in resp
                raise gen.Return(None)
            else:
                raise

        data = self.decode_body(resp.body)['Message']
        raise gen.Return(Message(
            data['MessageBody'],
            id=data['MessageId'],
            receipt=data['ReceiptHandle'],
            md5=data['MessageBodyMD5']
        ))

    @gen.coroutine
    def delete_message(self, msg):
        """ delete message from queue

        :param msg: Message
        """
        yield self._client.send_request(
            'DELETE', '/queues/%s/messages?ReceiptHandle=%s' % (self._name, msg.receipt)
        )

    @staticmethod
    def encode_body(root, body):
        root = ET.Element(root, {'xmlns': "http://mqs.aliyuncs.com/doc/v1/"})
        for k, v in body.items():
            node = ET.SubElement(root, k)
            node.text = str(v)
        return ET.tostring(root, encoding='utf-8')

    @staticmethod
    def decode_body(body):
        t = ET.XML(body)
        return etree_to_dict(t)


def etree_to_dict(t):
    tag = t.tag.split('}', 1)[1]
    d = {tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.iteritems():
                dd[k].append(v)
        d = {tag: {k: v[0] if len(v) == 1 else v for k, v in dd.iteritems()}}
    if t.attrib:
        d[tag].update(('@' + k, v) for k, v in t.attrib.iteritems())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[tag]['#text'] = text
        else:
            d[tag] = text
    return d
