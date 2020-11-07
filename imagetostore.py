from PIL import Image
from pathlib import Path
import os.path
import re

png_signature = ["89504E470D0A1A0A"]
jpg_signature = ["FFD8FFE0", "FFD8FFE1", "FFD8FFE8"]
pgm_signature = ["50350A", "50320A", "50320D"]
gif_signature = ["47494638"]
svg_signature = ["3C73766720"]
webp_signature = ["52494646"]
ico_signature = ["00000100"]
bmp_signature = ["424D"]
file_format_backup = ["89504E470D0A1A0A","FFD8FFE0", "FFD8FFE1", "FFD8FFE8", "50350A", "50320A", "50320D","47494638", "3C73766720", "00000100", "424D"]
file_format= {'.png': png_signature, '.jpg': jpg_signature, '.jpeg':jpg_signature, ".pgm":pgm_signature, ".gif":gif_signature, ".webp":webp_signature, ".ico":ico_signature, ".bmp":bmp_signature, ".svg":svg_signature}
def combine_pairs(img_array):
    hexa_pairs = []
    for i in range(len(img_array)):
        if(i % 2 == 0):
            hexa_pairs.append(img_array[i:i+2])
    return(hexa_pairs)

def signature_decimal(Image, extension):
    with open(Image, 'rb') as f:
        content = f.read().hex()
        file_hex = "00"
        decimal_values = []
        try: #check signature based on file extension
            for i in file_format[extension]:
                if(content.find(i.lower()) != -1):
                    file_hex = i
        except: #if file extension doesnt exist
            file_hex = "00"
        if(file_hex == "00"): #if no signature detected, recheck the entire signature list
            for i in file_format_backup:
                if(content.find(i.lower()) != -1):
                    file_hex = i
        hex_list = list(file_hex)
        combined = combine_pairs(hex_list)
        #translate hexas into decimals
        for y in combined:
            hexa_combined = ''.join(y)
            decimal_conv = int(hexa_combined, 16)
            decimal_values.append(decimal_conv)
        hexsum = sum(decimal_values)/len(decimal_values)
        return hexsum

def image_color_avg_rgb(image):
    r = 0
    g = 0
    b = 0
    im = image.convert('RGB')
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

def dimension_val(img):
    return img.size[0] * img.size[1]

def depth_val(Images):
    mode_to_bpp = {'1': 1, 'L': 8, 'P': 8, 'RGB': 24, 'RGBA': 32, 'CMYK': 32, 'YCbCr': 24, 'I': 32, 'F': 32}
    bpp = mode_to_bpp[Images.mode]
    return bpp

def size_val(Images):
    size = Path(Images).stat().st_size
    return size

def imagetostore(filename,images,directory):
    #filename="testpool.txt"
    file=open(filename,"r+")
    path = directory
    line_num = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
    file.close()
    #add content
    name = os.path.splitext(images)[0]
    extension = os.path.splitext(images)[1]
    try:
        images_open = Image.open(images)
        r, g, b = image_color_avg_rgb(images_open)
        bit_depth = depth_val(images_open)
        dimension = dimension_val(images_open)
    except:
        try:
            with open(images) as inp:
                data = (inp.read().split('\n'))
                h, w = (data[2].split(' '))
                dimension = int(h) * int(w)
        except:
            dimension = size_val(images) - (size_val(images) % 64)
        r, g, b = 125, 125, 125
        bit_depth = 8
    size = size_val(images)
    sig = round(signature_decimal(images, extension), 8)
    file = open(filename, "a")
    file.write("\n"+str(name)+","+str(r)+","+str(g)+","+str(b)+","+extension+","+str(dimension)+","+str(bit_depth)+","+str(size)+","+str(sig))
    file.close()

    #change counter
    a_file = open(filename, "r")
    list_of_lines = a_file.readlines()
    list_of_lines[0] = (str(line_num)+"\n")
    a_file = open(filename, "w")
    a_file.writelines(list_of_lines)
    a_file.close()


#imagetostore("try.txt","D:\dumac\SEproject\Testpool\image2.pgm")
def store_to_files(directory,filetosave):
    filenames=[]
    directory = directory
    for filename in sorted(os.listdir(directory)):
         filenames.append(filename)

    r = re.compile("(\d+)\.")
    filenames.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
    file = open(filetosave, "r+")
    print(file.readline())
    if os.path.getsize(filetosave) != 0:
        file.truncate(0)
        # file.write("0")

    for filename in filenames:
         path=os.path.join(directory, filename)
         imagetostore(filetosave,path,directory)

