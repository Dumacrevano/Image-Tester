from RT_Algo import *
from ART_Algo import *

#x = input("enter a number: ")
def algo_comparison(trial_no,filename,testpoolfolder):
	x = trial_no

	# initialize variables
	RT = 0
	RT_first_error = 0
	RT_sum_error = 0

	ART = 0
	ART_first_error = 0
	ART_sum_error = 0

	draw = 0

	for i in range (0,x):
		print("LOOP:", i)
		RT_error, temp = RT_algo(filename,testpoolfolder)
		RT_sum_error += temp

		ART_error, temp = ART_algo(filename,testpoolfolder)
		ART_sum_error += temp

		if(RT_error < ART_error):
			RT += 1
		elif(RT_error > ART_error):
			ART += 1
		else:
			draw += 1
	ART_average = ART_sum_error/trial_no
	RT_average = RT_sum_error/trial_no

	print("RT = " + str(RT))
	print("RT sum errors = " + str(RT_sum_error))
	print("RT average errors = " + str(RT_average))

	print("ART = " + str(ART))
	print("ART sum errors = " + str(ART_sum_error))
	print("ART average errors = " + str(ART_average))

	print("Draw = " + str(draw))
algo_comparison(1, "D:\Education\Semester 6\Software Engineering\SE-Project\Image-Tester/testpool.txt", "D:\Education\Semester 6\Software Engineering\SE-Project\Image-Tester/Testpool")