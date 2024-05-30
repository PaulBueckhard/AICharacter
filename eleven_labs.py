from elevenlabs import generate, stream, set_api_key, voices, play, save
import time
import os
from dotenv import load_dotenv

load_dotenv()
try:
  set_api_key(os.getenv('ELEVENLABS_API_KEY'))
except TypeError:
  exit("Could not access ELEVENLABS_API_KEY")

class ElevenLabsManager:
    def __init__(self):
        all_voices = voices()
        print(f"\nAll ElevenLabs voices: \n{all_voices}\n")

    # Convert text to speech, save to file, return file path
    def text_to_audio(self, input_text, voice="Little Aerisita", save_as_wave=True, subdirectory=""):
        audio_saved = generate(
          text=input_text,
          voice=voice,
          model="eleven_multilingual_v1"
        )
        if save_as_wave:
          file_name = f"___Msg{str(hash(input_text))}.wav"
        else:
          file_name = f"___Msg{str(hash(input_text))}.mp3"
        tts_file = os.path.join(os.path.abspath(os.curdir), subdirectory, file_name)
        save(audio_saved,tts_file)
        return tts_file

    # Convert text to speech, play out loud
    def text_to_audio_played(self, input_text, voice="Little Aerisita"):
        audio = generate(
          text=input_text,
          voice=voice,
          model="eleven_multilingual_v1"
        )
        play(audio)

    # Convert text to speech, stream out loud
    def text_to_audio_streamed(self, input_text, voice="Little Aerisita"):
        audio_stream = generate(
          text=input_text,
          voice=voice,
          model="eleven_multilingual_v1",
          stream=True
        )
        stream(audio_stream)
