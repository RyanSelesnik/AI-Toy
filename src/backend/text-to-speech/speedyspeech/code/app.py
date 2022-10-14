from typing import Text
from flask import Flask, send_file
from flask import request
import argparse
from inference import TextToSpeech
import torch

app = Flask(__name__)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--speedyspeech_checkpoint", default='checkpoints/speedyspeech.pth',
                        type=str, help="Checkpoint file for speedyspeech model")
    parser.add_argument("--melgan_checkpoint", default='checkpoints/melgan.pth',
                        type=str, help="Checkpoint file for MelGan.")
    parser.add_argument("--device", type=str, default='cuda' if torch.cuda.is_available()
                        else 'cpu',  help="What device to use.")
    parser.add_argument("--audio_folder", type=str,
                        default="synthesized_audio", help="Where to save audios")
    args = parser.parse_args()
    return args


@app.route('/',  methods=['POST'])
def synthesise():
    msg = request.json['message']
    tts.get_spoken_response(msg)
    path_to_file = "../synthesized_audio/0.wav"

    return send_file(
        path_to_file,
        mimetype="audio/wav",
        as_attachment=True,
        download_name="0.wav")


if __name__ == "__main__":
    args = parse_args()

    tts = TextToSpeech()
    tts.load_checkpoints(args)
    app.run(debug=True)
