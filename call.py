#! /usr/bin/env python3

__author__        = "James Ng"
__copyright__     = "Copyright 2016 James Ng"
__license__       = "GPL"
__version__       = "1.0"
__maintainer__    = "James Ng"
__email__         = "jng@slt.net"
__status__        = ""

import argparse
import os
import sys
import subprocess

# --- options parsing and management
pargs = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='invoke a command against a list of items read from STDIN')
pargs.add_argument('-n', '--no_exec', dest='noexec', action='count', help='do not run command')

# --- only one option is valid
xgroup = pargs.add_mutually_exclusive_group(required=False)
xgroup.add_argument('-1', dest='arg1', action='count', help='only one item per command invocation')
xgroup.add_argument('-m', '--max_args', metavar="<count>", dest='max_args', type=int, help='maximum number of items per command invocation, default=500', default=500)

# --- rest of options
pargs.add_argument('-f', '--finalarg', metavar="<arg>", dest='finalarg', help='added as last argument on the command line after all items')
pargs.add_argument('--sub', metavar="<string>", dest='sub', help='subsitute string for first item, default=\"{}\"')
pargs.add_argument('--sep', metavar="<string>", dest='sep', help='string use to seperate items when substituting into argument, default=\" \"', default=' ')
pargs.add_argument('-v', '--verbose', dest='verbose', action='count', help='print command to stderr before execution')

# --- command to execute
#pargs.add_argument('--cmd', dest='cmdcmd', metavar='cmd', help='command to invoke, this overrides the command argument')
pargs.add_argument(dest='cmd', metavar="command", help='command to invoke')
pargs.add_argument(dest='cmdargs', metavar="...", nargs=argparse.REMAINDER, help='arguments for command')

args = pargs.parse_args();

if args.arg1:
	args.max_args = 1
	
if args.max_args == None:
	args.max_args = 500

# at least one item per invocation
if args.max_args < 1:
	args.max_args = 1

if args.finalarg == None:
	args.finalarg = ""

if args.sub == None:
	args.sub = "{}"

# --- go through the arguments for the command and splice in the items
# --- doesn't necessarily make sense in all cases but...
def subarg(cmdargs, itemlist):
	ncmdargs = []
	for a in cmdargs:
		# substr found alone, replace with items list
		if a == args.sub:
			ncmdargs.extend(itemlist)
		elif not args.sub in a:
			ncmdargs.append(a)
		else:
			# ---
			# substr found as part of string (ie. destdir/{})
			# split the string, insert the items, stitch it back together.
			narg = []
			b = a.split(args.sub)
			if (b[0]):
				narg.append(b[0])
			b.pop(0)
			for c in b:
				narg.extend(itemlist)
				if c: 
					narg.append(c)
			ncmdargs.append(args.sep.join(narg))

			#---
			# ...probably can (and should be) replace with;
			#ncmdargs.append(a.replace(args.sub, args.sep.join(itemlist)))

	return(ncmdargs)

# --- do we need to do argument subsitution?
dosubarg = False
for a in args.cmdargs:
	if (args.sub in a):
		dosubarg = True
		break

def runcmd(itemlist):
	# --- do argument subsitution
	if dosubarg:
		cmdargs = subarg(args.cmdargs.copy(), itemlist)
	else:
		cmdargs = args.cmdargs + itemlist

	# --- tack on last argument
	if args.finalarg:
		command = [args.cmd] + cmdargs + [args.finalarg]
	else:
		command = [args.cmd] + cmdargs

	if args.verbose:
		print(" ".join(command), file=sys.stderr)
		#print(command, file=sys.stderr)

	if not args.noexec:
		subprocess.run(command)

try:
	itemlist = []
	count = 0
	for item in sys.stdin:
		count += 1
		item = item.rstrip(os.linesep)
		itemlist.append(item);

		# --- collect arguments up to max_args
		if count < args.max_args:
			continue

		# --- invoke command  with collected bunch of items
		runcmd(itemlist)

		# --- reset count for next bunch of items
		count = 0
		itemlist = []

	# --- run with final bunch of items
	if len(itemlist):
		runcmd(itemlist)

# --- catch errors from subprocess.run
except OSError as e:
	print("{}".format(str(e.strerror)), file=sys.stderr)
