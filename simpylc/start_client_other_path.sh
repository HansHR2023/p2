#!/usr/bin/env bash

export PYTHONPATH=simulations/car
export LIBGL_ALLOW_SOFTWARE=1

(cd simulations/car/control_client/; python better_than_tesla.py)
