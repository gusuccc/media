# -*- coding: gbk -*-
import numpy as np
import pydub
from pydub import AudioSegment

# ��ȡmp3�ļ�
from scipy.io import wavfile



# ��ȡwav�ļ�
fs, audio = wavfile.read("c.wav")

# ����ÿ����֡�ĳ���
subframe_length = int(fs * 32 / 1152)

# ����ÿ����֡�п���Ƕ����Ϣ��Ƶ��ϵ��������
freq_components = subframe_length // 2

# ����ÿ��Ƶ��ϵ������Ƕ�����Ϣλ��
bit_per_component = 1

# ������Ƶ�ļ��а�������֡����
num_subframes = len(audio) // subframe_length

# �������Ƕ������
max_capacity = freq_components * bit_per_component * num_subframes

print("���Ƕ��������", max_capacity, "λ")

