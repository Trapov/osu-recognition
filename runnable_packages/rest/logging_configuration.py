import logging

from logging import Handler
from typing import Callable

import logging, logging.config
from queue import deque, Queue
from logging.handlers import QueueListener

class BufferedQueueHandler(Handler):
    def __init__(self, dequeue: deque, level):
        super().__init__(level)
        self.__dequeue : deque = dequeue

    def emit(self, record) -> None:
        self.__dequeue.append(record)
    

def __default_logging_configure() -> dict:
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
            },
        },
        'handlers': {
        },
        'loggers': { 
        }
    }

def configure(logging_dict_config : dict = __default_logging_configure(), maxlen: int = 10) -> Callable:
    dequeue = deque(maxlen=maxlen)
    q = Queue()
    
    listener = QueueListener(q, BufferedQueueHandler(dequeue, 'INFO'))
    listener.start()
    
    logging_dict_config.setdefault('handlers', {}).setdefault('logtweeb', 
        {
            'level': 'DEBUG',
            'class': 'logging.handlers.QueueHandler',
            'queue': q
        }
    )

    root_logger_config = logging_dict_config.setdefault('loggers', {}).setdefault('', {})
    root_logger_config.setdefault('level', 'DEBUG')
    root_logger_config.setdefault('propogate', True)
    root_logger_config.setdefault('handlers', []).append('logtweeb')

    logging.config.dictConfig(logging_dict_config)

    return lambda : list(dequeue)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        },
    },
    'handlers': {
        'default': { 
            'level': 'DEBUG',
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout', 
        }
    },
    'loggers': { 
        '': {  # root logger
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        }
    }
}