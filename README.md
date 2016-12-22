
##CALL.PY

*call.py* is a replacement for the xargs command.
```
usage: call.py [-h] [-n] [-1 | -m <count>] [-f <arg>] [--sub <string>]
               [--sep <string>] [-v]
               command ...

invoke a command against a list of items read from STDIN

positional arguments:
  command               command to invoke
  ...                   arguments for command

optional arguments:
  -h, --help            show this help message and exit
  -n, --no_exec         do not run command
  -1                    only one item per command invocation
  -m <count>, --max_args <count>
                        maximum number of items per command invocation,
                        default=500
  -f <arg>, --finalarg <arg>
                        added as last argument on the command line after all
                        items
  --sub <string>        subsitute string for item list, default="{}"
  --sep <string>        string use to seperate items when substituting into
                        argument, default=" "
  -v, --verbose         print command to stderr before execution
