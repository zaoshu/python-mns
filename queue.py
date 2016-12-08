import logging
import json
import time
import threading
from . import config
from .mns.mns_client import MNSClient
from .mns.queue import Queue, QueueMeta, Message
from .mns.mns_exception import MNSExceptionBase

_null_logger = logging.getLogger('aliyun-mns')
_null_logger.setLevel(logging.ERROR)

def get_queue(name):
    client = MNSClient(
        config.MNS_HOST,
        config.MNS_ACCESS_ID,
        config.MNS_ACCESS_KEY,
        logger=_null_logger,
    )
    q = Queue(name, client)
    q.set_encoding(False)
    return q


def create_queue(queue):
    try:
        meta = QueueMeta()
        meta.set_maximum_message_size(65536)
        meta.set_message_retention_period(345600)
        queue.create(QueueMeta())
        logging.info('create queue succeed, name: %s', queue.queue_name)
    except MNSExceptionBase as e:
        if e.type == 'QueueAlreadyExist':
            logging.info('queue already exist, name: %s', queue.queue_name)
        else:
            raise


def loop_queue(queue, func):
    if queue is None:
        raise Exception('queue must not be None')
    if not callable(func):
        raise Exception('func must be callable')

    logging.info('start to listen on queue %s', queue.queue_name)
    while True:
        try:
            msg = queue.receive_message(config.MNS_POLLING_WAIT_SECONDS)
            logging.info('received message on [%s]: %s', queue.queue_name,
                         msg.message_body)
            try:
                data = json.loads(msg.message_body)
                try:
                    func(queue.queue_name, data)
                    # message handled, delete it
                    delete_message(queue, msg)
                except Exception as e:
                    logging.error(
                        'failed to handle message on [%s], data %s, error %s',
                        queue.queue_name, msg.message_body, e,
                    )
                    # do not delete this message
            except Exception as e:
                logging.error(
                    'can not parse message on [%s], data incorrect, %s, error %s, delete this message',
                    queue.queue_name, msg.message_body, e,
                )
                delete_message(queue, msg)
        except MNSExceptionBase as e:
            if e.type == "QueueNotExist":
                create_queue(queue)
            elif e.type == "MessageNotExist":
                pass
            else:
                logging.error(
                    'error in loop queue [%s], %s, restart loop 5 seconds later',
                    queue.queue_name, e,
                )
                time.sleep(5)


def send_message(queue, data, delay=0):
    msg = Message(json.dumps(data))
    msg.set_delayseconds(delay)

    for i in range(0, 3):
        try:
            queue.send_message(msg)
            return
        except MNSExceptionBase as e:
            if e.type == "QueueNotExist":
                create_queue(queue)
                continue
            else:
                raise


def delete_message(queue, msg):
    try:
        queue.delete_message(msg.receipt_handle)
    except MNSExceptionBase as e:
        if e.type == "QueueNotExist":
            logging.info('delete message failed, queue %s not exist',
                         queue.queue_name)
        elif e.type == "MessageNotExist":
            logging.info(
                'delete message failed, queue %s receipt handle %s invalid',
                queue.queue_name, msg.receipt_handle)
        else:
            raise

def start_background_loop(queue, func):
    if queue is None:
        raise Exception('queue must not be None')
    if not callable(func):
        raise Exception('func must be callable')

    loopper = threading.Thread(target=loop_queue, args=(queue, func))
    loopper.daemon = True
    loopper.start()
    return loopper
