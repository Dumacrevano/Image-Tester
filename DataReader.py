import os
import math
import DistanceCalc
import numpy
from PIL import Image


with open("testpool.txt") as inp:
    data = (inp.read().split('\n'))
data_pool = []
x = 0
length = 0
for i in data:
    if (x >= 1):
        arr_lines = i.split(',')
        entry = {'Name': arr_lines[0], 'RGB': "("  + arr_lines[1] + ", " + arr_lines[2] +  ", " + arr_lines[3] + ")",  'Type': arr_lines[4], 'Dimension': arr_lines[5],'BitDepth': arr_lines[6], 'Size':arr_lines[7], 'Signature':arr_lines[8]}
        data_pool.append(entry)
    else:
        length = int(i)
    x += 1

# initialize variables
tested_pictures = []
trials = 10
trial_num = 1
tested_pictures.append(data_pool[0])
number_of_candidate = 3
candidates = []
sample_errors = []
program_name = "imageconv.py"
resultfolder = "results"

# check if results folder exists
if not os.path.exists(resultfolder):
    # create folder
    os.mkdir(resultfolder)

while trial_num < trials:
    print("Trial " + str(trial_num + 1) + ":")

    for i in range(number_of_candidate):
        candidates.append(data_pool[numpy.random.randint(0, length)])

    # initialize variables
    potential_candidate = ""
    min_dist = math.inf
    max_dist = -math.inf

    # loop through candidates to find ideal candidate
    for i in candidates:
        # reset min distance
        min_dist = math.inf
        imageB = i["Name"]+i["Type"]
        imageBRGB = eval(i["RGB"])
        imageBDimension = i["Dimension"]
        imageBBitDepth = i["BitDepth"]
        imageBSize = i['Size']
        imageBSignature = i['Signature']
        # print("Image B", imageB)
        # loop through previous images and compare distance to find min distance
        for j in tested_pictures:
            imageA = j["Name"]+j["Type"]
            # print("Image A", imageA)
            imageARGB = eval(j["RGB"])
            imageADimension = j["Dimension"]
            imageABitDepth = j["BitDepth"]
            imageASize = j['Size']
            imageASignature = j['Signature']
            color_dist = DistanceCalc.image_color_difference(imageARGB, imageBRGB)
            dimen_dist = DistanceCalc.feature_difference(imageADimension, imageBDimension)
            bitdept_dist = DistanceCalc.feature_difference(imageABitDepth, imageBBitDepth)
            size_dist = DistanceCalc.feature_difference(imageASize, imageBSize)
            signature_dist = DistanceCalc.feature_difference(imageASignature, imageBSignature)
            dist = (color_dist + dimen_dist + bitdept_dist + size_dist + signature_dist)/5
            # print("ImageA",imageA, "ImageB", imageB, "Distance", dist)
            # compare distance between candidate and previous points
            if dist < min_dist:
                min_dist = dist
            # print("min dist: " + str(min_dist))
            del imageA


        # compare distance between candidate to find max distance
        if min_dist > max_dist:
            potential_candidate = i
            max_dist = min_dist
        del imageB
        # print("max dist: " + str(max_dist))
        # print("\n")


    print("Selected Candidate", potential_candidate["Name"]+potential_candidate["Type"])
    tested_pictures.append(potential_candidate)
    filename = potential_candidate["Name"] + potential_candidate["Type"]
    try:
        # set formats list
        file_formats = ["png", "jpg", "pgm"]
        # print("python " + program_name + " " + "\"" + filename + "\" " + "jpg")

        # check current format and update file formats
        if(potential_candidate["Type"] == ".png"):

            cur_format = file_formats.pop(0)
        elif(potential_candidate["Type"] == ".jpg"):
            cur_format = file_formats.pop(1)

        else:
            cur_format = file_formats.pop(2)

        # convert the file to the two other formats
        os.system("python " + program_name + " " + "\"" + filename + "\" " + file_formats[0])
        output_filename1 = filename.replace(cur_format, file_formats[0])
        os.system("python " + program_name + " " + "\"" + filename + "\" " + file_formats[1])
        output_filename2 = filename.replace(cur_format, file_formats[1])

        # open first file and check format
        img = Image.open(output_filename1)
        result_format = img.format
        print("Output file 1 format is: " + result_format)
        del img

        # move file 1 to results folder
        os.rename(output_filename1, output_filename1.replace("Testpool", resultfolder))

        if (result_format.lower() == "jpeg"):
            result_format = "jpg"

        if (result_format.lower() == "ppm"):
            result_format = "pgm"

        if (result_format.lower() != file_formats[0]):
            sample_errors.append(filename)

        # open file 2 and check format
        img = Image.open(output_filename2)
        result_format = img.format
        print("Output file 2 format is: " + result_format)
        del img

        # move file 2 to results folder
        os.rename(output_filename2, output_filename2.replace("Testpool", resultfolder))

        if (result_format.lower() == "jpeg"):
            result_format = "jpg"

        if (result_format.lower() == "ppm"):
            result_format = "pgm"

        if (result_format.lower() != file_formats[1]):
            sample_errors.append(filename)

    except Exception as e:
        print(e)
        print("Error in trial:" + str(trial_num))
        sample_errors.append(filename)
    trial_num = trial_num + 1
print("Possible errors for:")
print(sample_errors)
