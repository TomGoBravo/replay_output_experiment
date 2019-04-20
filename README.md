Replay Output Experiment
========================

Experiment using faust to replay the output topic


:License: MIT


Settings
--------

Settings are created based on [local-settings](https://github.com/drgarcia1986/simple-settings) package.

The only settings required if the `KAFKA_BOOTSTRAP_SERVER` environment variable.

```python
SIMPLE_SETTINGS = {
    'OVERRIDE_BY_ENV': True,
    'CONFIGURE_LOGGING': True,
    'REQUIRED_SETTINGS': ('KAFKA_BOOTSTRAP_SERVER',),
}

# The following variables can be ovirriden from ENV
KAFKA_BOOTSTRAP_SERVER = "kafka://kafka:9092"
```

The settings also include a basic logging configuration:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'replay_output_experiment': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
```

Basic Commands
--------------


* Start application: `make run-dev`. This command start both the *Page Views* and *Leader Election* applications
* Stop and remove containers: `make clean`
* List topics: `make list-topics`
* Send events to page_view topic/agent: `make send-page-view-event payload='{"id": "foo", "user": "bar"}'`
  



Docker
------

The `Dockerfile` is based on  `python:3.7-slim`. The most important here is that the [`entrypoint`]() will wait for `kafka` too be ready and after that execute the script [`run.sh`]()





Docker Compose
--------------

`docker-compose.yaml` includes `zookeepeer`, `kafka` and `schema-registry` based on `confluent-inc`.
For more information you can go to [confluentinc](https://docs.confluent.io/current/installation/docker/docs/index.html) and see the docker compose example [here](https://github.com/confluentinc/cp-docker-images/blob/master/examples/cp-all-in-one/docker-compose.yml#L23-L48)

Useful ENVIRONMENT variables that you may change:

|Variable| description  | example |
|--------|--------------|---------|
| WORKER_PORT | Worker port | `6066` |
| KAFKA_BOOTSTRAP_SERVER | Kafka servers | `kafka://kafka:9092` |
| KAFKA_BOOSTRAP_SERVER_NAME | Kafka server name| `kafka` |
| KAFKA_BOOSTRAP_SERVER_PORT | Kafka server port | `9092` |
| SCHEMA_REGISTRY_SERVER | Schema registry server name | `schema-registry` |
| SCHEMA_REGISTRY_SERVER_PORT | Schema registry server port | `8081` |
| SCHEMA_REGISTRY_URL | Schema Registry Server url | `http://schema-registry:8081` |



Type checks
-----------

Running type checks with mypy:

```
mypy replay_output_experiment
```
