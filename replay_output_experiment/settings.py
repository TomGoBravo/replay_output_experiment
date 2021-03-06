SIMPLE_SETTINGS = {
    "OVERRIDE_BY_ENV": True,
    "CONFIGURE_LOGGING": True,
    "REQUIRED_SETTINGS": ("KAFKA_BOOTSTRAP_SERVER",),
}

# The following variables can be ovirriden from ENV
KAFKA_BOOTSTRAP_SERVER = "kafka://kafka:9092"
# SCHEMA_REGISTRY_URL = "http://schema-registry:8081"

BALANCES_TOPIC = "faust_bank_v1_balances"
TRANSFERS_TOPIC = "faust_bank_v1_transfers"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": "%(asctime)s %(levelname)s %(name)s %(message)s"}
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default",
        }
    },
    "loggers": {  # fmt: off
        "replay_output_experiment": {
            "handlers": ["console"],
            "level": "INFO",
        }
    },
}
