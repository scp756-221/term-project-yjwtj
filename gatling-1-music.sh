#!/usr/bin/env bash
docker container run --rm \
  -v ${PWD}/gatling/results:/opt/gatling/results \
  -v ${PWD}/gatling:/opt/gatling/user-files \
  -v ${PWD}/gatling/target:/opt/gatling/target \
  -e CLUSTER_IP=`tools/getip.sh kubectl istio-system svc/istio-ingressgateway`\
  -e USERS=1 \
  -e SIM_NAME=ReadMusicSim \
  --label gatling \
  ghcr.io/t2wan/gatling:3.4.2 \
  -s proj756.ReadMusicSimkubectl create ns c756nsaws dynamodb list-tables