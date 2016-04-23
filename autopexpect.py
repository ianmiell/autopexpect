#!/usr/bin/env python
import pexpect
import sys
import string
import time
import os
import stat


def input_filter(c):
	global userbuf
	global start_time
	global elapsed_time
	if len(c) == 1:
		if ord(c) == 13:
			elapsed_time = time.time() - start_time
			start_time = time.time()
			sendcmd(userbuf,elapsed_time)
			userbuf = ''
		else:
			userbuf+=c
	else:
		pass
		#userbuf+=c
	if userbuf != '':
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
	s=regsub(s)
	cmd('child.expect_exact(r"""' + s + '""")')


def sendcmd(s,elapsed_time):
	s=regsub(s)
	cmd('time.sleep(' + str(elapsed_time) + ')')
	cmd('child.sendline(r"""' + s + '""")')


def regsub(s):
	s=s.replace('\\\\','\\\\\\\\')
	s=s.replace('\r','\\r')
	s=s.replace('"','\\"')
	s=s.replace('\\\[','\\\[')
	s=s.replace('\\\]','\\\]')
	return s


def cmd(s):
	global fd
	fd.write(s+'\n')


# globals
filename     = 'script.py'
lastkey      = ""
outputbuf    = ""
userbuf      = ""
start_time   = 0
elapsed_time = 0


# Script starts
fd = open(filename,'w')
os.chmod(filename,stat.S_IRWXU)
cmd('#!/usr/bin/env python')
cmd('# -*- coding: utf-8 -*-')
cmd('import pexpect')
cmd('import sys')
cmd('import os')
cmd('import time')
cmd("""child=pexpect.spawn('/bin/bash')""")
cmd("""child.logfile=sys.stdout""")


child = pexpect.spawn('/bin/bash')
start_time = time.time()
child.interact(input_filter=input_filter,output_filter=output_filter)
# Finish with a return.
sendcmd('',0)
child.close()
print '\r\nScript written to: ' + filename
print '\r\nRun it with: ./' + filename

