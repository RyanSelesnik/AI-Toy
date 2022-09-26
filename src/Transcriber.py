# TO DO: add kenLM as the language model or just use huggingFaces

from typing_extensions import Self
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC, Wav2Vec2ProcessorWithLM, Wav2Vec2CTCTokenizer
from pyctcdecode import build_ctcdecoder
import json


from datasets import load_dataset


class Transcriber():
    def __init__(self, model_name):
        self.processor = Wav2Vec2Processor.from_pretrained(model_name)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_name)

        # Extract vocabulary from tokenizer to use for pyctcdecode
        vocab_dict = self.processor.tokenizer.get_vocab()

        self.sorted_vocab_dict = {k.lower(): v for k, v in sorted(
            vocab_dict.items(), key=lambda item: item[1])}
        vocab_file = "vocab.json"

        with open(vocab_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.sorted_vocab_dict, ensure_ascii=False))

        self.processor.tokenizer = Wav2Vec2CTCTokenizer(vocab_file)
        self.processor.save_pretrained("./processor")
        self.processor = Wav2Vec2Processor.from_pretrained(
            "./processor", eos_token=None, bos_token=None)

        vocab_dict = self.processor.tokenizer.get_vocab()
        self.sorted_vocab_dict = {k.lower(): v for k, v in sorted(
            vocab_dict.items(), key=lambda item: item[1])}

        decoder = build_ctcdecoder(
            labels=list(self.sorted_vocab_dict.keys()),
            kenlm_model_path="5gram_correct.arpa",
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
                The transcribed string"""

        if (len(audio_buffer) == 0):
            return ""

        inputs = self.processor(torch.tensor(
            audio_buffer), sampling_rate=16_000, return_tensors="pt", padding=True)
        with torch.no_grad():
            # Get token probabilities to pass to the decoder
            logits = self.model(**inputs).logits.numpy()

        transcription = self.processor.batch_decode(logits)

        return transcription[0][0]


def main():
    transcriber = Transcriber('facebook/wav2vec2-base-100h')
    dataset = load_dataset(
        "hf-internal-testing/librispeech_asr_demo", "clean", split="validation")
    audio_sample = dataset[2]
    transcription = transcriber.transcribe(audio_sample["audio"]["array"])
    print(transcription)


if __name__ == '__main__':
    main()
