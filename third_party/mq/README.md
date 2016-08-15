# MQ

## DEPS file config

`'xxxx/third_party/mq': 'git@bitbucket.org:kuaikuaiyu/MQ.git@master'`

## Push Message

```python
import mq
from tornado import gen

@gen.coroutine
def Test():
    mq.set_debug(True)
    client = mq.default_push_client()
    
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
```
