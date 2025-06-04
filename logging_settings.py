import sys

logging_config = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': '--> [%(levelname)-8s] - %(name)s:%(funcName)s - %(message)s'
        },
        'formatter_1': {
            'format': '--> %(message)s'
        }
    },
    'handlers': {
        'default': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'stdout': {
            'class': 'logging.StreamHandler',
            'formatter': 'formatter_1',
            'stream': sys.stdout
        },

    },
    'loggers': {
        'main': {
            'level': 'INFO',
            'handlers': ['stdout']
        },
        'my_app': {
            'level': 'INFO',
            'handlers': ['stdout']
        }

    },
    'root': {
        'formatter': 'INFO',
        'handlers': ['stdout']
    }
}