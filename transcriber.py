"""Step 1: Audio -> Text using OpenAI's Whisper model (via faster-whisper)."""
from faster_whisper import WhisperModel

_model = None


def load_model(size="base"):
    """Load the Whisper model once and reuse it (downloads on first run)."""
    global _model
    if _model is None:
        # int8 on CPU = works on any normal laptop, no GPU needed
        _model = WhisperModel(size, device="cpu", compute_type="int8")
    return _model


def transcribe(audio_path):
    """Convert an audio file (mp3, wav, m4a, ogg, flac...) into text."""
    model = load_model()
    segments, info = model.transcribe(audio_path, beam_size=5)
    text = " ".join(seg.text.strip() for seg in segments)
    return text.strip(), info.language
