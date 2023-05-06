# -*- coding: gbk -*-
import numpy as np
import pydub
from pydub import AudioSegment

# 读取mp3文件
from scipy.io import wavfile



# 读取wav文件
fs, audio = wavfile.read("c.wav")

# 计算每个子帧的长度
subframe_length = int(fs * 32 / 1152)

# 计算每个子帧中可以嵌入信息的频域系数的数量
freq_components = subframe_length // 2

# 计算每个频域系数可以嵌入的信息位数
bit_per_component = 1

# 计算音频文件中包含的子帧数量
num_subframes = len(audio) // subframe_length

# 计算最大嵌入容量
max_capacity = freq_components * bit_per_component * num_subframes

print("最大嵌入容量：", max_capacity, "位")

