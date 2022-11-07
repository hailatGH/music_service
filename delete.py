# from CaaS import audio_compression
# response = audio_compression("./Audio.mp3","compressed_Audio.mp3","token")

# from pydub import AudioSegment
# sound = AudioSegment.from_mp3("./Audio.mp3")
# sound.export("./c.mp3", format="mp3", bitrate="128k")

import tempfile
from pydub import AudioSegment
from urllib.request import urlopen

data = urlopen('https://storage.googleapis.com/kin-project-352614-kinmusic-storage-dev/Media_Files/Tracks_Audio_Files/4-Yene%20Zema-2022-11-04/2022-11-04/Balageru4_audio.mp3').read()
f = tempfile.NamedTemporaryFile(delete=False)
f.write(data)
AudioSegment.from_mp3(f.name).export('result.ogg', format='ogg')
f.close()