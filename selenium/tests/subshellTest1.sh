#!/bin/bash
function back()
{
    sleep $1
    exit $2
}
back $1 $2 &
b=$!
if `wait $!`;then
    echo success
else
    echo failure
fi
