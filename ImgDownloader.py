#https://stackoverflow.com/questions/62338957/downloading-random-images-from-google-using-python
# importing google_images_download module
from google_images_download import google_images_download
import urllib.request
import json
import random
import shutil
import os
#Deletes current testpool if exists (restarts image batch)

def downloadimages(file_type,words,response,directory):
    # keywords is the search query
    # format is the image file format
    # limit is the number of images to be downloaded
    # print urs is to print the image file url
    # size is the image size which can
    # be specified manually ("large, medium, icon")
    # aspect ratio denotes the height width ratio
    # of images to download. ("tall, square, wide, panoramic")
    arguments = {
                "keywords": random.choice(words['data']),
                "output_directory": directory,
                "format": file_type,
                "no_directory": True,
                "limit": 50,
                "print_urls": True,
                 }
    try:
        response.download(arguments)

    # Handling File NotFound Error
    except FileNotFoundError:
        arguments = {
                    "keywords": random.choice(words['data']),
                    "format": file_type,
                    "output_directory": "Testpool",
                    "no_directory":True,
                    "limit": 10,
                    "print_urls": True,
                }

        # Providing arguments for the searched query
        try:
            # Downloading the photos based
            # on the given arguments
            response.download(arguments)
        except:
            pass


# Driver Code
def start_download(testpool):
    testpool = testpool
    if (os.path.exists(testpool)):
        shutil.rmtree(testpool)

    corpus_link = "https://www.randomlists.com/data/words.json"
    response = urllib.request.urlopen(corpus_link)
    json_data = response.read().decode()
    words = json.loads(json_data)


    # creating object
    response = google_images_download.googleimagesdownload()


    file_type= [
        "png",
        "gif",
        "jpg",
        "bmp",
        "webp",
        "ico"
    ]

    for type in file_type:
        downloadimages(type,words,response,testpool)
        print()

