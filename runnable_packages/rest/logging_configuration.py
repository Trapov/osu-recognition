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
        },
    },
    'loggers': { 
        '': {  # root logger
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}