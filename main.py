import os
import sys

from dotenv import load_dotenv
from google import genai

MODEL_NAME = "gemini-3.8-flash"


def load_client() -> genai.Client:
    """Read GEMINI_API_KEY from .env and create the API client."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        sys.exit("Error: GEMINI_API_KEY not found. Copy .env.example to .env and add your key.")
    return genai.Client(api_key=api_key)


def setup_voice():
    """Bonus: text-to-speech. Returns an engine, or None if unavailable."""
    try:
        import pyttsx3
        return pyttsx3.init()
    except Exception:
        print("(Voice output unavailable - install pyttsx3 to enable it.)")
        return None


def speak(engine, text: str) -> None:
    engine.say(text)
    engine.runAndWait()


def main() -> None:
    client = load_client()

    previous_id = None   # id of the last interaction = conversation memory
    voice_engine = None

    print("Gemini Chatbot")
    print("Commands: 'exit' to quit, 'voice' to toggle voice output, 'clear' to reset memory.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        if user_input.lower() == "clear":
            previous_id = None
            print("Memory sucessfully cleared.\n")
            continue
        if user_input.lower() == "voice":
            if voice_engine is None:
                voice_engine = setup_voice()
                if voice_engine:
                    print("Voice output ON.")
            else:
                voice_engine = None
                print("Voice output OFF.")
            continue

        try:
            # Send the message to the API (previous_id links it to earlier turns)
            interaction = client.interactions.create(
                model=MODEL_NAME,
                input=user_input,
                previous_interaction_id=previous_id,
            )
            reply = interaction.output_text
            previous_id = interaction.id   # remember for the next turn
        except Exception as e:
            print(f"Error talking to the API: {e}\n")
            continue

        print(f"ChatBot: {reply}\n")
        if voice_engine:
            speak(voice_engine, reply)


if __name__ == "__main__":
    main()
