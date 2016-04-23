#!/usr/bin/env python

import pexpect
import sys
import string

filename = 'script.py'

def input_filter(c):
	global userbuf
	if len(c) == 1:
		if ord(c) == 13:
			sendcmd(userbuf)
			userbuf = ''
		else:
			userbuf+=c
	else:
		userbuf+=c
	sys.stdout.write(c)
	return c

def output_filter(o):
	global outputbuf
	outputbuf+=o
	# Newline detected
	if userbuf=='' and outputbuf!='':
		outputbuf_list = outputbuf.split()
		for line in outputbuf_list:
			expcmd(line)
		outputbuf=''
	return o

def expcmd(s):
	cmd('child.expect_exact(r"""' + s + '""")')

def sendcmd(s):
	cmd('child.sendline(r"""' + s + '""")')

def cmd(s):
	global fd
	fd.write(s+'\n')


fd = open(filename,'w')
cmd('import pexpect')
cmd("""child=pexpect.spawn('/bin/bash')""")

# globals
lastkey = ""
outputbuf = ""
userbuf = ""

child = pexpect.spawn('/bin/bash')
child.interact(input_filter=input_filter,output_filter=output_filter)
child.close()
	
