from operator import is_not
import pyaudio
from Transcriber import Transcriber
import webrtcvad
import numpy as np
import threading
import copy
import time
from sys import exit
import contextvars
from queue import Queue


class ASR():
    exit_event = threading.Event()

    def __init__(self, model_name, device_name="default"):
        self.model_name = model_name
        self.device_name = device_name

    def stop(self):
        """stop the ASR process"""
        ASR.exit_event.set()
        self.asr_input_queue.put("close")
        print("ASR stopped")

    def start(self):
        """start the asr process"""
        self.asr_output_queue = Queue()
        self.asr_input_queue = Queue()
        self.asr_process = threading.Thread(target=ASR.asr_process, args=(
            self.model_name, self.asr_input_queue, self.asr_output_queue,))
        self.asr_process.start()
        time.sleep(5)  # start vad after asr model is loaded
        self.vad_process = threading.Thread(target=ASR.vad_process, args=(
            self.device_name, self.asr_input_queue,))
        self.vad_process.start()

    def vad_process(device_name, asr_input_queue):
        """Detects voice activity"""
        vad = webrtcvad.Vad()
        # 0 is the least aggressive about filtering out non-speech, 3 is the most aggressive.
        vad.set_mode(3)

        audio = pyaudio.PyAudio()
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        SAMPLE_RATE = 16000
        # A frame must be either 10, 20, or 30 ms in duration for webrtcvad
        WINDOW_DURATION = 30
        # Essentially how many samples per 30 ms
        SAMPLES_PER_WINDOW = int(SAMPLE_RATE * WINDOW_DURATION / 1000)
        RECORD_SECONDS = 50

        microphones = ASR.list_microphones(audio)
        selected_input_device_id = ASR.get_input_device_id(
            device_name, microphones)

        stream = audio.open(input_device_index=selected_input_device_id,
                            format=FORMAT,
                            channels=CHANNELS,
                            rate=SAMPLE_RATE,
                            input=True,
                            frames_per_buffer=SAMPLES_PER_WINDOW)

        frames = b''
        NUM_OF_WINDOW_DURATIONS = 1
        is_not_speech = 0
        while True:
            if ASR.exit_event.is_set():
                break
            frame = stream.read(SAMPLES_PER_WINDOW,
                                exception_on_overflow=False)
            is_speech = vad.is_speech(frame, SAMPLE_RATE)
            if is_speech:
                frames += frame
            elif is_not_speech > NUM_OF_WINDOW_DURATIONS:
                if len(frames) > 1:
                    asr_input_queue.put(frames)
                frames = b''
                is_not_speech = 0
            else:
                is_not_speech += 1

        stream.stop_stream()
        stream.close()
        audio.terminate()

    def asr_process(model_name, in_queue, output_queue):
        transcriber = Transcriber(model_name, use_lm=True)

        print("\nlistening to your voice\n")
        while True:
            audio_frames = in_queue.get()
            if audio_frames == "close":
                break

            # 2^15-1 = 32767
            MAX_16_BIT_INT = 32767
            float64_buffer = np.frombuffer(
                audio_frames, dtype=np.int16) / MAX_16_BIT_INT
            start = time.perf_counter()
            text = transcriber.transcribe(float64_buffer)
            text = text.lower()
            inference_time = time.perf_counter()-start
            sample_length = len(float64_buffer) / 16000  # length in sec
            if text != "":
                output_queue.put(
                    [text, sample_length, inference_time])

    def get_input_device_id(device_name, microphones):
        for device in microphones:
            if device_name in device[1]:
                return device[0]

    def list_microphones(pyaudio_instance):
        info = pyaudio_instance.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        result = []
        for i in range(0, numdevices):
            if (pyaudio_instance.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                name = pyaudio_instance.get_device_info_by_host_api_device_index(
                    0, i).get('name')
                result += [[i, name]]
        return result

    def get_last_text(self):
        """returns the text, sample length and inference time in seconds."""
        return self.asr_output_queue.get()


if __name__ == "__main__":
    print("Live ASR")

    asr = ASR("facebook/wav2vec2-base-100h")
    # asr = ASR("patrickvonplaten/wav2vec2-base-100h-with-lm")

    asr.start()

    try:
        while True:
            text, sample_length, inference_time = asr.get_last_text()
            print(
                f"{sample_length:.3f}s\t{inference_time:.3f}\t{text}")

    except KeyboardInterrupt:
        asr.stop()
        exit()
