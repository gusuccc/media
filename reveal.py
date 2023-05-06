# -*- coding: gbk -*-

import wave

from max_stego import read_wave_data
from max_stego import lsb_replace
from max_stego import lsb_matching


def extract_message(data, bit, algorithm):
    message_bits = []
    for byte in data:
        message_bits.append(format(byte, "08b")[-1])
    message_bits = message_bits[:-(len(message_bits) % 8)]
    message = bytearray()
    for i in range(0, len(message_bits), 8):
        byte = int("".join(message_bits[i:i+8]), 2)
        if byte == 0:
            break
        message.append(byte)
    return message.decode("utf-8")


if __name__ == "__main__":
    # 读取音频文件的数据
    stego_data = read_wave_data("lsbr_stego_audio.wav")

    # 提取LSBR算法嵌入的消息
    message = extract_message(stego_data, "0", lsb_replace)
    with open("lsbr_extracted_message.txt", "w") as f:
        f.write(message)

    # 提取LSBM算法嵌入的消息
    message = extract_message(stego_data, "0", lsb_matching)
    with open("lsbm_extracted_message.txt", "w") as f:
        f.write(message)
