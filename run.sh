#!/bin/bash -x

./listen.py &

cleanup() {
   killall listen.py haproxy
}

trap cleanup EXIT

while : ;
do
    inotifywait -e MODIFY ./minecraftHaProxy.conf
    killall haproxy
    haproxy -f  ./minecraftHaProxy.conf &
done
