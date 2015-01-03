#!/usr/bin/python
# recursively rename all files and directories in a given folder to lowercase

import sys, os, itertools, re, logging, subprocess
logging.basicConfig(format='%(asctime)s [%(levelname)-8s]: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

REG_WS = re.compile(r'[ \r\n\t]+')
	
def cmd(command, showoutput=False):
	logging.debug(u'>>> '+repr(command))
	output=''
	if showoutput:
		return subprocess.call(command,stderr=subprocess.STDOUT) == 0
	try:
		output = subprocess.check_output(command,stderr=subprocess.STDOUT)
		return True
	except Exception as e:
		logging.error(u"$ "+u' '.join(command))
		logging.error(output)
		logging.error(e)
		return False
	
def cleanFilename(s):
	s=s.replace('&','and')
	s = REG_WS.sub(s," ")
	nwfn = (i for i in s if i not in u"#?!")
	return ''.join(nwfn)

if len(sys.argv) < 2:
	print >> sys.stderr, "usage: lower PATH"
	sys.exit(2)
if not os.path.isdir(sys.argv[1]):
	print >> sys.stderr, sys.argv[1], "not a directory"
	sys.exit(1)

for root, dirs, files in os.walk(sys.argv[1]):
	for path in itertools.chain(files, dirs):
		old, new = os.path.join(root, path), os.path.join(root, cleanFilename(path))
		convert=False
		if old.endswith(".wav"):
			new=new.replace(".wav",".mp3")
			convert=True
		if old == new: 
			#print('  {} == {}'.format(old,new))
			continue
		#print('  {} != {}'.format(old,new))
		if not os.path.exists(new):
			if convert:
				cmd(['/usr/bin/avconv', '-i', old, new],showoutput=False)
			else:
				os.rename(old, new)
			logging.info("{} -> {}".format(old,new))
		if os.path.exists(old): os.remove(old)