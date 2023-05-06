# -*- coding: gbk -*-
import wave

def read_wave_data(filename):
    with wave.open(filename, "rb") as wav:
        frames = wav.readframes(wav.getnframes())
        return bytearray(frames)

def calculate_capacity(data, algorithm):
    # ��Ƶ���ݵĳ��ȣ����ֽ�Ϊ��λ��
    data_length = len(data)
    # ÿ���������λ��
    sample_width = 2
    # ÿ���������ͨ����
    channels = 2
    # �����ʣ�ÿ���������
    frame_rate = 44100
    # ��Ƶ��ʱ�����룩
    duration = data_length / (sample_width * channels * frame_rate)
    # ���õı�����
    capacity = 0
    for i, byte in enumerate(data):
        for j in range(8):
            message_bits = [int(bit) for bit in format(byte, "08b")]
            message_bits[j] = algorithm(message_bits[j])
            if message_bits != [int(bit) for bit in format(byte, "08b")]:
                capacity += 1
    # ÿ������Ƕ������
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
    print("LSBR���Ƕ��������{:.2f} bps".format(lsbr_max_capacity))
    print("LSBM���Ƕ��������{:.2f} bps".format(lsbm_max_capacity))
