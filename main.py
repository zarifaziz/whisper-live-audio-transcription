import sounddevice as sd
import numpy as np
import threading
import queue
import tempfile
import os
from whispercpp import Whisper

class AudioRecorder:
    """Class to handle audio recording."""
    def __init__(self, sample_rate=16000, channels=1):
        """Initialize the audio recorder with given sample rate and channels."""
        self.sample_rate = sample_rate
        self.channels = channels
        self.audio_queue = queue.Queue()
        self.recording = threading.Event()

    def audio_callback(self, indata, frames, time, status):
        """Callback function for audio stream."""
        if self.recording.is_set():
            self.audio_queue.put(indata.copy())

    def start(self):
        """Start the audio recording and streaming."""
        self.stream = sd.InputStream(callback=self.audio_callback,
                                     channels=self.channels,
                                     samplerate=self.sample_rate)
        self.stream.start()
        self.recording.set()

    def stop(self):
        """Stop the audio recording and streaming."""
        self.recording.clear()
        self.stream.stop()
        self.stream.close()

class WhisperTranscriber(threading.Thread):
    """Class to transcribe audio using Whisper."""
    def __init__(self, audio_queue):
        """Initialize the transcriber with the audio queue."""
        super().__init__()
        self.audio_queue = audio_queue
        self.model = Whisper('tiny')
        self.transcribing = threading.Event()

    def run(self):
        """Run the transcription process."""
        self.transcribing.set()
        while self.transcribing.is_set():
            if not self.audio_queue.empty():
                audio_chunk = self.audio_queue.get()
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmpfile:
                    self.save_audio_to_file(audio_chunk, tmpfile.name)
                    transcript = self.transcribe_with_whisper(tmpfile.name)
                    print(f"Transcription: {transcript}")
                    os.remove(tmpfile.name)

    def stop(self):
        """Stop the transcription process."""
        self.transcribing.clear()

    def save_audio_to_file(self, audio_data, filename):
        """Save audio data to a file."""
        audio_data = np.concatenate(audio_data)
        sd.write(filename, audio_data, samplerate=16000)

    def transcribe_with_whisper(self, filename):
        """Transcribe audio from a file using Whisper."""
        result = self.model.transcribe(filename)
        return self.model.extract_text(result)

def main():
    """Main function to start the recorder and transcriber."""
    recorder = AudioRecorder()
    audio_queue = recorder.audio_queue

    transcriber = WhisperTranscriber(audio_queue)

    try:
        recorder.start()
        transcriber.start()

        while True:
            pass
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        recorder.stop()
        transcriber.stop()
        transcriber.join()

if __name__ == "__main__":
    main()
