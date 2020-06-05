#! /bin/bash

#
# Static analysis using pylint
#

source scripts/colors.sh
. ./scripts/utils.sh

TESTNAME=pylint
FAIL_UNDER=$TESTNAME-fail-under
FLAG_FAIL_UNDER=--fail_under
THRESHOLD=9.0
FLAG_RC="--rcfile .pylintrc"

testing $TESTNAME

check_input "$@"
py_lib_check $TESTNAME || exit 1
py_lib_check $FAIL_UNDER || exit 1

PROJECT_NAME=$1

$FAIL_UNDER $FLAG_RC $FLAG_FAIL_UNDER $THRESHOLD $PROJECT_NAME && ok $TESTNAME || fail $TESTNAME