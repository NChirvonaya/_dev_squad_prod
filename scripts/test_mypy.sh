#! /bin/bash

#
# Static analysis using mypy
#

source scripts/colors.sh
. ./scripts/utils.sh

TESTNAME=mypy

testing $TESTNAME

check_input "$@"
py_lib_check $TESTNAME

PROJECT_NAME=$1

$TESTNAME --ignore-missing-imports $PROJECT_NAME && ok $TESTNAME || fail $TESTNAME