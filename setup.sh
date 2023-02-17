#!/usr/bin/env bash

# This script is run only once, when the autograder zip gets uploaded.
# The idea is that it prepares the docker image, and when a student submits, that image gets cloned
# for the autograding to happen. 

apt update

cd /autograder

apt install -y jq
apt install -y texlive-full python3 python3-pip python3-dev

cp source/config.json ./

#########################################
##  LEAN AUTOGRADER SETUP
#########################################

# -sSf means curl should run silently, except for error messages, and HTTP error messages should get converted to command failure.
# sh -s just runs a shell in interactive mode (reading commands from stdin.) The extra arguments become
# positional parameters to the curled script: install elan with lean4 nightly as default toolchain
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y --default-toolchain leanprover/lean4:nightly-2023-01-16

LEAN_AUTOGRADER_REPO=$(jq -r '.autograder_repo' < config.json)
git clone "https://github.com/$LEAN_AUTOGRADER_REPO" "lean_ag_src"
cp config.json lean_ag_src
cd lean_ag_src

~/.elan/bin/lake exe cache get 
~/.elan/bin/lake build autograder AutograderTests 

cd /autograder
git clone "https://github.com/westluke/unified-autograder" "unified_ag_src"
