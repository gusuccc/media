# -*- coding: gbk -*-
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

# 读取原始音频文件和嵌入信息的音频文件
fs_orig, audio_orig = wavfile.read("c.wav")
fs_stego_LSBR, audio_stego_LSBR = wavfile.read("lsbr_stego_audio.wav")
fs_stego_LSBM, audio_stego_LSBM = wavfile.read("lsbm_stego_audio.wav")

# 分别计算两个音频文件的直方图
bins = np.linspace(-1, 1, 256)
hist_orig, _ = np.histogram(audio_orig, bins=bins)
hist_stego_LSBR, _ = np.histogram(audio_stego_LSBR, bins=bins)
hist_stego_LSBM, _ = np.histogram(audio_stego_LSBM, bins=bins)

# 画出直方图
plt.figure()
plt.hist(audio_orig, bins=10000, alpha=0.5, label='Original')
plt.hist(audio_stego_LSBR, bins=10000, alpha=0.5, label='LSBR')
plt.hist(audio_stego_LSBM, bins=10000, alpha=0.5, label='LSBM')
plt.xlabel('Sample Value')
plt.ylabel('Count')
plt.legend(loc='upper right')
plt.xlim(-5,5)
plt.show()

# 画出直方图
#plt.figure()
#plt.hist(audio_orig, bins=256, alpha=0.5, label='Original')
#plt.hist(audio_stego_LSBM, bins=256, alpha=0.5, label='LSBM')
#plt.xlabel('Sample Value')
#plt.ylabel('Count')
#plt.legend(loc='upper right')
#plt.xlim(-1000,1000)
#plt.show()


