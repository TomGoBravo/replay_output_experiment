#!/bin/bash
set -x

export SIMPLE_SETTINGS=replay_output_experiment.settings

replay_output_experiment worker --web-port=$WORKER_PORT