import speech_recognition as sr
import threading
import os
from whispercpp import Whisper
import time
from pydub import AudioSegment

import queue

audio_queue = queue.Queue()

def initialize_whisper_model():
    """Initialize and return the Whisper model."""
    return Whisper('medium')

def save_audio_to_file(audio_data, filepath):
    """Save audio data from SpeechRecognition to a file in MP3 format."""
    audio_segment = AudioSegment(
        data=audio_data.get_wav_data(),
        sample_width=audio_data.sample_width,
        frame_rate=audio_data.sample_rate,
        channels=1
    )
    mp3_path = filepath.replace('.wav', '.mp3')
    audio_segment.export(mp3_path, format="mp3")

def transcribe_with_whisper(filename, model):
    """Transcribe an audio file using the Whisper model."""
    result = model.transcribe(filename)
    return model.extract_text(result)

def listen_and_transcribe(recognizer, microphone, model, audio_queue, buffer_time: int = 3):
    """Continuously capture and transcribe audio."""
    if not os.path.exists('data'):
        os.makedirs('data')

    with open('data/transcript.txt', 'a', encoding='utf-8') as transcript_file:
        while not stop_listening:
            with microphone as source:
                print("Listening...")
                audio = recognizer.listen(source, phrase_time_limit=buffer_time)
                audio_queue.put(audio)

            if not audio_queue.empty():
                audio_to_process = audio_queue.get()
                temp_filename = 'data/temp_audio.mp3'
                save_audio_to_file(audio_to_process, temp_filename)

                # Check if the file exists before proceeding
                while not os.path.exists(temp_filename):
                    time.sleep(0.1)

                transcription = transcribe_with_whisper(temp_filename, model)
                print(f"Transcription: {transcription}")

                transcript_file.write(' '.join(transcription) + '\n')
                transcript_file.flush()

                os.remove(temp_filename)

# Initialize Whisper model
whisper_model = initialize_whisper_model()

# Create recognizer and microphone instances
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Flag to control the listening state
stop_listening = False

# Start transcription in a separate thread
transcription_thread = threading.Thread(target=listen_and_transcribe, args=(recognizer, microphone, whisper_model, audio_queue))
transcription_thread.start()

# Main loop to keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Stopping transcription...")
    stop_listening = True
    transcription_thread.join()
