# -*- coding: gbk -*-
import wave


def read_wave_data(filename):
    with wave.open(filename, "rb") as wav:
        frames = wav.readframes(wav.getnframes())
        return bytearray(frames)


def write_wave_data(filename, data):
    with wave.open(filename, "wb") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(44100)
        wav.writeframes(data)


def lsb_algorithm(data, message, bit, algorithm):
    message = bytearray(message, "utf-8")
    #print(message)
    message += bytearray(b"\0")
    message_bits = [bit for b in message for bit in format(b, "08b")]
    message_bits = message_bits + [bit] * (len(data) - len(message_bits))
    stego_data = algorithm(data, message_bits)
    return stego_data


def lsb_replace(data, message_bits):
    stego_data = bytearray()
    for i, byte in enumerate(data):
        stego_byte = byte & ~1 | int(message_bits[i])
        stego_data.append(stego_byte)
    return stego_data


def lsb_matching(data, message_bits):
    stego_data = bytearray()
    for i, byte in enumerate(data):
        if i % 2 == 0:
            bit_to_replace = int(message_bits[i])
        else:
            bit_to_replace = int(message_bits[i - 1] != message_bits[i])
        stego_byte = byte & ~1 | bit_to_replace
        stego_data.append(stego_byte)
    return stego_data



if __name__ == "__main__":
    # 读取音频文件和文本文件的数据
    audio_data = read_wave_data("c.wav")
    with open("1.txt", "r") as f:
        message = f.read()

    # 使用LSBR算法嵌入消息
    lsbbr_stego_data = lsb_algorithm(audio_data, message, "0", lsb_replace)
    write_wave_data("lsbr_stego_audio.wav", lsbbr_stego_data)

    # 使用LSBM算法嵌入消息
    lsbm_stego_data = lsb_algorithm(audio_data, message, "0", lsb_matching)
    write_wave_data("lsbm_stego_audio.wav", lsbm_stego_data)
