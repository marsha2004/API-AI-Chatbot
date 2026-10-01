# Gemini CLI Chatbot

## What I Built
A command-line (CLI) chatbot in Python. You type a message, it is sent to Google's
Gemini model, and the reply is printed in the terminal. It remembers earlier
messages in the conversation and can optionally read replies aloud.

## Features
- Accepts user messages in the terminal
- Sends them to the Gemini API and displays the response
- Conversation history (the bot remembers context)
- Voice output (type `voice` to toggle)
- API key stored safely in `.env` (ignored by Git)

## Technology Used
- Python 3.9+
- `google-genai` (official Google GenAI SDK)
- `python-dotenv` (loads the API key from `.env`)
- `pyttsx3` (offline text-to-speech)

## How to Run
```bash
git clone <your-repo-url>
cd ai-chatbot

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env            # Windows: copy .env.example .env
# open .env and paste your key from https://aistudio.google.com/apikey

python main.py
```
Commands inside the chat: `voice` toggles voice output, `exit` quits.

## API Integration Approach
1. `python-dotenv` loads `GEMINI_API_KEY` from `.env`, so the key is never in the code.
2. A `genai.Client` is created with that key.
3. `client.chats.create(model="gemini-2.5-flash")` starts a chat session that
   stores the history automatically.
4. Each user message goes through `chat.send_message(...)`; the model sees the
   full history, and `response.text` is printed.
5. API calls are wrapped in `try/except` so network or key errors don't crash the app.

## What I Learned
- How to get API Keys
- How to call an LLM API from Python and read its response
- Why secrets belong in `.env` and `.gitignore`
- How chat sessions keep context between messages
- Basic error handling for external APIs

## What I Would Improve Next
- Streaming responses so text appears as it is generated
- A proper web UI so that it is easier for wide scale production (Streamlit or Gradio)
- Saving conversations to a file
- A system prompt to give the bot a personality
- Speech input as well as speech output
- Latency during conversations