#!/bin/bash
function back()
{
  sleep $1
  exit $2
}
back $1 $2 &
b=$!

wait $b

#echo success || echo failure
