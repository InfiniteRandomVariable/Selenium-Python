echo 'command1 --foo=bar' | batch      
echo 'command2' | batch
at -q b -l              # on many OSes, a slightly shorter synonym is: atq -q b
#at -q b -r 1234         # Unschedule a pending task (atq gives the task ID)
