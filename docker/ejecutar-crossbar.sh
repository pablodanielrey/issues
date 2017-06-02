#!/bin/bash
docker pull crossbario/crossbar
docker run -it --name crossbar -p 9000:8080 crossbario/crossbar

