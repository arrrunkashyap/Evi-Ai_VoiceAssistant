from audio.listener import listen
from audio.speaker import speak

speak("Hello, I am EVI.")

while True:
    text = listen()

    if text:
        speak(f"You said {text}")

    if text == "exit":
        speak("Goodbye.")
        break