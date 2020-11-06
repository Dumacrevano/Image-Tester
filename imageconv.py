# https://www.freecodecamp.org/news/how-to-build-an-image-type-convertor-in-six-lines-of-python-d63c3c33d1db/
from PIL import Image
import sys


if(len(sys.argv) > 1):
	file = sys.argv[1]
	file_format = sys.argv[2]
else:
	# file = input("Please input file name: ")
	file = "TestpoolOriginal\image24.svg"
	# file_format = input("Please input file type to save as: ")
	file_format = "jpg"
img = Image.open(file)
image_format = img.format.lower()

# print(image_format)
# print(file.replace(image_format.lower(), file_format.lower()))
if image_format.lower() == "jpeg":
	image_format = "jpg"
elif image_format.lower() == "ppm":
	image_format = "pgm"
try:
	if(image_format.lower() == "pgm"):
		img.save(file.lower().replace(image_format.lower(), file_format.lower()))

	elif img.mode != 'RGB':
		rgb_img = img.convert('RGB')
		rgb_img.save(file.lower().replace(image_format.lower(), file_format.lower()))

	else:
		img.save(file.lower().replace(image_format.lower(), file_format.lower()))

except Exception as e:
	print(e)



