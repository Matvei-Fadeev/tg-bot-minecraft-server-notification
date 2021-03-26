#!/bin/bash

case "$1" in
    'start' | 'stop' | 'restart' | 'status')
        bash tg-bot-users-register.sh $1
		bash tg-bot-broadcast.sh $1				
        ;;
    *)
        echo
        echo "Usage: $0 { start | stop | restart | status }"
        echo
        exit 1
        ;;
esac

exit 0