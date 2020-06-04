#! /bin/bash

source scripts/colors.sh

usage()
# Prints usage
{
    if [ "$1" == 1 ]; then
        echo -e "${RED}Usage: `basename $0` [ PROJECT_NAME ]${RESET}"
    else
        echo "Usage: `basename $0` [ PROJECT_NAME ]"
    fi
    exit $1
}

py_lib_check()
# Checks if lib is installed
{
    pip list | grep -F $1 > /dev/null \
    || \
    (echo -e "${RED}No ${1} util!${RESET} \nInstall with:\n\tpip3 install ${1}" && exit 1)
}

help()
# Print help if running with "-h"
{
    if [ "$1" == "-h" ]; then
        usage 0
    fi
}

check_project_name()
# Checks if project name passed
{
    [ "$#" -eq 1 ] || usage 1
}

check_input()
# Checks input
{
    help "$@"
    check_project_name "$@"
}

warning()
{
    echo -e "${YELLOW}$@${RESET}"
}

success()
{
    echo -e "${GREEN}$@${RESET}"
}

error()
{
    echo -e "${RED}$@${RESET}"
}

starting()
{
    warning "Starting $@"
}

testing()
{
    warning "Testing using $@"
}

building()
{
    warning "Building using $@"
}

ok()
{
    success "$@ finished successfully"
    exit 0
}

fail()
{
    error "$@ failed"
    exit 1
}

echobreak()
{
    echo
    # warning "////////// $@ \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"
    warning "<<<<<<<<<< $@ >>>>>>>>>>"
    echo
}