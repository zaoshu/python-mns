from .queue import create_queue
from .queue import get_queue
from .queue import send_message
from .queue import start_background_loop


def emit(queue_name, data, delay=0):
    """
    Emit data to queue *queue_name*

    :param queue_name: event name
    :param data: event data, type is dict
    :param delay: delay in seconds
    :return: None
    """
    send_message(get_queue(queue_name), data, delay)


def on(queue_name, func):
    """
    Listen on queue *queue_name*

    Example of func:
        def on_event(e, data):
            # e: queue name
            # data: event data, type is dict
            print(e)

    :param queue_name: event name
    :param func: event handle function
    :return: None
    """
    q = get_queue(queue_name)
    create_queue(q)
    start_background_loop(q, func)


def forever():
    import threading
    threading.Event().wait()
