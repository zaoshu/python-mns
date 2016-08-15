#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wzy'
__date__ = '2015/07/14'

from models import ModelAccesser
from base.RedisBase import RedisBase


class Behavior(ModelAccesser, RedisBase):

    @staticmethod
    def now_time():
        from time import time
        return int(time() * 1000)
