import pyaudio
import wave
import numpy as np
import os

def recording(
    output_filename="modules/voice.wav",
    format=pyaudio.paInt16,
    channels=1,
    rate=44100,     # sampling rate1
    chunk=4096,
    silence_threshold=500,  # volume threshold
    silence_duration=2      # silence duration threshold
):
    audio = pyaudio.PyAudio()

    stream = audio.open(format=format, channels=channels,
                        rate=rate, input=True,
                        frames_per_buffer=chunk)

    print("start recording...")

    frames = []
    silent_chunks = 0
    max_silent_chunks = int(rate / chunk * silence_duration)

    while True:
        data = stream.read(chunk)
        frames.append(data)

        # calc volume
        audio_data = np.frombuffer(data, dtype=np.int16)
        volume = np.abs(audio_data).mean()

        print(f"volume: {volume}")

        if volume < silence_threshold:
            silent_chunks += 1
        else:
            silent_chunks = 0

        if silent_chunks > max_silent_chunks:
            print("Recording finished.")
            break

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # 録音したデータをWAVファイルとして保存
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    print("Recording saved:", output_filename)

