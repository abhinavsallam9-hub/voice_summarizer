"""Step 2: Transcript -> Structured summary using a Generative AI model (Gemini)."""
import re
from collections import Counter

# ---- PROMPT DESIGN (document this in your report) ----
SUMMARY_PROMPT = """You are an expert note-taker. Below is a raw transcript of an audio
recording (a lecture, meeting, or study discussion). It may contain filler words,
repetitions and speech-recognition mistakes.

Write a clean, well-structured summary in English using exactly these sections:

## Overview
2-3 sentences describing what the recording is about.

## Key Points
5-8 bullet points with the most important ideas, in the order they appear.

## Important Details
Bullet points for any names, dates, numbers, definitions or formulas mentioned.
Write "None" if there are none.

## Action Items / Takeaways
Bullet points for tasks, deadlines or things to remember. Write "None" if there are none.

Rules: do not invent information that is not in the transcript; fix obvious
transcription errors; keep the language simple.

TRANSCRIPT:
\"\"\"{transcript}\"\"\"
"""


def summarize_with_gemini(transcript, api_key, model="gemini-2.5-flash"):
    from google import genai

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model, contents=SUMMARY_PROMPT.format(transcript=transcript)
    )
    return response.text


STOPWORDS = set("""a an the and or but if is are was were be been to of in on at for with
this that these those it its as by from so we you i he she they them our your his her
not no yes do does did have has had will would can could should just like um uh okay
also there here what which who when where how then than about into very really""".split())


def summarize_offline(transcript, n_points=6):
    """Backup summary (no internet / no API key): picks the most important sentences."""
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", transcript) if len(s.split()) > 4]
    if not sentences:
        return "## Key Points\n- " + transcript
    words = [w for w in re.findall(r"[a-z']+", transcript.lower()) if w not in STOPWORDS]
    freq = Counter(words)
    scored = [
        (sum(freq[w] for w in re.findall(r"[a-z']+", s.lower())) / len(s.split()), i, s)
        for i, s in enumerate(sentences)
    ]
    top = sorted(sorted(scored, reverse=True)[:n_points], key=lambda x: x[1])
    keywords = ", ".join(w for w, _ in freq.most_common(8))
    return (
        "## Key Points\n" + "\n".join(f"- {s}" for _, _, s in top)
        + f"\n\n## Keywords\n{keywords}"
    )


def summarize(transcript, api_key=None):
    """Use Gemini if an API key is given, otherwise fall back to the offline method."""
    if api_key:
        try:
            return summarize_with_gemini(transcript, api_key), "Gemini (Generative AI)"
        except Exception as e:
            return summarize_offline(transcript), f"Offline (Gemini failed: {e})"
    return summarize_offline(transcript), "Offline (extractive)"
