from PIL import Image
from PIL import ImageFile
from pathlib import Path
import cv2

import cv2
from skimage.measure import compare_ssim

def image_feature_compare(imageA,imageB):
    imageA = cv2.imread(imageA)
    imageB = cv2.imread(imageB)
    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")

    # convert similarity percentage into distance between 0 to 100
    dist = abs(score * 100 - 100)
    return dist
#file_signature
file_format = ["50350A", "89504E470D0A1A0A", "FFD8FFE0", "FFD8FFE1", "FFD8FFE8"]

def combine_pairs(img_array):
    hexa_pairs = []
    for i in range(len(img_array)):
        if(i % 2 == 0):
            hexa_pairs.append(img_array[i:i+2])
    return(hexa_pairs)

def signature_decimal(Image1):
    with open(Image1, 'rb') as f:
        content = f.read().hex()
        file_hex = ''
        decimal_values = []
        for i in file_format:
            if(content.find(i.lower()) != -1):
                file_hex = i
        hex_list = list(file_hex)
        combined = combine_pairs(hex_list)
        for y in combined:
            hexa_combined = ''.join(y)
            decimal_conv = int(hexa_combined, 16)
            decimal_values.append(decimal_conv)
        hexsum = sum(decimal_values)/len(decimal_values)
        return hexsum

def signature_difference(Image1, Image2):
    difference = abs(Image1 - Image2)
    if (Image1 > Image2):
        largersize = Image1
    else:
        largersize = Image2
    final_avg = difference / largersize * 100
    return final_avg

def size_difference(Image1, Image2):
    size1 = Path(Image1).stat().st_size
    size2 = Path(Image2).stat().st_size
    difference = abs(size1-size2)
    if (size1 > size2):
        largersize = size1
    else:
        largersize = size2
    final_avg = difference/largersize * 100
    return final_avg

def depth_difference(Image1, Image2):
    mode_to_bpp = {'1': 1, 'L': 8, 'P': 8, 'RGB': 24, 'RGBA': 32, 'CMYK': 32, 'YCbCr': 24, 'I': 32, 'F': 32}
    bpp1 = mode_to_bpp[Image1.mode]
    bpp2 = mode_to_bpp[Image2.mode]
    difference = abs(bpp1-bpp2)
    if (bpp1 > bpp2):
        largersize = bpp1
    else:
        largersize = bpp2
    final_avg = difference/largersize * 100
    return final_avg

def image_dimension_difference(image1,image2):
    im1 = Image.open(image1)
    im2 = Image.open(image2)
    im1_size =  im1.size[0] * im1.size[1]
    im2_size = im2.size[0] * im2.size[1]
    difference = abs(im1_size - im2_size)
    if(im1_size > im2_size):
        largersize = im1_size
    else:
        largersize = im2_size
    final_avg = difference/largersize * 100
    return final_avg

def image_color_avg_rgb(image):
    r = 0
    g = 0
    b = 0
    im = Image.open(image).convert('RGB')
    pixelMap = im.load()
    rgb = []
    img = Image.new( im.mode, im.size)
    for i in range(img.size[0]):
        for j in range(0, img.size[1]):
            rgb_pixel = pixelMap[i,j]
            mapped = [rgb_pixel[0],rgb_pixel[1], rgb_pixel[2]]
            r+=rgb_pixel[0]
            g+=rgb_pixel[1]
            b+=rgb_pixel[2]
            rgb.append(mapped)
    red_average= (r/len(rgb))
    green_average=(g/len(rgb))
    blue_average=(b/len(rgb))
    return red_average,green_average,blue_average


def image_color_difference(image1_RGB,image2_RGB):
    rgb_difference_percentage=[]
    for x in range(3):
        if image1_RGB[x] == image2_RGB[x]:
            rgb_difference_percentage.append(0)
        elif image1_RGB[x] ==0 or image2_RGB[x] == 0:
            rgb_difference_percentage.append(100)
        else:
            big_num = image1_RGB[x] if image1_RGB[x] >= image2_RGB[x] else image2_RGB[x]
            c = (abs(image1_RGB[x] - image2_RGB[x])) / big_num * 100
            rgb_difference_percentage.append(c)
    final_average=sum(rgb_difference_percentage)/len(rgb_difference_percentage)
    return final_average


Image1 = "TestpoolOriginal/image0.jpg"
Image2 = "TestpoolOriginal/image0.jpg"
depth_diff = depth_difference(Image.open(Image1), Image.open(Image2))
size_diff = size_difference(Image1, Image2)
dimen_diff = image_dimension_difference(Image1, Image2)
color_diff = image_color_difference(image_color_avg_rgb(Image1), image_color_avg_rgb(Image2))
sig_diff = signature_difference(signature_decimal(Image1), signature_decimal(Image2))
calc = depth_diff + size_diff + dimen_diff + color_diff + sig_diff
print(calc/5)

#36.4596909457134
