#!/bin/sh
sudo nvidia-docker run -it -p 8888:8888 -v $(pwd)/workspace:/notebook -P gym
