import os
import pprint
from . import event
from . import config

def on_test(e, data):
    print(e)
    pprint.pprint(data)

if __name__ == '__main__':
    config.MNS_HOST = os.getenv('MNS_HOST')
    config.MNS_ACCESS_ID = os.getenv('MNS_ACCESS_ID')
    config.MNS_ACCESS_KEY = os.getenv('MNS_ACCESS_KEY')

    event.on('test', on_test)
    event.forever()