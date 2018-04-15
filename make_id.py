import pickle
import dlib
from skimage import io
from scipy.spatial import distance

ID=0

with open("da.pickle", "rb") as f:
    array_data = []
    try:
        while True:
            array_data.append(pickle.load(f))
    except (EOFError, pickle.UnpicklingError):
        pass

print(array_data)

for i in range(len(array_data)):
	if (i==0):
		array_data[i][1]=0
		ID=ID+1

	if (array_data[i][1]=="none"):
		array_data[i][1]=ID
		ID=ID+1
	print('i= ',i)
	for k in range(len(array_data)-i-1):
		if (array_data[k+i+1][1]=="none"):
			dist=distance.euclidean(array_data[i][4], array_data[k+i+1][4])
			array_data[i+k+1][5]=dist
			print (dist)
			
			print()
			if (dist<=0.5 	):
				array_data[k+i+1][1]=array_data[i][1]
				print('ID',array_data[k+i+1][1])


for i in range(len(array_data)):
	print()
	print(array_data[i])
