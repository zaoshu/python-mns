#coding=utf-8
# Copyright (C) 2015, Alibaba Cloud Computing

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

class RequestInfo:
    def __init__(self, request_id = None):
        """ Client传递的请求信息
            @note: 可传递属性
            :: request_id: 可将client端的request_id传到MNS服务器端，方便直接使用Client端request_id进行问题排查
        """
        self.request_id = request_id

class TopicHelper:

    @staticmethod
    def generate_queue_endpoint(region, accountid, queue_name):
        """ 根据参数构造QueueEndpoint
            @type region: string
            @param region: 队列所在的地域，例如杭州是: cn-hangzhou

            @type accountid: string
            @param region: 队列拥有者的账号ID

            @type queue_name: string
            @param queue_name: 队列名称
        """
        return "acs:mns:%s:%s:queues/%s" % (region, accountid, queue_name)

    @staticmethod
    def generate_mail_endpoint(mail_address):
        """ 根据参数构造MailEndpoint
            @type mail_address: string
            @param mail_address: 邮箱地址
        """
        return "mail:directmail:%s" % mail_address 
