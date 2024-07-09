import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer
import difflib


def load_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().lower().split()


def recognize_from_microphone():
    # Load Vosk model
    model = Model("C:\\Users\\msimbisayi\Private\\vosk_model_small")
    recognizer = KaldiRecognizer(model, 16000)

    # Initialize PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=4096)
    stream.start_stream()

    print("Listening...")
    text = ''
    stop_flag = False
    textfile_text = load_text_file("C:\\Users\\msimbisayi\Private\\read.txt")

    try:
        while True and not stop_flag:
            data = stream.read(4096)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result)["text"] + " "
                text = text.split(' ')
                for word in text:
                    next_word = textfile_text.pop(0)
                    if word not in next_word:
                        stop_flag = True
                        print("Stopped, you said: {}".format(text))
                        break
                    if "stop" in next_word.lower():
                        print("Stopped, you said: {}".format(text))
                        break
    except KeyboardInterrupt:
        print("You said: {}".format(text))
        print("Stopped by user")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == "__main__":
    recognize_from_microphone()
