import logging
import threading
from queue import Queue

logger = logging.getLogger('main.{}'.format(__name__))
extra = {'signature': '---SIGNATURE-NOT-SET---'}


class BaseThreadClass:

    @staticmethod
    def create_thread_queue(func, thread_count=10, **kwargs):
        enclosure_queue = Queue()
        logger.debug('Initialising thread queue with thread count {}'.format(thread_count), extra=extra)
        for i in range(thread_count):
            thread = threading.Thread(target=func, args=(i, enclosure_queue), kwargs=kwargs)
            thread.setDaemon(True)
            thread.start()

        return enclosure_queue
