# PS-5: AI-Based Audio-to-Text Summarization System

An application that takes an audio recording (lecture, meeting, study session),
converts the speech to text with **OpenAI's Whisper model**, and produces a clean,
structured **summary** using a **Generative AI model (Google Gemini)**.

---

## 1. How to run (Windows)

1. Double-click **`run.bat`**.
   - The first time, it installs the libraries (takes a few minutes).
   - The browser then opens at `http://localhost:8501`.
2. (Optional, for a better summary) Get a free API key from
   <https://aistudio.google.com/apikey> and paste it into the sidebar.
3. Upload an audio file (mp3 / wav / m4a / ogg / flac / webm) and click
   **Transcribe & Summarize**.

> Without an API key the app still works: it uses a simple offline method that
> picks out the most important sentences.

---

## 2. Project structure

| File | What it does |
|---|---|
| `app.py` | Web interface (Streamlit): upload audio and show the results |
| `transcriber.py` | **Step 1**: Audio → Text with the Whisper model |
| `summarizer.py` | **Step 2**: Text → Summary (Gemini prompt + offline backup) |
| `requirements.txt` | List of Python libraries |
| `run.bat` | One-click install + start |
| `samples/` | Sample audio used for testing |

---

## 3. Transcription and summarization workflow

```
 Audio file (mp3/wav/m4a)
        │
        ▼
 [Streamlit UI] ── user uploads file
        │
        ▼
 [Whisper "base" model]  (faster-whisper, runs locally on CPU)
   - decodes audio, resamples to 16 kHz
   - detects language automatically
   - converts speech → raw transcript
        │
        ▼
 [Generative AI – Gemini 2.5 Flash]  (structured prompt)
   - cleans filler words / transcription errors
   - produces Overview, Key Points, Details, Action Items
   (fallback: offline extractive summary if no key/internet)
        │
        ▼
 Summary + full transcript shown on screen, downloadable as .txt
```

**Technologies:** Python 3.12, Streamlit (UI), faster-whisper (an optimized
implementation of OpenAI Whisper), Google Gemini API (LLM summarization).
No model was trained from scratch; only pre-trained models and APIs are used.

### Model/API configuration
- Whisper model size: `base` (~140 MB, good speed/accuracy on a laptop CPU),
  `device="cpu"`, `compute_type="int8"`, `beam_size=5`.
  You can change `"base"` to `"small"` in `transcriber.py` for better accuracy (slower).
- LLM: `gemini-2.5-flash` via the `google-genai` SDK.

---

## 4. Prompt design

The prompt (in `summarizer.py`) was designed with these ideas:

1. **Role**: "You are an expert note-taker" sets the tone and quality.
2. **Context**: it tells the model the input is a *raw* transcript that may contain
   filler words and recognition mistakes, so it cleans them up.
3. **Fixed output structure**: four headings (Overview, Key Points, Important
   Details, Action Items), so every summary has the same well-structured format.
4. **Constraints**: "do not invent information" reduces hallucination;
   "keep the language simple" makes it easy to read; "None" is written for empty sections.
5. **Delimiters**: the transcript is wrapped in triple quotes so the model
   clearly separates instructions from data.

---

## 5. Sample input and output

**Input:** `samples/sample_lecture.wav` (a ~40 s lecture about machine learning)

**Whisper transcript (actual output):**
> Good morning everyone. Today we will learn about machine learning. Machine learning
> is a branch of artificial intelligence where computers learn patterns from data
> instead of being explicitly programmed. There are three main types. Supervised
> learning uses labeled data, for example predicting house prices. Unsupervised
> learning finds hidden groups in unlabelled data, like customer segmentation.
> Reinforcement learning trains an agent using rewards and penalties. Remember, your
> assignment on linear regression is due next Friday, the 31st of October.

Detected language: `en`

**Summary (offline method, actual output):**
```
## Key Points
- Today we will learn about machine learning.
- Machine learning is a branch of artificial intelligence where computers learn patterns from data instead of being explicitly programmed.
- Supervised learning uses labeled data, for example predicting house prices.
- Unsupervised learning finds hidden groups in unlabelled data, like customer segmentation.
- Reinforcement learning trains an agent using rewards and penalties.
- Remember, your assignment on linear regression is due next Friday, the 31st of October.
```

**Summary (Gemini):** run the app with your API key and paste the result here,
with a screenshot.

---

## 6. Limitations and future work
- Long recordings (1 hour or more) take several minutes on CPU.
- Accuracy drops with heavy background noise or mixed languages.
- Future work: speaker labels, Hindi summaries, live microphone recording,
  and a text-to-speech version of the summary (PS-6).
