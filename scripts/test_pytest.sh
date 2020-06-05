#! /bin/bash

#
# Testing using pytest
#

source scripts/colors.sh
. ./scripts/utils.sh

PREFIX="python3 -m"
TESTNAME=pytest
FLAG_NOCAPTURE=-s
FLAG_VERBOSE=-v
FLAG_COVERAGE=--cov
FLAG_COVERAGE_CONFIG=--cov-config=.coveragerc
FLAG_PROFILE=--profile-svg

testing $TESTNAME

check_input "$@"
py_lib_check $TESTNAME
py_lib_check $TESTNAME-cov
py_lib_check $TESTNAME-sugar

PROJECT_NAME=$1

FLAG_COVERAGE_FULL="${FLAG_COVERAGE}=app"

FULLCOMMAND="${PREFIX} ${TESTNAME} ${FLAG_NOCAPTURE} ${FLAG_VERBOSE} ${FLAG_COVERAGE_FULL} ${FLAG_PROFILE} tests/"

            # $FLAG_COVERAGE_CONFIG \

# echo "WHY"
echo -e "${FULLCOMMAND}"

$FULLCOMMAND && ok $TESTNAME || fail $TESTNAME
# coverage html -d docs/ && exit 0 || exit 1W