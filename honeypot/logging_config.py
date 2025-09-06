import logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} [{levelname}] {name}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'systemout_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/SystemOut.log',
            'formatter': 'verbose',
        },
        'honeypot_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'logs/HoneyPot.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'filemon': {
            'handlers': ['systemout_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'honeypot': {
            'handlers': ['honeypot_file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}


