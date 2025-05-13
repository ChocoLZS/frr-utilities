from __future__ import absolute_import

import os

# =============================================================================
# BGP configuration.
# =============================================================================
BGP = {
    # AS number for this BGP instance.
    "local_as": 30,
    # 'local_port': 5555,
    # BGP Router ID.
    "router_id": "3.0.3.2",
    # Default local preference
    "local_pref": 100,
    # List of TCP listen host addresses.
    "bgp_server_hosts": ["0.0.0.0", "::"],
    # List of BGP neighbors.
    # The parameters for each neighbor are the same as the arguments of
    # BGPSpeaker.neighbor_add() method.
    "neighbors": [
        {
            "address": "10.23.32.1",
            "remote_as": 20,
            "enable_ipv6": True,
            "enable_ipv4": True,
            # "local_address": "3.0.3.2",
        },
        {
            "address": "10.32.33.2",
            "remote_as": 30,
            "enable_ipv6": True,
            "enable_ipv4": True,
            "is_next_hop_self": True,
            # "local_address": "3.0.3.2",
        },
    ],
    "routes": [
    ],
}


# =============================================================================
# SSH server configuration.
# =============================================================================
SSH = {
    "ssh_port": 22222,
    "ssh_host": "localhost",
    # 'ssh_host_key': '/etc/ssh_host_rsa_key',
    # 'ssh_username': 'ryu',
    # 'ssh_password': 'ryu',
}


# =============================================================================
# Logging configuration.
# =============================================================================
LOGGING = {
    # We use python logging package for logging.
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            + "[%(process)d %(thread)d] %(message)s"
        },
        "simple": {
            "format": "%(levelname)s %(asctime)s %(module)s %(lineno)s " + "%(message)s"
        },
        "stats": {"format": "%(message)s"},
    },
    "handlers": {
        # Outputs log to console.
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "console_stats": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "stats",
        },
        # Rotates log file when its size reaches 10MB.
        "log_file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(".", "bgpspeaker.log"),
            "maxBytes": "10000000",
            "formatter": "verbose",
        },
        "stats_file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(".", "statistics_bgps.log"),
            "maxBytes": "10000000",
            "formatter": "stats",
        },
    },
    # Fine-grained control of logging per instance.
    "loggers": {
        "bgpspeaker": {
            "handlers": ["console", "log_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "stats": {
            "handlers": ["stats_file", "console_stats"],
            "level": "INFO",
            "propagate": False,
            "formatter": "stats",
        },
    },
    # Root loggers.
    "root": {
        "handlers": ["console", "log_file"],
        "level": "DEBUG",
        "propagate": True,
    },
}
