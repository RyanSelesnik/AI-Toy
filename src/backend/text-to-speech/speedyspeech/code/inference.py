"""Synthesize audio from text

echo "One sentence. \nAnother sentence. | python code/inference.py checkpoint1 checkpoint2 --device cuda --audio_folder ~/audio
cat text.txt | python code/inference.py checkpoint1 checkpoint2 --device cuda

Run from the project root.
Audios are by default saved to ~/audio.
Does not handle numbers - write everything in words.

usage: inference.py [-h] [--speedyspeech_checkpoint SPEEDYSPEECH_CHECKPOINT]
                    [--melgan_checkpoint MELGAN_CHECKPOINT] [--device DEVICE]
                    [--audio_folder AUDIO_FOLDER]

optional arguments:
  -h, --help            show this help message and exit
  --speedyspeech_checkpoint SPEEDYSPEECH_CHECKPOINT
                        Checkpoint file for speedyspeech model
  --melgan_checkpoint MELGAN_CHECKPOINT
                        Checkpoint file for MelGan.
  --device DEVICE       What device to use.
  --audio_folder AUDIO_FOLDER
                        Where to save audios
"""
import argparse
import sys
import os
import time
import torch
from librosa.output import write_wav

from speedyspeech import SpeedySpeech
from melgan.model.generator import Generator
from melgan.utils.hparams import HParam
from hparam import HPStft, HPText
from utils.text import TextProcessor
from functional import mask
from torch.profiler import profile, record_function, ProfilerActivity

class TextToSpeech():

    def __init__(self, m="", melgan="", spec=""):
        self.m = m
        self.melgan = melgan
        self.spec = spec

    def load_checkpoints(self, args):
        print('Loading model checkpoints')
        self.m = SpeedySpeech(
            device=args.device
        ).load(args.speedyspeech_checkpoint, map_location=args.device)
        self.m.eval()
        checkpoint = torch.load(args.melgan_checkpoint,
                                map_location=args.device)
        hp = HParam("code/melgan/config/default.yaml")
        self.melgan = Generator(hp.audio.n_mel_channels).to(args.device)
        self.melgan.load_state_dict(checkpoint["model_g"])
        self.melgan.eval(inference=False)

    def get_spoken_response(self, user_input, device='cpu'):
        print('Processing text')
        txt_processor = TextProcessor(
            HPText.graphemes, phonemize=HPText.use_phonemes)
        text = [user_input.strip()]
        phonemes, plen = txt_processor(text)
        # append more zeros - avoid cutoff at the end of the largest sequence
        phonemes = torch.cat(
            (phonemes, torch.zeros(len(phonemes), 5).long()), dim=-1)
        phonemes = phonemes.to(device)
        self.synthesise_speech(phonemes, plen)
        self.generate_audio()

    def synthesise_speech(self, phonemes, plen, device='cpu'):
        print('Synthesizing')
        # generate spectrograms
        with torch.no_grad():
            self.spec, durations = self.m((phonemes, plen))
        # invert to log(mel-spectrogram)
        self.spec = self.m.collate.norm.inverse(self.spec)
        # mask with pad value expected by MelGan
        msk = mask(self.spec.shape, durations.sum(
            dim=-1).long(), dim=1).to(device)
        self.spec = self.spec.masked_fill(~msk, -11.5129)
        # Append more pad frames to improve end of the longest sequence
        self.spec = torch.cat((self.spec.transpose(
            2, 1), -11.5129*torch.ones(len(self.spec), HPStft.n_mel, 5).to(device)), dim=-1)

    def generate_audio(self, audio_folder='synthesized_audio'):
        # generate audio
        with torch.no_grad():
            audio = self.melgan(self.spec).squeeze(1)
        print('Saving audio')
        # TODO: cut audios to proper length
        for i, a in enumerate(audio.detach().cpu().numpy()):
            write_wav(os.path.join(audio_folder,
                                   f'{i}.wav'), a, HPStft.sample_rate, norm=False)


def main(args):
    generator = TextToSpeech()
    with torch.profiler.profile(profile_memory=True, with_flops=True) as prof:
        generator.load_checkpoints(args)
        generator.get_spoken_response("Hey there how are you")
    print(prof.key_averages().table(sort_by="self_cpu_time_total"))

if __name__ == "__main__":
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

    main(args)
