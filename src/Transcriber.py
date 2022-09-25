# TO DO: add kenLM as the language model or just use huggingFaces

from typing_extensions import Self
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

from datasets import load_dataset


class Transcriber():
    def __init__(self, model_name):
        self.processor = Wav2Vec2Processor.from_pretrained(model_name)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_name)

    def transcribe(self, audio_buffer, use_lm=True):
        """Transcribes audio to text

            Args:
                audio_buffer: an array of floats
                use_lm: a boolean indicating whether to use a language model or not 

            Returns:
                The transcribed string

        """

        if (len(audio_buffer) == 0):
            return ""

        inputs = self.processor(torch.tensor(
            audio_buffer), sampling_rate=16_000, return_tensors="pt", padding=True)
        with torch.no_grad():
            logits = self.model(**inputs).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)

        return transcription[0].lower()


def main():
    transcriber = Transcriber('facebook/wav2vec2-base-100h')
    dataset = load_dataset(
        "hf-internal-testing/librispeech_asr_demo", "clean", split="validation")
    audio_sample = dataset[2]
    print(audio_sample["audio"]["array"])
    transcription = transcriber.transcribe(audio_sample["audio"]["array"])
    print(transcription)


if __name__ == '__main__':
    main()
