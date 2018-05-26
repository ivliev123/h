# python3 make_id1.py  -f 'da.pickle' -m 'w' -t 'ID.txt'

import pickle
import argparse
import dlib
from skimage import io
from scipy.spatial import distance
import time
import datetime

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--filefrom",type=str, default="",
	help="использование pi камеры")
ap.add_argument("-t", "--fileto", type=str, default="ID.txt",
	help="выбор файла")
ap.add_argument("-m", "--metod", type=str, default="w",
	help="выбор- открытие файла для чтения, записи, дозаписи")
args = vars(ap.parse_args())


#кончный масив с конечной обработаной информацией
array_finish_list=[]

ID=0

with open(args["filefrom"], "rb") as f:
    array_data = []
    try:
        while True:
            array_data.append(pickle.load(f))
    except (EOFError, pickle.UnpicklingError):
        pass

#print(array_data)

for i in range(len(array_data)):
	if (i==0):
		array_data[i][0]=0
		ID=ID+1



	for k in range(len(array_data)-i-1):

		if (array_data[k+i+1][0]=="none"):
			dist=distance.euclidean(array_data[i][6], array_data[k+i+1][6])
			array_data[i+k+1][8]=dist

			
			if (dist<=0.5 	):
				array_data[k+i+1][0]=array_data[i][0]
				#print('ID',array_data[k+i+1][0])
	if (array_data[i][0]=="none"):
		array_data[i][0]=ID
		ID=ID+1

print(i)				
				

for i in range(len(array_data)):
	#проверка на метку
	#метка означает что эта строка уже обработана (по времени)
	if (array_data[i][7]==False):
		#если строка не обработана, то переменной ID_2 присваиваем id этой строки
		ID_2=array_data[i][0]
		array_data[i][7]==True
		print('ID===========',ID_2)

		mass=[]
		mass.append(array_data[i])
		#далее производим обработку всех строк, которые не обработаны и имеют такой же ID
		for k in range(len(array_data)-i-1):
			#проверка на метку и соответствие сторк i и i+k+1 на id
			if (array_data[k+i+1][7]==False) and (array_data[k+i+1][0]==ID_2):
				mass.append(array_data[k+i+1])
				if (mass[len(mass)-1][5]-mass[len(mass)-2][5]< 2):
					#print(mass[len(mass)-1][5]-mass[len(mass)-2][5])
					#ставим метку что строка обработана
					array_data[k+i+1][7]=True
					#print(len(mass))
				else:
					mass.pop()
				

		if len(mass)>0:
			finish=mass[len(mass)-1][5]+1
			finish=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(finish))
			array_f=mass
			array_f[0][5]=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(array_f[0][5]))
			array_f[0][7]=finish
			array_f[0][6]=len(mass)
			array_finish_list.append(array_f[0])

				
				


				
for l in  range(len(array_finish_list)):
	print()
	print(array_finish_list[l])

print(len(array_data))
d = open(args["fileto"], args["metod"])
for i in range(len(array_finish_list)):
	s= str(array_finish_list[i][0]) +"  "+ str(array_finish_list[i][5]) +"  " + str(array_finish_list[i][7]) 
	d.write(s+ '\n')

d.close()
