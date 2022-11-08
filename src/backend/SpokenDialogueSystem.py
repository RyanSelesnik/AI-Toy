import argparse
import io
import re
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import tempfile
import os
import requests
#from playsound import playsound


parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--model", default="tiny", help="Model to use",
                    choices=["tiny", "base", "small", "medium", "large"])
parser.add_argument("--english", default=True,
                    help="Whether to use English model", type=bool)
parser.add_argument("--stop_word", default="stop",
                    help="Stop word to abort transcription", type=str)
parser.add_argument("--verbose", default=False,
                    help="Whether to print verbose output", type=bool)
parser.add_argument("--energy", default=300,
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
        """Record audio stream and return the WAV data as an audipo segment"""
        self.speech_engine.adjust_for_ambient_noise(source)
        audio = self.speech_engine.listen(source)
        data = io.BytesIO(audio.get_wav_data())
        return AudioSegment.from_file(data)

    def transcribe(self):
        "Convert a wave file to text through a speech to text model"
        if args.english:
            result = self.audio_model.transcribe(
                self.save_path,
                language='english',
                temperature=0.2)
        else:
            result = self.audio_model.transcribe(self.save_path)

        if not args.verbose:
            return result["text"]
        else:
            return result

    def interact(self):
        """
        Interact with the spoken dialogue system by speaking into the mic and waiting for a response
        until the user utters a stop word
        """

        with sr.Microphone(device_index=1, sample_rate=16000) as source:
            print("Speak...")
            while True:

                audio_clip = self.record_audio_stream(source)
                # Save audio clip to save_path
                audio_clip.export(self.save_path, format="wav")

                # Covert recorded audio to text
                predicted_text = self.transcribe()
                if predicted_text != '':
                    print('\nDone transcribing:')
                    print(f'\n\nYou said:\t{predicted_text}\n\n')
                    print("synethesisng speech...")
                    self.text_to_speech(predicted_text)
                        

                # If the predicted text is not empty, get a response from the backend
                #if predicted_text != '':
                    #responses = self.get_bot_response(predicted_text)
                    #print(f'responses: {responses}')
                    #for response in responses:
                    #    self.text_to_speech(response)

                    # print(f'bot response: {response}')

                if self.check_stop_word(predicted_text):
                    break

    def text_to_speech(self, text):
        text = f'You said {text}'
        url = 'http://0.0.0.0:59125/api/tts?voice=en_US/ljspeech_low'
        try:
            res = requests.post(url, data=text)
        except Exception as e:
            pass
        else:
            data = io.BytesIO(res.content)
            audio = AudioSegment.from_file(data)
            audio.export('./test.wav', format="wav")
            os.system('aplay test.wav')

    def get_bot_response(self, transcribed_text):
        """Fetch the bot's response"""

        url = 'http://0.0.0.0:5005/webhooks/rest/webhook'

        payload = {
            "sender": "test_user",
            "message": transcribed_text
        }

        responses = requests.post(url, json=payload).json()
        full_response = []
        # Loop through all bot responses
        for response in responses:
            # If its a textual response
            if 'text' in response:
                text = str(response['text']).replace("'", "")
                full_response.append(text)

        return full_response

    def check_stop_word(self, predicted_text: str) -> bool:
        # Checks for the stop word to terminate the system
        pattern = re.compile('[\W_]+', re.UNICODE)
        return pattern.sub('', predicted_text).lower() == args.stop_word


if __name__ == "__main__":
    sds = SpokenDialogueSystem()
    sds.interact()
    # sds.get_bot_response("play math game")
    # sds.text_to_speech("hello there")
