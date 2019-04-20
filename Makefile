
service=replay_output_experiment
worker=replay_output_experiment.app
partitions=4

bash:
	docker-compose run --user=$(shell id -u) ${service} bash

# Build docker image
build:
	docker-compose build

restart:
	docker-compose restart ${service}

run:
	docker-compose up

logs:
	docker-compose logs

# Removes old containers, free's up some space
remove:
	# Try this if this fails: docker rm -f $(docker ps -a -q)
	docker-compose rm --force -v

stop:
	docker-compose stop

run-dev: build run

clean: stop remove

# Kafka related
list-topics:
	docker-compose exec kafka kafka-topics --list --zookeeper zookeeper:32181

# Faust commands related
send-page-view-event:
	docker-compose exec -e SIMPLE_SETTINGS=replay_output_experiment.settings ${service} faust -A ${worker} send page_views '${payload}'
