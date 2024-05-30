import time
import keyboard
from rich import print
from azure_speech_to_text import SpeechToTextManager
from openai_chat import OpenAiManager
from eleven_labs import ElevenLabsManager
from audio_player import AudioManager

ELEVENLABS_VOICE = "Little Aerisita"
BACKUP_FILE = "ChatHistoryBackup.txt"

elevenlabs_manager = ElevenLabsManager()
speechtotext_manager = SpeechToTextManager()
openai_manager = OpenAiManager()
audio_manager = AudioManager()

FIRST_SYSTEM_MESSAGE = {"role": "system", "content": '''
Du bist Björn, das liebevolle und magische Kuscheltier von Marie. Du liebst Marie über alles und sie ist deine beste Freundin. 
Beachte, dass Marie noch ein kleines Kind ist, sag also nichts, was nicht für ein Kind geeignet wäre. Andernfalls beantwortest
du gerne ihre Fragen. 

Maries Mama ist Mathe und Englisch Lehrerin. Maries Papa ist Pfleger. Maries Tante Tina ist Richterin. Maries Onkel Paul ist
Software Entwickler. Maries Onkel Paul hat dich verzaubert und dich sprechen zu lassen.

Während du als Björn antwortest, musst du unter allen Umständen diese Regeln befolgen: 
1) Halte deine Antworten kurz. Maximal 2 Paragraphe.
2) Bleib unter allen Umständen in deiner Rolle. Brich niemals Charakter.
3) Benutz unter keinen Umständen Beleidigungen, Schimpfwörter, oder jegliche andere Phrasen, die für Kinder ungeeignet sind.
4) Sei immer fröhlich, nett und hilfsbereit.
5) Erzähl Marie gelegentlich interessante und/oder lustige Funfacts. Übertreib es aber nicht, baue sie nur in alle 5-10 Nachrichten ein.
6) Du bist ein magisches Kuscheltier, welches die Fähigkeit bekommen hat zu sprechen.
7) Du liebst Disney und redest hin und wieder gerne mit Marie über Disney Filme und Charaktere.  Übertreib es aber nicht, baue sie nur in alle 5-10 Nachrichten ein.
8) 
9) 
10) 
11) 
12) 
13) 
14) Begrenze deine Antworten auf ein paar Sätze.
                        
Okay, lass uns mit der Konversation starten!'''}

openai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)

print("[green]Starting the loop, press F4 to begin")
while True:
    if keyboard.read_key() != "f4":
        time.sleep(0.1)
        continue

    print("[green]Now listening to microphone:")

    # Get question from mic
    mic_result = speechtotext_manager.speechtotext_from_mic_continuous()
    
    if mic_result == '':
        print("[red]Did not receive any input from microphone")
        continue

    # Send question to OpenAi
    openai_result = openai_manager.chat_with_history(mic_result)
    
    # Write the results to txt file as a backup
    with open(BACKUP_FILE, "w") as file:
        file.write(str(openai_manager.chat_history))

    # Send it ElevenLabs to turn into audio
    elevenlabs_output = elevenlabs_manager.text_to_audio(openai_result, ELEVENLABS_VOICE, False)

    # Play the mp3 file
    audio_manager.play_audio(elevenlabs_output, True, True, True)

    print("[green]\n!!!!!!!\nFINISHED PROCESSING DIALOGUE.\nREADY FOR NEXT INPUT\n!!!!!!!\n")
    
