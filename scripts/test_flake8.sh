#! /bin/bash

#
# Static analysis using flake8
#

source scripts/colors.sh
. ./scripts/utils.sh

TESTNAME=flake8

testing $TESTNAME

check_input "$@"
py_lib_check $TESTNAME

PROJECT_NAME=$1

$TESTNAME --max-line-length=140 $PROJECT_NAME && ok $TESTNAME || fail $TESTNAME