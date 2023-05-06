# -*- coding: gbk -*-
import wave

def read_wave_data(filename):
    with wave.open(filename, "rb") as wav:
        frames = wav.readframes(wav.getnframes())
        return bytearray(frames)

def calculate_capacity(data, algorithm):
    # 音频数据的长度（以字节为单位）
    data_length = len(data)
    # 每个采样点的位数
    sample_width = 2
    # 每个采样点的通道数
    channels = 2
    # 采样率（每秒采样数）
    frame_rate = 44100
    # 音频的时长（秒）
    duration = data_length / (sample_width * channels * frame_rate)
    # 可用的比特数
    capacity = 0
    for i, byte in enumerate(data):
        for j in range(8):
            message_bits = [int(bit) for bit in format(byte, "08b")]
            message_bits[j] = algorithm(message_bits[j])
            if message_bits != [int(bit) for bit in format(byte, "08b")]:
                capacity += 1
    # 每秒的最大嵌入容量
    max_capacity_per_second = capacity / duration
    return max_capacity_per_second

def lsb_replace(bit):
    return 0

def lsb_matching(bit):
    return int(not bit)

if __name__ == "__main__":
    audio_data = read_wave_data("c.wav")
    lsbr_max_capacity = calculate_capacity(audio_data, lsb_replace)
    lsbm_max_capacity = calculate_capacity(audio_data, lsb_matching)
    print("LSBR最大嵌入容量：{:.2f} bps".format(lsbr_max_capacity))
    print("LSBM最大嵌入容量：{:.2f} bps".format(lsbm_max_capacity))
