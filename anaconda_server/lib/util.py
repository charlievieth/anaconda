import logging
from logging import handlers
import os
import queue
import sys


def setup_logger(log_directory, level=logging.DEBUG, debug=False):
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    file_handler = handlers.RotatingFileHandler(
        filename=os.path.join(log_directory, 'anaconda_jsonserver.log'),
        maxBytes=1024 * 1024 * 20,
        backupCount=5,
        encoding='utf-8'
    )
    if debug:
        hdlrs = [
            file_handler,
            logging.StreamHandler(sys.stderr),
        ]
    else:
        hdlrs = [file_handler]
    logging.basicConfig(
        level=level,
        # TODO (CEV): use this format and name loggers
        # format='%(asctime)s %(name)s: %(levelname)s %(message)s',
        format='%(asctime)s: %(levelname)-8s: %(message)s',
        handlers=hdlrs,
    )


def setup_queue_logger(log_directory, level=logging.DEBUG, debug=False):
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    file_handler = handlers.RotatingFileHandler(
        filename=os.path.join(log_directory, 'anaconda_jsonserver.log'),
        maxBytes=1024 * 1024 * 20,
        backupCount=5,
        encoding='utf-8'
    )
    log_queue = queue.Queue(-1)
    if debug:
        stream_handler = logging.StreamHandler(sys.stderr)
        queue_listener = handlers.QueueListener(log_queue, file_handler,
                                                stream_handler)
    else:
        queue_listener = handlers.QueueListener(log_queue, file_handler)
    queue_handler = handlers.QueueHandler(log_queue)
    logging.basicConfig(
        level=level,
        # TODO (CEV): use this format and name loggers
        format='%(asctime)s %(name)s: %(levelname)s %(message)s',
        # format='%(asctime)s: %(levelname)-8s: %(message)s',
        handlers=[queue_handler],
    )
    queue_listener.start()
    return queue_listener
