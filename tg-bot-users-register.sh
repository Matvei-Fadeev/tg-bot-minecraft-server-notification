#!/bin/bash

# The names of tmp-files 
APP_NAME="tg_bot_MSN"
NAME="tg_bot_users-register"

BASE="/tmp/$APP_NAME"
PID="$BASE/$NAME.pid"
LOG="$BASE/$NAME.log"
ERROR="$BASE/$NAME-error.log"


# The command which will be transffered to nohup
CMD='python3'
PY_MAIN='bot_users_register.py'
COMMAND="$CMD $PY_MAIN"


USR=user

source start-stop-module.sh