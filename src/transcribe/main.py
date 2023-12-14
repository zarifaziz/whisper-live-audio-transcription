import sounddevice as sd
import wavio as wv
import whisper
import multiprocessing
import os
from loguru import logger

from .settings import settings


def record():
    """Record audio from the microphone and save it as a WAV file."""
    freq = 44100
    duration = 5

    logger.info("Recording")

    while True:
        # Start recorder with the given values of duration and sample frequency
        # PTL Note: I had to change the channels value in the original code to fix a bug
        recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)

        # Record audio for the given number of seconds
        sd.wait()

        # Convert the NumPy array to audio file
        wv.write(settings.audio_file, recording, freq, sampwidth=2)


def transcribe():
    """Transcribe audio file to text using the Whisper model."""

    model = whisper.load_model("base")
    last_transcription = None

    while True:
        audio = whisper.load_audio(settings.audio_file)
        audio = whisper.pad_or_trim(audio)

        logger.info("Transcribing audio")
        mel = whisper.log_mel_spectrogram(audio).to(model.device)
        options = whisper.DecodingOptions(language="en", fp16=False)
        result = whisper.decode(model, mel, options)
        if result.text != "." and result.text != last_transcription:
            logger.info(result.text)
            with open(settings.transcript_file, "a", encoding="utf-8") as file:
                file.write(result.text + "\n")
            last_transcription = result.text


def loadfile(directory):
    """Load and return the content of all files in the given directory."""
    content = {}

    for file in os.scandir(directory):
        with open(file, encoding="utf-8") as f:
            filename = os.path.split(file)[1]
            contents = f.read()
            content[filename] = contents
    return content


if __name__ == "__main__":
    to_mic, to_whisper = multiprocessing.Pipe()

    mic = multiprocessing.Process(target=record)
    whisp = multiprocessing.Process(target=transcribe)

    mic.start()
    whisp.start()

    mic.join()
    whisp.join()
