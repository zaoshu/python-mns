#!/usr/bin/env python
# coding: utf-8
__author__ = 'wzy'
__date__ = '2015-07-03 20:02'


from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest
from tornado.httputil import HTTPHeaders
import base64
import time
import hmac
import hashlib


class Client(object):

    def __init__(self, host, access_id, access_key, version='2015-06-06'):
        self._host = host
        self._access_id = access_id
        self._access_key = access_key
        self._version = version

    def get_signature(self, method, headers, uri):
        mqs_headers = filter(lambda k: k.startswith('X-Mns-'), headers.keys())
        mqs_headers.sort()

        data = []
        data.append(method)
        data.append(headers.get('Content-MD5'))
        data.append(headers.get('Content-Type'))
        data.append(headers.get('Date'))
        data.extend('%s:%s' % (k.lower(), headers[k]) for k in mqs_headers)
        data.append(uri)

        h = hmac.new(self._access_key, '\n'.join(data), hashlib.sha1)
        signature = base64.b64encode(h.digest())
        return "MNS %s:%s" % (self._access_id, signature)

    def build_request(self, method, url, body):
        body_length = 0
        if body:
            body_length = len(body)
        headers = HTTPHeaders({
            'Connection': 'Keep-Alive',
            'Content-MD5': '',
            'Content-Type': 'text/xml;charset=UTF-8',
            'Date': time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime()),
            'Host': self._host,
            'x-mns-version': self._version,
            'Content-Length': str(body_length)
        })
        headers.add('Authorization', self.get_signature(method, headers, url))
        return HTTPRequest(
            'http://%s%s' % (self._host, url),
            method=method, headers=headers, body=body
        )

    @gen.coroutine
    def send_request(self, method, url, body=None):
        req = self.build_request(method, url, body)
        resp = yield AsyncHTTPClient().fetch(req)
        raise gen.Return(resp)
