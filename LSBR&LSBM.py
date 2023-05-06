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

def lsb_encode_using_lsbr(audio_file, message_file, stego_file):
    audio_data = read_wave_data(audio_file)
    with open(message_file, "r") as f:
        message = f.read()
    # 计算嵌入容量
    capacity = len(audio_data) * 8 // 9
    message_length = len(message) * 8
    if message_length > capacity:
        message = message[:capacity // 8]
    # 使用LSBR算法嵌入消息
    lsbbr_stego_data = lsb_algorithm(audio_data, message, "0", lsb_replace)
    write_wave_data(stego_file, lsbbr_stego_data)

def lsb_encode_using_lsbm(audio_file, message_file, stego_file):
    audio_data = read_wave_data(audio_file)
    with open(message_file, "r") as f:
        message = f.read()
    # 计算嵌入容量
    capacity = len(audio_data) // 2
    message_length = len(message) * 8
    if message_length > capacity:
        message = message[:capacity // 8]
    # 使用LSBM算法嵌入消息
    lsbm_stego_data = lsb_algorithm(audio_data, message, "0", lsb_matching)
    write_wave_data(stego_file, lsbm_stego_data)

def reveal_message_using_lsbr(stego_file, message_file):
    stego_data = read_wave_data(stego_file)
    # 读取消息长度
    message_length_bits = []
    for i in range(64):
        message_length_bits.append(str(stego_data[i] & 1))
    message_length = int("".join(message_length_bits), 2)
    # 读取消息
    message_bits = []
    for i in range(64, (message_length + 1) * 8, 9):
        byte_bits = "".join([str(bit & 1) for bit in stego_data[i:i+8]])
        message_bits.append(byte_bits)
    message = bytearray([int(bits, 2) for bits in message_bits]).decode("utf-8").rstrip("\0")
    # 写入消息
    with open(message_file, "w") as f:
        f.write(message)



def reveal_message_using_lsbm(stego_file, message_file):
    # 读取音频文件数据
    audio_data = read_wave_data(stego_file)

    # 获取嵌入消息的大小
    message_size = 0
    for i in range(32):
        message_size <<= 1
        message_size |= audio_data[i] & 1

    # 提取嵌入的消息
    message_bits = []
    for i in range(message_size * 8):
        if i % 2 == 0:
            bit_to_extract = audio_data[i + 32] & 1
        else:
            bit_to_extract = audio_data[i + 32 - 1] & 1
        message_bits.append(str(bit_to_extract))

    message = ""
    for i in range(0, len(message_bits), 8):
        message += chr(int("".join(message_bits[i:i + 8]), 2))
        if message.endswith("\0"):
            break

    # 将消息写入文件
    with open(message_file, "w") as f:
        f.write(message.rstrip("\0"))

    print("Message revealed successfully.")


if __name__ == "__main__":
    # 读取音频文件和文本文件的数据
    audio_data = read_wave_data("c.wav")
    with open("1.txt", "r") as f:
        message = f.read()

    # 使用LSBR算法嵌入消息
    lsbr_stego_data = lsb_algorithm(audio_data, message, "0", lsb_replace)
    write_wave_data("lsbr_stego_audio.wav", lsbr_stego_data)

    # 使用LSBM算法嵌入消息
    lsbm_stego_data = lsb_algorithm(audio_data, message, "0", lsb_matching)
    write_wave_data("lsbm_stego_audio.wav", lsbm_stego_data)

    # 提取LSBR算法嵌入的消息
    #reveal_message_using_lsbr("lsbr_stego_audio.wav", "lsbr_extracted_message.txt")

    # 提取LSBM算法嵌入的消息
    reveal_message_using_lsbm("lsbm_stego_audio.wav", "lsbm_extracted_message.txt")
