import mutagen
from .ryebase import RyeBase

class RyeVorbis(RyeBase):
	def __init__(self,filename):
		RyeBase.__init__(self,filename,mutagen.File(filename))
		
		self.translation={
			u'ALBUM'       : 'album',
			u'TITLE'       : 'title',
			u'ARTIST'      : 'artist',
			u'ALBUMARTIST' : 'albumartist'
		}
		
		self.load()