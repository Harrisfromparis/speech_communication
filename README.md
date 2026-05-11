# Let's Talk

Let's Talk is a Streamlit app focused on speech communication support. It combines a guided chatbot, a voice-practice experience called Speakify, community sharing, learning resources, and simple speech activities.

## Features

- **Let's Talk chatbot** for questions about speech communication and support resources
- **Speakify practice** to hear prompts, speak them aloud, and review browser-generated transcripts
- **Community page** for sharing thoughts and encouragement
- **Resources page** with helpful links and tips
- **Activities page** with a quick word-definition game

## Project Structure

- `/home/runner/work/speech_communication/speech_communication/app.py` - main Streamlit application
- `/home/runner/work/speech_communication/speech_communication/templates/index.html` - embedded Speakify voice-practice experience
- `/home/runner/work/speech_communication/speech_communication/pdf.pdf` - document used by the chatbot retrieval flow

## Installation

1. Create and activate a Python virtual environment.
2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Add an `.env` file with your `OPENAI_API_KEY`.

## Run the App

```bash
streamlit run app.py
```

## Notes

- Speakify uses browser speech APIs, so microphone access and speech recognition depend on browser support.
- The chatbot uses the local PDF knowledge source together with the configured OpenAI key.
