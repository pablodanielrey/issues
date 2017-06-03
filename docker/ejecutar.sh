#!/bin/bash
sudo docker run -ti --name $1 --rm --env-file environment $1 $2

