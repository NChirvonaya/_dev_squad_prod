#! /bin/bash

#
# Building
#

source scripts/colors.sh
. ./scripts/utils.sh

TEST_FLAKE8=./scripts/test_flake8.sh
TEST_MYPY=./scripts/test_mypy.sh
TEST_PYLINT=./scripts/test_pylint.sh

TEST_PYTEST=./scripts/test_pytest.sh

testing all

check_input "$@"

PROJECT_NAME=$1

echobreak LINTING TESTS

bash $TEST_FLAKE8 $PROJECT_NAME
echo
bash $TEST_MYPY $PROJECT_NAME
echo
bash $TEST_PYLINT $PROJECT_NAME

echobreak UNIT TESTS

bash $TEST_PYTEST .