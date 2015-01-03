
import glob, os, hashlib, logging, subprocess, shutil, sys, json, yaml, time

# Ryetalin is our shitty standardization library.
sys.path.append('lib/ryetalin')
import ryetalin

def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % \
        reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
            [(t*1000,),1000,60,60])

class TimeExecution(object):
    def __init__(self, label):
        self.start_time=None
        self.label = label
    
    def __enter__(self):
        self.start_time = TIME_SOURCE()
        return self
    
    def __exit__(self, type, value, traceback):
        logging.info('  Completed in {1}s - {0}'.format(self.label, secondsToStr(TIME_SOURCE() - self.start_time)))
        return False

# Try to clean up UTF8 (NEVER WORKS)
def removeNonAscii(s): 
	return u''.join(i for i in s if ord(i)<128)

# Remove ampersands, hashes, question marks, and exclamation marks.
def cleanFilename(s):
	s=s.replace(u'&',u'and')
	nwfn=(i for i in s if i not in u"#?!")
	return u''.join(nwfn)

def move(fromdir, todir, fromexts, toext, op, **op_args):
	for root, dirs, files in os.walk(fromdir):
		path = root.split(u'/')
		newroot=os.path.join(todir,root[len(fromdir)+1:])
		for file in files:
			fromfile=os.path.join(root,file)
			title, ext = os.path.splitext(os.path.basename(fromfile))
			if ext.strip(u'.') not in fromexts:
				#logging.warn(u'Skipping {} ({})'.format(fromfile, ext))
				continue
			if not os.path.isdir(newroot):
				os.makedirs(newroot)
			op(fromfile,newroot,op_args)
	
def check(wdir, exts, op, **kwargs):
	for root, dirs, files in os.walk(wdir):
		for file in files:
			fromfile=os.path.join(root,file)
			title, ext = os.path.splitext(os.path.basename(fromfile))
			if ext.strip(u'.') not in exts:
				#logging.warn(u'Skipping {} ({})'.format(fromfile, ext))
				continue
			op(fromfile, **kwargs)

# Copy the file's tags and convert to id3v2
def fix_tags(origf):
	orig = ryetalin.Open(origf)
	if orig is None:
		logging.critical(u'Unable to open {}!'.format(origf))
		sys.exit(1)
		
	# you can iterate over the tag names
	# they will be the same for all file types
	changed=[]
	numtags = 0
	
	if 'artist' not in orig:
		titleparts = orig['title'].split(u'-',1)
		if len(titleparts) >= 2:
			orig['artist']=titleparts[0].strip()
			orig['title']=titleparts[1].strip()
			changed += ['title','artist']
	#logging.info("{0}: {1} tags.".format(newf,numtags))
	warnings=[]
	if 'title' not in orig:
		warnings += ['title']
	if 'artist' not in orig and 'album' not in orig:
		warnings += ['artist OR album']
	if len(warnings) > 0:
		logging.warn(u'Missing tags in {}: {}'.format(origf,', '.join(warnings)))
	if len(changed) > 0:
		orig.save()
		logging.info('Updated tags in {}: {}'.format(origf,', '.join(changed)))


logging.basicConfig(format='%(asctime)s [%(levelname)-8s]: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

logging.info('Searching for mis-tagged items...')

check(sys.argv[1], ('m4a','wav','mp3','ogg','webm','oga'), fix_tags)