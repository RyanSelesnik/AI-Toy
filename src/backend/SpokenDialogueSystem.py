import argparse
import io
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

temp_dir = tempfile.mkdtemp()
save_path = os.path.join(temp_dir, "temp.wav")


class SpokenDialogueSystem():

    def __init__(self) -> None:
        transcrinber_model = args.model
        # there are no english models for large
        if args.model != "large" and args.english:
            self.model = transcrinber_model + ".en"
        self.audio_model = whisper.load_model(transcrinber_model)

        # load the speech recognizer with CLI settings
        self.r = sr.Recognizer()
        self.r.energy_threshold = args.energy
        self.r.pause_threshold = args.pause
        self.r.dynamic_energy_threshold = args.dynamic_energy

    def interact(self) -> str:
        print("Speak...")
        with sr.Microphone(sample_rate=16000) as source:
            while True:

                # record audio stream into wav
                audio = self.r.listen(source)
                data = io.BytesIO(audio.get_wav_data())
                audio_clip = AudioSegment.from_file(data)
                audio_clip.export(save_path, format="wav")

                if args.english:
                    result = self.audio_model.transcribe(
                        save_path, language='english')
                    response = self.get_bot_response(result['text'])
                else:
                    result = self.audio_model.transcribe(save_path)

                if not args.verbose:
                    predicted_text = result["text"]
                    print("Input: " + predicted_text)
                    print(f"Bot response: {response}")
                else:
                    print(result)

                if self.check_stop_word(predicted_text):
                    break

    def get_bot_response(self, transcribed_text):
        url = 'http://0.0.0.0:5005/webhooks/rest/webhook'
        payload = {
            "sender": "test_user",
            "message": transcribed_text
        }
        response = requests.post(url, json=payload).json()
        return response[0]['text']

    def check_stop_word(self, predicted_text: str) -> bool:
        import re
        pattern = re.compile('[\W_]+', re.UNICODE)
        return pattern.sub('', predicted_text).lower() == args.stop_word


if __name__ == "__main__":
    sds = SpokenDialogueSystem()
    sds.interact()
