#!/usr/bin/env bash
# Transfer the files to c756-exer

if [[ $# -ne 1 || ! -d ${1} ]]; then
  echo "Usage: ${0} PATH"
  echo "  Transfer files into c756-exer PATH directory."
  echo "  Where PATH is parent of `profiles`."
  exit 1
fi

set -o nounset
set -o errexit

dest=${1}
dp=${dest}/profiles

set -o xtrace
sed -e 's|^PROFILE=~/\.ec2\.mak|#PROFILE=~/\.ec2\.mak|' -e 's|^#PROFILE=profiles/ec2\.mak|PROFILE=profiles/ec2\.mak|' .aws-a   > ${dp}/aws-a
sed -e 's|^LOGD=\.|#LOGD=\.|'                           -e 's|^#LOGD=logs|LOGD=logs|'                                 .ec2.mak > ${dp}/ec2.mak
/bin/cp -f README.md ${dp}/README-aws.md
