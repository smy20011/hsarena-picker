#!/bin/bash
TOKEN=`pwgen 16`
echo "Notebook address: http://localhost:8888/?token=$TOKEN"

sudo nvidia-docker run -it --env TOKEN=$TOKEN -p 8888:8888 -v $(pwd)/workspace:/notebook -P gym
