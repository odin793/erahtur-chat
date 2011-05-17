#!/bin/bash

DIR=/home/odin/erahtur-chat/tornado-chat
NAME=tornado-chat
LOG=/home/odin/logs/$NAME.log

cd $DIR

function start {
    pid=$(ps ax | grep runtornado | grep -v grep | awk '{ print $1 }')
    if [ "$pid" ]; then
        echo $NAME is already running
        return
    fi
    echo starting $NAME
    nohup ./manage.py runtornado 78.46.32.206:19999 &
    echo done
}

function stop {
    pid=$(ps ax | grep runtornado | grep -v grep | awk '{ print $1 }')
    case "$pid" in
    
        "") 
            echo $NAME is already stopped
            return 
            ;;
            
        * ) 
            echo stopping $NAME
            kill $pid
            echo done
            ;;
    esac
}

case $1 in 
    
    start)
        start
        ;;
    
    stop)
        stop
        ;;
    
    restart)
        stop
        start
        ;;
    
    *)
        echo 'valid arguments are: start, stop, restart'
        ;;
esac
        