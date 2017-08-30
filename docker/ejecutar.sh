#!/bin/bash
sudo docker run -ti -d --name issues -v $(pwd)/src:/src -p 5015:5000 -p 5016:5001 -p 5017:5002 -p 5018:5003 --env-file $HOME/gitlab/fce/produccion/issues issues
sudo docker exec -t issues bash instalar.sh

