# import subprocess

# subprocess.call(['ffmpeg', '-i', 'Audio.mp3', 'converted_to_wav_file.wav'])
# print(value)

# subprocess.call(['ffmpeg', '-i', 'test.ogg', '-c:a', 'libvorbis', '-ab', '32k', '-ar', '22050', 'test2.ogg'])

import tempfile
from pydub import AudioSegment
from urllib.request import urlopen

data = urlopen('https://storage.googleapis.com/kin-project-352614-kinmusic-storage/Media_Files/Tracks_Audio_Files/7-Yena%20Zema-2022-10-04/2022-10-04/Balageru_4_786758307.mp3').read()
f = tempfile.NamedTemporaryFile(delete=False)
f.write(data)
AudioSegment.from_mp3(f.name).export('result.ogg', format='ogg')
f.close()

# # subprocess.call(['ffmpeg', '-i', self.track_audioFile, 'audio_test.wav'])
# data = playsound(self.track_audioFile)
# # urlopen('https://storage.googleapis.com/kin-project-352614-kinmusic-storage/Media_Files/Tracks_Audio_Files/7-Yena%20Zema-2022-10-04/2022-10-04/Balageru_4_786758307.mp3').read()
# f = tempfile.NamedTemporaryFile(delete=False)
# f.write(data)
# AudioSegment.from_mp3(f.name).export('result2.ogg', format='ogg')
# f.close()
# # self.track_audioFile = subprocess.call(['ffmpeg', '-i', file, '-c:a', 'libvorbis', '-ab', '32k', '-ar', '22050', f'{file_name}.ogg'])
# subprocess.call(['ffmpeg', '-i', f'{file}', '-c:a', 'libvorbis', '-ab', '64k', '-ar', '22050', f'{file_name}.ogg'])