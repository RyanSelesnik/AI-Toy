import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC, Wav2Vec2ProcessorWithLM, Wav2Vec2CTCTokenizer
from pyctcdecode import build_ctcdecoder
import json
import argparse
import os


from datasets import load_dataset


class Transcriber():
    def __init__(self, model_name, use_lm):
        self.use_lm = use_lm
        self.processor = Wav2Vec2Processor.from_pretrained(model_name)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_name)
        if use_lm:
            # Extract vocabulary from tokenizer to use for pyctcdecode
            vocab_dict = self.processor.tokenizer.get_vocab()

            self.sorted_vocab_dict = {k.lower(): v for k, v in sorted(
                vocab_dict.items(), key=lambda item: item[1])}
            vocab_file = "LM_vocab.json"

            with open(vocab_file, "w", encoding="utf-8") as f:
                f.write(json.dumps(self.sorted_vocab_dict, ensure_ascii=False))

            self.processor.tokenizer = Wav2Vec2CTCTokenizer(vocab_file)
            os.system(f'rm {vocab_file}')
            self.processor.save_pretrained("./processor")
            self.processor = Wav2Vec2Processor.from_pretrained(
                "./processor", eos_token=None, bos_token=None)

            os.system("rm -r ./processor")
            vocab_dict = self.processor.tokenizer.get_vocab()
            self.sorted_vocab_dict = {k.lower(): v for k, v in sorted(
                vocab_dict.items(), key=lambda item: item[1])}

            decoder = build_ctcdecoder(
                labels=list(self.sorted_vocab_dict.keys()),
                kenlm_model_path="5gram_correct.bin",
            )
            self.processor = Wav2Vec2ProcessorWithLM(
                feature_extractor=self.processor.feature_extractor,
                tokenizer=self.processor.tokenizer,
                decoder=decoder)

    def transcribe(self, audio_buffer, use_lm=True):
        """Transcribes audio to text

            Args:
                audio_buffer: an array of floats not sure if it has to be fp32 or fp16
                use_lm: a boolean indicating whether to use a language model or not
                TO DO: take in sample rate

            Returns:
                The transcribed string
        """

        if (len(audio_buffer) == 0):
            return ""

        inputs = self.processor(torch.tensor(
            audio_buffer), sampling_rate=16_000, return_tensors="pt", padding=True)
        with torch.no_grad():
            if self.use_lm:
                # Get token probabilities to pass to the decoder
                logits = self.model(**inputs).logits.numpy()
            else:
                logits = self.model(**inputs).logits
                predicted_ids = torch.argmax(logits, dim=-1)
                transcription = self.processor.batch_decode(predicted_ids)
                return transcription[0].lower()

        transcription = self.processor.batch_decode(logits)

        return transcription[0][0]


def main(args):
    transcriber = Transcriber('facebook/wav2vec2-base-100h', args.use_lm)
    librispeech_eval = load_dataset("librispeech_asr", "clean", split="test")

    dataset = load_dataset(
        "hf-internal-testing/librispeech_asr_demo", "clean", split="validation")
    audio_sample = dataset[2]
    text = dataset.map(transcriber.transcribe, args(args.use_lm))
    # transcription = transcriber.transcribe(audio_sample["audio"]["array"])
    # print(transcription)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    def str2bool(v):
        if isinstance(v, bool):
            return v
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    parser.add_argument(
        "--use_lm", default=False, type=str2bool, required=True, help="Use a language model"
    )
    args = parser.parse_args()
    main(args)
