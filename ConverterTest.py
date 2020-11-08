import os
from PIL import Image
import shutil
sample_errors = []
resultfolder = "results"
errorfolder = "errors"
program_name = "imageconv.py"
potential_candidate = ".png"

if os.path.exists(resultfolder):
    #delete folder contents if exists
    shutil.rmtree(resultfolder)
if not os.path.exists(resultfolder):
    # create folder
    os.mkdir(resultfolder)

if os.path.exists(errorfolder):
    # delete folder contents if exists
    shutil.rmtree(errorfolder)
if not os.path.exists(errorfolder):
    # create folder
    os.mkdir(errorfolder)

filename = "D:/Education/Semester 6/Software Engineering/SE-Project/Image-Tester/Testpool\image39.png"

try:
    # set formats list
    file_formats = ["png", "gif", "jpg", "bmp", "webp", "ico", "pgm"]
    # print("python " + program_name + " " + "\"" + filename + "\" " + "jpg")

    # check current format and update file formats
    if (potential_candidate.lower() == ".png"):
        cur_format = file_formats.pop(0)

    elif (potential_candidate.lower() == ".gif"):
        cur_format = file_formats.pop(1)

    elif (potential_candidate.lower() == ".jpg"):
        cur_format = file_formats.pop(2)

    elif (potential_candidate.lower() == ".bmp"):
        cur_format = file_formats.pop(3)

    elif (potential_candidate.lower() == ".webp"):
        cur_format = file_formats.pop(4)

    elif (potential_candidate.lower() == ".ico"):
        cur_format = file_formats.pop(5)

    elif (potential_candidate.lower() == ".pgm"):
        cur_format = file_formats.pop(6)

    # convert the file to the other formats
    for i in range(len(file_formats)):
        os.system("python " + program_name + " " + "\"" + filename + "\" " + file_formats[i])
        output_filename = filename.lower().replace(cur_format, file_formats[i])
        img = Image.open(output_filename)
        result_format = img.format
        print("Output file " + str(i) + " format is: " + result_format)
        del img

        # move file to results folder
        os.rename(output_filename, output_filename.replace("Testpool".lower(),
                                                           resultfolder))  # !!!!! folder name should be LOWERED!!!!

        if (result_format.lower() == "jpeg"):
            result_format = "jpg"

except FileExistsError:
    pass
except FileNotFoundError as e:
    print(e)
    sample_errors.append(filename)
except Exception as e:  # catches other errors
    print(e)
    if os.path.isfile(output_filename):
        os.rename(output_filename, output_filename.replace("TestPool".lower(),
                                                           errorfolder))  # place error file into error folder
