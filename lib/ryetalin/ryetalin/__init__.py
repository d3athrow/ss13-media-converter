'''
RYETALIN - A standardization API for Mutagen.

MIT goes here.
'''
import mutagen, os
from .ryebase import RyeBase, RyeGeneric
from .ryevorbis import RyeVorbis

translators={
	None:  RyeGeneric, # Handles MP4 and MP3
	'ogg': RyeVorbis,  # Ogg Vorbis
}

def Open(filename):
	title, ext = os.path.splitext(os.path.basename(filename))
	ext=ext[1:]
	#print(ext)
	translatorType = translators[None]
	if ext in translators:
		translatorType = translators[ext]
	o = translatorType(filename)
	#print(repr(o))
	return o