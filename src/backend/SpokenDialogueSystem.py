import argparse
import io
import re
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import tempfile
import os
import requests


parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--model", default="base", help="Model to use",
                    choices=["tiny", "base", "small", "medium", "large"])
parser.add_argument("--english", default=True,
                    help="Whether to use English model", type=bool)
parser.add_argument("--stop_word", default="stop",
                    help="Stop word to abort transcription", type=str)
parser.add_argument("--verbose", default=False,
                    help="Whether to print verbose output", type=bool)
parser.add_argument("--energy", default=500,
                    help="Energy level for mic to detect", type=int)
parser.add_argument("--dynamic_energy", default=False,
                    help="Flag to enable dynamic energy", type=bool)
parser.add_argument("--pause", default=0.8,
                    help="Minimum length of silence (sec) that will register as the end of a phrase", type=float)
args = parser.parse_args()


class SpokenDialogueSystem():

    def __init__(self) -> None:
        transcrinber_model = args.model
        # there are no english models for large
        if args.model != "large" and args.english:
            self.model = transcrinber_model + ".en"
        self.audio_model = whisper.load_model(transcrinber_model)

        # load the speech recognizer with CLI settings
        self.speech_engine = sr.Recognizer()
        self.speech_engine.energy_threshold = args.energy
        self.speech_engine.pause_threshold = args.pause
        self.speech_engine.dynamic_energy_threshold = args.dynamic_energy

        temp_dir = tempfile.mkdtemp()
        self.save_path = os.path.join(temp_dir, "temp.wav")

    def record_audio_stream(self, source):
        # record audio stream into wav
        self.speech_engine.adjust_for_ambient_noise(source)
        audio = self.speech_engine.listen(source)
        data = io.BytesIO(audio.get_wav_data())
        return AudioSegment.from_file(data)

    def transcribe(self):
        if args.english:
            result = self.audio_model.transcribe(
                self.save_path, language='english')
        else:
            result = self.audio_model.transcribe(self.save_path)

        if not args.verbose:
            return result["text"]
        else:
            return result

    def interact(self):
        print("Speak...")
        with sr.Microphone(sample_rate=16000) as source:
            while True:

                audio_clip = self.record_audio_stream(source)
                audio_clip.export(self.save_path, format="wav")

                predicted_text = self.transcribe()
                if predicted_text != '':
                    response = self.get_bot_response(predicted_text)
                    print(f'input: {predicted_text}')
                    print(f'bot response: {response}')

                if self.check_stop_word(predicted_text):
                    break

    def get_bot_response(self, transcribed_text):
        url = 'http://0.0.0.0:5005/webhooks/rest/webhook'
        payload = {
            "sender": "test_user",
            "message": transcribed_text
        }
        responses = requests.post(url, json=payload).json()
        full_response = ""
        for response in responses:
            if 'text' in response:
                full_response += f"{response['text']}\n"

        return full_response

    def check_stop_word(self, predicted_text: str) -> bool:
        pattern = re.compile('[\W_]+', re.UNICODE)
        return pattern.sub('', predicted_text).lower() == args.stop_word


if __name__ == "__main__":
    sds = SpokenDialogueSystem()
    sds.interact()
