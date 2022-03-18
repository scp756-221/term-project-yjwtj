#!/usr/bin/env bash
set -o nounset
set -o errexit
set -o xtrace
eid() {
    aws --output json ec2 describe-instances --filters Name=tag:mnemonic-name,Values="${1}" \
    | jq -r '.Reservations[].Instances[0] | .InstanceId'
    #| jq -r '.Reservations[].Instances[]| .InstanceId + " " + .InstanceType + " " + .State.Name + " " + .PublicIpAddress + " " + .Tags[0].Value'
}
eid ${1}
