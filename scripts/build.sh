#! /bin/bash

#
# Building
#

source scripts/colors.sh
. ./scripts/utils.sh

BUILDER=setup.py
FLAG_DISTRIBUTE=bdist

building $BUILDER

check_input "$@"

PROJECT_NAME=$1

python3 $BUILDER $FLAG_DISTRIBUTE