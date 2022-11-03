from CaaS import audio_compression
response = audio_compression("./Audio.mp3","compressed_Audio.mp3","token")

# from pydub import AudioSegment
# sound = AudioSegment.from_mp3("./Audio.mp3")
# sound.export("./c.mp3", format="mp3", bitrate="128k")