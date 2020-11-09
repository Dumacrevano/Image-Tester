import os
import math
import DistanceCalc
import numpy
from PIL import Image
import shutil
from DataReader import *
import PIL


def RT_algo(filename,testpoolfolder):
    # data pool creation
    data_pool, length = datareader(filename)

    # initialize variables
    trials = 10
    trial_num = 0
    sample_errors = []
    program_name = "imageconv.py"
    resultfolder = "results"
    errorfolder = "errors"
    first_error = math.inf

    # check if results folder exists
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

    while trial_num < trials:
        print("RT Trial " + str(trial_num + 1) + ":")

        potential_candidate = data_pool[numpy.random.randint(0, length)]

        print("Selected Candidate", potential_candidate["Name"]+potential_candidate["Type"])

        filename = potential_candidate["Name"] + potential_candidate["Type"].lower()
        folder_path = '/'.join(testpoolfolder.split('/')[-1:])
        parent_path = '/'.join(os.getcwd().split('\\')[:-1]) + "/"
        trial_num = trial_num + 1
        try:
            # set formats list
            file_formats = ["png", "gif", "jpg", "bmp", "webp", "ico", "pgm"]
            # print("python " + program_name + " " + "\"" + filename + "\" " + "jpg")

            # check current format and update file formats
            if (potential_candidate["Type"].lower() == ".png"):
                cur_format = file_formats.pop(0)

            elif (potential_candidate["Type"].lower() == ".gif"):
                cur_format = file_formats.pop(1)

            elif (potential_candidate["Type"].lower() == ".jpg"):
                cur_format = file_formats.pop(2)

            elif (potential_candidate["Type"].lower() == ".jpeg"):
                cur_format = file_formats.pop(2)

            elif (potential_candidate["Type"].lower() == ".bmp"):
                cur_format = file_formats.pop(3)

            elif (potential_candidate["Type"].lower() == ".webp"):
                cur_format = file_formats.pop(4)

            elif (potential_candidate["Type"].lower() == ".ico"):
                cur_format = file_formats.pop(5)

            elif (potential_candidate["Type"].lower() == ".pgm"):
                cur_format = file_formats.pop(6)

            # convert the file to the other formats
            for i in range(len(file_formats)):
                os.system("python " + program_name + " " + "\"" + filename + "\" " + file_formats[i])
                output_filename = filename.replace(cur_format, file_formats[i])
                img = Image.open(output_filename)
                result_format = img.format
                # print("Output file "+ str(i) + " format is: " + result_format)
                del img
                output_path = '/'.join(output_filename.split('/')[-1:])
                # move file to results folder
                shutil.move(output_filename, parent_path + "comparison/" + output_path.replace(folder_path,
                                                                             resultfolder))  # !!!!! folder name should be LOWERED!!!!
                if (result_format.lower() == "jpeg"):
                    result_format = "jpg"

                elif (result_format.lower() == "ppm"):
                    result_format = "pgm"

                if (result_format.lower() != file_formats[i]):
                    if filename not in sample_errors:
                        sample_errors.append(filename)
                    if (first_error == math.inf):
                        first_error = trial_num
                    print("Error")

        except PermissionError:
            continue
        except FileExistsError:
            continue
        except FileNotFoundError as e:
            print(e)
            if filename not in sample_errors:
                sample_errors.append(filename)
            if (first_error == math.inf):
                first_error = trial_num

        except Exception as e:  # catches other errors
            print(e)
            if os.path.isfile(output_filename):
                try:
                    shutil.move(output_filename, parent_path + "comparison/" + output_path.replace(folder_path,
                                                                             errorfolder))  # place error file into error folder
                except Exception as e:
                    continue

            print("Error in trial:" + str(trial_num))
            if filename not in sample_errors:
                sample_errors.append(filename)
            if (first_error == math.inf):
                first_error = trial_num

    print("Possible errors for:")
    print(sample_errors)
    print("first error found at trial:" + str(first_error))
    return first_error, len(sample_errors)


