import subprocess

subprocess.call(['ffmpeg', '-i', 'Audio.mp3', 'Audio.ogg'])
# subprocess.call(['ffmpeg', '-i', 'test.ogg', '-c:a', 'libvorbis', '-ab', '32k', '-ar', '22050', 'test2.ogg'])