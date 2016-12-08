import os
from . import emit
from . import config

if __name__ == '__main__':
    config.MNS_HOST = os.getenv('MNS_HOST')
    config.MNS_ACCESS_ID = os.getenv('MNS_ACCESS_ID')
    config.MNS_ACCESS_KEY = os.getenv('MNS_ACCESS_KEY')

    data = {
        'a': 1,
        'b': 2,
    }
    emit('test', data)