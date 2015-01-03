# VG Media Services

This is what we use to generate the playlist.json and the hashed files sent to the media server at http://media.nexisonline.net.  Jenkins CI does our builds automatically, thus all the references to Jenkins.

This should be in a secret location so nerds don't leech it.  /vg/ uses a privately-hosted GitLab instance for version control.

# Cloning the Repository

This is simple:
```
$ git clone GIT_CLONE_URI jukebox
# For getyoutube, easytag:
$ sudo apt-get install -y dl-youtube easytag
```
Be aware that cloning can take a long time if you are doing so from an active repo, as there can about 2GB of songs in git.

If you want to actually perform conversions on your box for testing purposes (or to set up Jenkins):

1. Create a (K)ubuntu VirtualBox, or get on a PC with Debian or Ubuntu.
2. ```apt-get install -y sox libsox-fmt-all libav-tools python-pip```
3. ```pip install pyyaml mutagen```
4. Edit jenkins-deploy.sh to upload files to your media server.

# Adding New Media

## From Youtube/LiveLeak/Vimeo etc

```bash
$ ./getyoutube PLAYLISTNAME VideoURL [...]
```

Remember to fix the tags of the file with easytag.

## Directly

Dump into ```source/playlist/``` and edit the tags with easytag.

# New playlist

1. Add your playlist to the ```playlists``` at the top of convert.py.  (You may also need to adjust config.yml if you want to transclude files between playlists)
2. Add the media to the appropriate ```source/``` directory.
3. Update the SS13-media playlists.json
4. Add to your jukebox's playlists list.
5. Run convert.py and deploy.

Boom, done.