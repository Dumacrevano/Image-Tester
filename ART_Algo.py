import os
import math
import DistanceCalc
import numpy
from PIL import Image
import shutil
from DataReader import *
import PIL
import time

def ART_algo(trialno,filename,testpoolfolder,root,treev, variable, bar, style):
    # data pool creation
    data_pool, length = datareader(filename)

    # initialize variables
    tested_pictures = []
    trials = trialno
    bar["maximum"] = trials
    trial_num = 1
    tested_pictures.append(data_pool[0])
    number_of_candidate = 3
    candidates = []
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
        print("Trial " + str(trial_num + 1) + ":")
        if(trial_num == 0):
            potential_candidate = data_pool[numpy.random.randint(0, length)]
            
        else:
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
        trial_num = trial_num + 1
        variable.set(trial_num)
        bar['value'] = trial_num
        style.configure('text.Horizontal.TProgressbar',text='Trial No: {0}/{1}'.format(trial_num, trials))
        time.sleep(0.02)
        root.update_idletasks()
        filename = potential_candidate["Name"] + potential_candidate["Type"]

        try:
            # set formats list
            file_formats = ["png", "gif", "jpg", "bmp", "webp", "ico", "pgm"]
            # print("python " + program_name + " " + "\"" + filename + "\" " + "jpg")

            # check current format and update file formats
            if(potential_candidate["Type"].lower() == ".png"):
                cur_format = file_formats.pop(0)

            elif(potential_candidate["Type"].lower() == ".gif"):
                cur_format = file_formats.pop(1)

            elif(potential_candidate["Type"].lower() == ".jpg"):
                cur_format = file_formats.pop(2)

            elif(potential_candidate["Type"].lower() == ".bmp"):
                cur_format = file_formats.pop(3)

            elif(potential_candidate["Type"].lower() == ".webp"):
                cur_format = file_formats.pop(4)

            elif(potential_candidate["Type"].lower() == ".ico"):
                cur_format = file_formats.pop(5)

            elif(potential_candidate["Type"].lower() == ".pgm"):
                cur_format = file_formats.pop(6)

            # convert the file to the other formats
            for i in range(len(file_formats)):
                os.system("python " + program_name + " " + "\"" + filename + "\" " + file_formats[i])
                output_filename = filename.lower().replace(cur_format, file_formats[i])
                img = Image.open(output_filename)
                result_format = img.format
                # print("Output file "+ str(i) + " format is: " + result_format)
                del img

                # move file to results folder
                os.rename(output_filename, output_filename.replace(testpoolfolder.lower(), resultfolder))  # !!!!! folder name should be LOWERED!!!!

                if (result_format.lower() == "jpeg"):
                   result_format = "jpg"

                elif (result_format.lower() == "ppm"):
                   result_format = "pgm"

                if (result_format.lower() != file_formats[i]):
                    sample_errors.append(filename)
                    if (first_error == math.inf):
                        first_error = trial_num
                    print("Error")
                    treev.insert("", 'end', text="L1", values=(filename, "Conversion Error from"+potential_candidate['Type']+" to "+result_format))

        except PermissionError:
            continue
        except FileExistsError:
            continue
        except FileNotFoundError as e:
            print(e)
            sample_errors.append(filename)
            if (first_error == math.inf):
                first_error = trial_num
            treev.insert("", 'end', text="L1",values=(filename, e))
            root.update_idletasks()
        except Exception as e:  # catches other errors
            print(e)
            if os.path.isfile(output_filename):
                os.rename(output_filename, output_filename.replace(testpoolfolder.lower(),
                                                                   errorfolder))  # place error file into error folder
            print("Error in trial:" + str(trial_num))
            sample_errors.append(filename)
            if (first_error == math.inf):
                first_error = trial_num
            treev.insert("", 'end', text="L1",
                         values=(filename, e))
            root.update_idletasks()


    print("Possible errors for:")
    print(sample_errors)
    print("first error found at trial:" + str(first_error))
    return first_error, len(sample_errors)

