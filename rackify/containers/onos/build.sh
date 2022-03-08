#!/bin/bash

docker build -t kianjones9/onos:latest .
docker push kianjones9/onos:latest
docker run -t -d --network host --name onos kianjones9/onos