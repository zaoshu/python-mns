from .event import on
from .event import emit
from .event import forever

def init(host='', access_id='', access_key='', polling_wait_seconds=10):
    from . import config
    config.MNS_HOST = host
    config.MNS_ACCESS_ID = access_id
    config.MNS_ACCESS_KEY = access_key
    config.MNS_POLLING_WAIT_SECONDS = polling_wait_seconds
