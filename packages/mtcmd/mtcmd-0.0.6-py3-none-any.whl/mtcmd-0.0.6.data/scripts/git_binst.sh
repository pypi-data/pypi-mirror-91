#!/bin/bash

if git rev-parse --git-dir > /dev/null 2>&1; then
    GIT_REPO_PATH=`git rev-parse --show-toplevel`
    CURR_PATH=$(pwd)
    echo "===== Building the Python package residing at ${GIT_REPO_PATH} ====="
    cd ${GIT_REPO_PATH}
    ./setup.py bdist_wheel
    echo "===== Installing the Python package, may need sudo privilege ====="
    WHEEL_FILE=`ls -t1 dist | head -n 1`
    PACKAGE_NAME=`echo "${WHEEL_FILE}" | cut -d'-' -f1`
    echo "Package name: ${PACKAGE_NAME}"
    echo "Wheel to install: ${WHEEL_FILE}"
    sudo pip3 uninstall -y ${PACKAGE_NAME}
    sudo pip3 install --extra-index https://nexus.winnow.tech/repository/ml-py-repo/simple/ --upgrade dist/${WHEEL_FILE}
    cd ${CURR_PATH}
else
    echo "This is not a git repo. No installation has been performed."
fi
