#!/usr/bin/env python
# coding: utf-8
__author__ = 'wzy'
__date__ = '2015-07-29 13:26'


from default import Default

from push import default_push_client
from message import send
from loop import MQLoop

def set_debug(debug=True):
    Default.debug = debug
