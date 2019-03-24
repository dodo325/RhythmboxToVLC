import xml.etree.ElementTree as ET
import os
from  urllib.parse import unquote
import xspf
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH

def addTrack(location, playlist):
    location_r = unquote(location.replace('file://', ''))
    try:
        
        mp3 = MP3File(location_r)
        tags = mp3.get_tags()
        tr = xspf.Track()
        tr.location = location

        if 'song' in tags['ID3TagV2'].keys():
            tr.title = tags['ID3TagV2']['song']
        if 'artist' in tags['ID3TagV2'].keys():
            tr.creator = tags['ID3TagV2']['artist']
        if 'album' in tags['ID3TagV2'].keys():
            tr.album = tags['ID3TagV2']['album']
        playlist.add_track(tr)
    except Exception as e:
        print('FileNotFoundError: ', location_r)
    
    return playlist





def main():
    print("Parsing rhythmbox playlists file")
    tree = ET.parse('/home/dodo/.local/share/rhythmbox/playlists.xml')
    root = tree.getroot()
    playlists = dict()
    
    print("Getting playlists from file")
    for child in root:
        if child.attrib['type'] == 'static':
            playlists[child.attrib['name']] = child

    print('Converte to ".xspf"')
    xspf_playlists = dict()
    for title, playlist in playlists.items():
        x = xspf.Xspf()
        x.title = title

        print("* playlist: ", title)

        for location in playlist:
            x = addTrack(location.text, x)
        xspf_playlists[title] = x
    
    if not os.path.exists('out'):
        os.makedirs('out')
        print("Created 'out' dirrectory")

    print("Saving in out/ converted lpaylisns")
    for tltie, playlist in xspf_playlists.items():
        file = open('out/'+tltie+'.xspf', 'wb')
        file.write(playlist.toXml().replace(b'\x00',b''))
        file.close()
if __name__ == "__main__":
    main()
