import mutagen,logging
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import EasyMP3
from mutagen.easymp4 import EasyMP4, EasyMP4Tags
from mutagen.oggflac import OggFLAC, OggFLACVComment

TagTypes={
	EasyMP3 : EasyID3,
	EasyMP4 : EasyMP4Tags,
	OggFLAC : OggFLACVComment,
	#mutagen.ogg.OggOpus : mutagen.ogg.OggOpusVComment,
}

class RyeBase(object):
	def __init__(self,filename,mutagenf):
		# mutagen => rye
		self.translation={}
		
		self.filename=filename
		
		#: The actual Mutagen tag handler.
		self.mutagen = mutagenf
		
		#: The tag values.
		self.tags={}
		
	def load(self):
		#print(self.__class__.__name__,self.filename,repr(self.translation))
		if self.mutagen is None:
			raise Exception('Mutagen unable to open {}'.format(self.filename))
		if self.mutagen.tags is None:
			self.mutagen.tags = TagTypes[self.mutagen.__class__]()
		for tag_name in self.mutagen.tags:
			tag_value = None
			if isinstance(tag_name,tuple):
				tag_name,tag_value = tag_name
			else:
				tag_value = self.mutagen.tags[tag_name]
			if isinstance(tag_value,(tuple,list)):
				tag_value=tag_value[0]
			if tag_value in (u'0',u''):
				continue
			tk = self.translateKey(tag_name)
			if tk is None:
				#logging.warn('Unhandled key {0}'.format(repr(tag_name)))
				continue
			self.tags[tk]=tag_value
			#logging.info(' {0} = {1}'.format(tk,repr(tag_value)))
			
	def getLength(self):
		return self.mutagen.info.length
		
	def translateKey(self,key):
		return self.translation.get(key,None)
	
	def detranslateKey(self,key):
		for k,v in self.translation.items():
			if v == key:
				return k
		return None
		
	def __getitem__(self,key):
		return self.tags[key]
	
	def __setitem__(self,key,value):
		self.tags[key]=value
	
	def __contains__(self,data):
		return data in self.tags
	
	def save(self):
		if self.mutagen.tags is None:
			self.mutagen.tags = self.mutagen.__class__._Tags()
			#print(repr(self.mutagen.tags))
		for tag_name in self.tags:
			mutatag=self.detranslateKey(tag_name)
			self.mutagen.tags[tag_name]=[self.tags[tag_name]]
		#print(repr(self.mutagen.tags))
		self.mutagen.save()
	
class RyeGeneric(RyeBase):
	
	def __init__(self,filename):
		RyeBase.__init__(self,filename,mutagen.File(filename, easy=True))
		self.translation={
			'artist': 'artist',
			'album':'album',
			'title':'title',
			'albumartist':'albumartist'
		}
		self.load()
		