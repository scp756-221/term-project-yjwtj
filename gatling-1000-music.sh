#!/usr/bin/env bash
docker container run --detach --rm \
  -v ${PWD}/gatling/results:/opt/gatling/results \
  -v ${PWD}/gatling:/opt/gatling/user-files \
  -v ${PWD}/gatling/target:/opt/gatling/target \
  -e CLUSTER_IP=`tools/getip.sh kubectl istio-system svc/istio-ingressgateway`\
  -e USERS=1000 \
  -e SIM_NAME=ReadMusicSim \
  --label gatling \
  ghcr.io/t2wan/gatling:3.4.2 \
  -s proj756.ReadMusicSim
