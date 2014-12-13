#!/bin/sh
{ sleep 5; echo waking up after 5 seconds; } &
{ sleep 1; echo waking up after 1 second; } &
wait
echo all jobs are done!
