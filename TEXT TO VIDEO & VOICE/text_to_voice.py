import pyttsx3
import os

def generate_voice(text, output_path="outputs/output_audio.wav"):
    # Initialize engine
    engine = pyttsx3.init()

    # Properties
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)

    voices = engine.getProperty('voices')
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)

    # Save file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    engine.stop()

    return output_path