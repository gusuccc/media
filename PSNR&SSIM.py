# -*- coding: gbk -*-
import cv2
import numpy as np

def calculate_psnr(img1, img2):
    """
    ��������ͼ���PSNRֵ
    """
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return float('inf')
    PIXEL_MAX = 255.0
    return 20 * np.log10(PIXEL_MAX / np.sqrt(mse))

def calculate_ssim(img1, img2):
    """
    ��������ͼ���SSIMֵ
    """
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    C1 = 6.5025
    C2 = 58.5225
    img1_sq = img1 ** 2
    img2_sq = img2 ** 2
    img12 = img1 * img2
    mu1 = cv2.GaussianBlur(img1, (11, 11), 1.5)
    mu2 = cv2.GaussianBlur(img2, (11, 11), 1.5)
    mu1_sq = mu1 ** 2
    mu2_sq = mu2 ** 2
    mu12 = mu1 * mu2
    sigma1_sq = cv2.GaussianBlur(img1_sq, (11, 11), 1.5) - mu1_sq
    sigma2_sq = cv2.GaussianBlur(img2_sq, (11, 11), 1.5) - mu2_sq
    sigma12 = cv2.GaussianBlur(img12, (11, 11), 1.5) - mu12
    ssim_map = ((2 * mu12 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2))
    return np.mean(ssim_map)

#��ȡYUV�ļ�������ת��Ϊnumpy����
def read_yuv_file(filename, width, height):
    with open(filename, 'rb') as f:
        # ��ȡY��U��V����
        Y = np.fromfile(f, dtype=np.uint8, count=width*height).reshape((height, width))
        U = np.fromfile(f, dtype=np.uint8, count=width*height//4).reshape((height//2, width//2))
        V = np.fromfile(f, dtype=np.uint8, count=width*height//4).reshape((height//2, width//2))

        # ��U��V�����ϲ���Ϊ��Y����һ���Ĵ�С
        U = np.repeat(np.repeat(U, 2, axis=0), 2, axis=1)
        V = np.repeat(np.repeat(V, 2, axis=0), 2, axis=1)

        # ת��ΪRGB��ʽ
        YUV = np.dstack((Y, U, V)).astype(np.float32)
        YUV[:,:,1:] -= 128.0
        M = np.array([[1.0, 1.0, 1.0], [0.0, -0.34414, 1.772], [1.402, -0.71414, 0.0]])
        RGB = np.dot(YUV, M.T)
        RGB = np.clip(RGB, 0, 255).astype(np.uint8)
        return RGB[:,:,::-1]  # BGR��ʽ

if __name__ == '__main__':


    # ����������YUV�ļ����ֱ�Ϊfile1.yuv��file2.yuv
    # ��ȡ�����ļ�������PSNR��SSIMֵ
    file_add="D:\\PostgraduateData\\year1 ss\\��ý����뼰����Ϣ��ȫӦ��\\ʵ��\\ʵ��2\\ffmpeg-master-latest-win64-gpl\\bin\\"
    ref = read_yuv_file(file_add+'akiyo_cif.yuv', width=352, height=288)
    file1 = read_yuv_file(file_add+'output_h264_80.yuv', width=352, height=288)
    file2 = read_yuv_file(file_add+'output_h264_160.yuv', width=352, height=288)
    file3 = read_yuv_file(file_add+'output_h264_320.yuv', width=352, height=288)
    file4 = read_yuv_file(file_add+'output_h265_80.yuv', width=352, height=288)
    file5 = read_yuv_file(file_add+'output_h265_160.yuv', width=352, height=288)
    file6 = read_yuv_file(file_add+'output_h265_320.yuv', width=352, height=288)
    #----#
    print("h264,80kbps:")
    psnr = calculate_psnr(ref, file1)
    ssim = calculate_ssim(ref, file1)
    print('PSNR:', psnr)
    print('SSIM:', ssim)
    print("-----------------------------------")

    #----#
    print("h264,160kbps:")
    psnr = calculate_psnr(ref, file2)
    ssim = calculate_ssim(ref, file2)
    print('PSNR:', psnr)
    print('SSIM:', ssim)
    print("-----------------------------------")

    #----#
    print("h264,320kbps:")
    psnr = calculate_psnr(ref, file3)
    ssim = calculate_ssim(ref, file3)
    print('PSNR:', psnr)
    print('SSIM:', ssim)
    print("-----------------------------------")

    #----#
    print("h265,80kbps:")
    psnr = calculate_psnr(ref, file4)
    ssim = calculate_ssim(ref, file4)
    print('PSNR:', psnr)
    print('SSIM:', ssim)
    print("-----------------------------------")

    #----#
    print("h265,160kbps:")
    psnr = calculate_psnr(ref, file5)
    ssim = calculate_ssim(ref, file5)
    print('PSNR:', psnr)
    print('SSIM:', ssim)
    print("-----------------------------------")

    #----#
    print("h265,320kbps:")
    psnr = calculate_psnr(ref, file6)
    ssim = calculate_ssim(ref, file6)
    print('PSNR:', psnr)
    print('SSIM:', ssim)




