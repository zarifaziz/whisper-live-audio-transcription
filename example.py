from whispercpp import Whisper

w = Whisper('tiny')

result = w.transcribe("temp_audio.mp3")
text = w.extract_text(result)