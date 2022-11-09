# import subprocess

# subprocess.call(['ffmpeg', '-i', 'Audio.mp3', 'Audio.ogg'])
# # subprocess.call(['ffmpeg', '-i', 'test.ogg', '-c:a', 'libvorbis', '-ab', '32k', '-ar', '22050', 'test2.ogg'])
# ffmpeg -i input.mp3 -c:a libvorbis -q:a 4 output.ogg
# subprocess.check_call("./script.ksh %s %s %s" % (arg1, str(arg2), arg3), shell=True)
# import subprocess
# import os

# filename = 'audio.wav'
# destination = r'./'
# subprocess.check_output(["ffmpeg", 
#     "-i", self.track_audioFile,
#     "-vn",
#     "-ar", "44100",
#     "-ac", "1",
#     "-b:a", "32k",
#     "-f", "wav",
#     os.path.join(destination, filename)
# ])
# import tempfile
# from pydub import AudioSegment
# from ffmpy3 import FFmpeg
# from urllib.request import urlopen
# import subprocess

# data = urlopen('http://127.0.0.1:8000/Media/Media_Files/Tracks_Audio_Files/1-A1_Singles-2022-11-09/2022-11-09/T2_Audio_K36Nr9G.mp3').read()
# f = tempfile.NamedTemporaryFile(delete=False)
# f.write(data)
# AudioSegment.from_mp3(f.name).export('result.ogg', format='ogg')
# f.close()
# FFmpeg(inputs={data: None}, outputs={'output.ogg': None}).run()
# subprocess.call(["ffmpeg", '-i', 'Audio.mp3', 'Audio.ogg'])



import requests

x = requests.get('http://0.0.0.0:8001/subscribedUsers/hailatFUI')
print(x.status_code)