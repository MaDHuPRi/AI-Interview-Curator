import tempfile
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
model = WhisperModel("base", device="cpu", compute_type="int8")

def record_audio(duration=30):
    """
    Records audio from mic and saves to WAV.
    """
    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype=np.int16
    )
    sd.wait()

    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    write(temp_wav.name, SAMPLE_RATE, audio)
    return temp_wav.name

def transcribe(wav_path: str) -> str:
    segments, _ = model.transcribe(wav_path)
    return " ".join(seg.text for seg in segments).strip()
