#!/bin/bash
set -x

export SIMPLE_SETTINGS=replay_output_experiment.settings

# Install the application. The Dockerfile build installs everything in
# requirements.txt so this will only install the application and any
# dependencies added since the image was last built.
pip3 install -e /repo_root

./wait_for_services.sh

which -a replay_output_experiment

# Run the application with exec, replacing this shell script in the same
# process. Exec is used so dumb-init can easily forward signals to the
# application.
export DEVLOG=1
exec replay_output_experiment worker --web-port=$WORKER_PORT --loglevel=INFO
