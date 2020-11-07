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

def feature_difference(Image1, Image2):
    Image1 = float(Image1)
    Image2 = float(Image2)
    difference = abs(Image1-Image2)
    if (Image1 > Image2):
        largersize = Image1
    else:
        largersize = Image2
    try:
        final_avg = difference/largersize * 100
    except ZeroDivisionError:
        final_avg = 0
    return final_avg