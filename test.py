# python3 make_id.py  -f 'da.pickle' -m 'w' -t 'ID.txt'

import pickle
import argparse
import dlib
from skimage import io
from scipy.spatial import distance
import numpy as np
import copy
import time

def index_min(array, n): #массив и номер столбца
    array_new=[]
    for i in range(len(array)):
        array_new.append(array[i][n])
    minimym = min(array_new)
    index=array_new.index(minimym)
    return minimym, index

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--filefrom",type=str, default="",
	help="использование pi камеры")
ap.add_argument("-t", "--fileto", type=str, default="ID.txt",
	help="выбор файла")
ap.add_argument("-m", "--metod", type=str, default="w",
	help="выбор- открытие файла для чтения, записи, дозаписи")
args = vars(ap.parse_args())



faceCount=0
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

i=0
faceList = []

while i < len(array_data):
	
	deltat=[[0]*array_data[i][9]]*len(faceList) 
	for tt in range(len(faceList)):
		for kk in range(array_data[i][9]):
			dt=array_data[i+kk][5]-faceList[tt][5]
			deltat[tt][kk]=dt
	tt=0
	while tt <(len(faceList)):
		n=0
		for kk in range(array_data[i][9]):
			
			if deltat[tt][kk]>2:
				n+=1
		if n==array_data[i][9]:
			del faceList[tt]		
		tt+=1
	

#1
	if(len(faceList) == 0):

		for k in range(array_data[i][9]):
			array_data[i+k][10]=faceCount
			faceList.append(copy.deepcopy(array_data[i+k]))
			faceCount += 1


#2
	if(len(faceList) <= array_data[i][9]):


		metka=[False]*array_data[i][9]

		for f in range(len(faceList)):
			#созаем пустой массив для временной обработки
			rectangle_now=np.zeros((array_data[i][9],3))	
			#перебор всех следующих элементов i-й и все лица что на этом кадре
			for rect in range(array_data[i][9]):
				x2=array_data[i+rect][1]
				y2=array_data[i+rect][2]

				x1=faceList[f][1]
				y1=faceList[f][2]
				dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 )
				
				rectangle_now[rect][0]=x2
				rectangle_now[rect][1]=y2
				rectangle_now[rect][2]=dist
			#поиск минимального расстояния
			minimym, index = index_min(rectangle_now, 2)
			#обновление массива
			metka[index]=True
					
			faceList[f][1]=rectangle_now[index][0]
			faceList[f][2]=rectangle_now[index][1]
			array_data[i+index][10]=faceList[f][10]
			faceList[f][5]=array_data[i+index][5] # обновление времени

		for k in range(array_data[i][9]):
			if (metka[k]==False):
				array_data[i+k][10]=faceCount
				faceList.append(copy.deepcopy(array_data[i+k]))
				faceCount += 1
	
#3
	if(len(faceList) > array_data[i][9]):
		metka=[0]*len(faceList)
		for rect in range(array_data[i][9]):
			rectangle_now=np.zeros((len(faceList),3))
			for f in range(len(faceList)):
		
				x2=array_data[i+f][1]
				y2=array_data[i+f][2]

				x1=faceList[rect][1]
				y1=faceList[rect][2]
				dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 )
				
				rectangle_now[f][0]=x2				
				rectangle_now[f][1]=y2
				rectangle_now[f][2]=dist
			#поиск минимального расстояния
			minimym, index = index_min(rectangle_now, 2)
			#обновление массива
			faceList[rect][1]=rectangle_now[index][0]
			faceList[rect][2]=rectangle_now[index][1]
			faceList[rect][5]=array_data[i+index][5] # обновление времени	
			array_data[i+rect][10]=faceList[index][10]		
			metka[index]=True

		n=0
		while n < len(faceList):
			if(metka[n]==False):
				del faceList[n]
			n+=1
	i+=array_data[i][9]


for i in range(len(array_data)):
	if (i==0):
		array_data[i][0]=0
		ID=ID+1

	if (array_data[i][0]=="none"):
		array_data[i][0]=ID
		ID=ID+1
	
	for k in range(len(array_data)-i-1):
		
		namber_k=array_data[k+i+1][10]
		if (array_data[k+i+1][0]=="none"):
			n_array=[]
			array_namber_k=[]			
			
			for n in range(len(array_data)-i-k-1):
				if (array_data[k+i+n+1][10]==namber_k):
					n_array.append(n)				
					dist=distance.euclidean(array_data[i][6], array_data[k+i+n+1][6])
					array_data[i+k+n+1][8]=dist
					list_1=copy.deepcopy(array_data[k+i+n+1])
					array_namber_k.append(list_1)
			
			#if len(array_namber_k)>0:
			minimym, index = index_min(array_namber_k,8)
			if (minimym<=0.5):
				print('minim',minimym)
				for d in range(len(array_namber_k)):
					#array_data[k+i+1][0]=array_data[i][0]
					array_data[k+i+n_array[d]+1][0]=array_data[i][0]
					print(array_data[k+i+n_array[d]+1][0],i)					
					#array_namber_k[d][0]=array_data[i][0]

for i in range(len(array_data)):
	#проверка на метку
	#метка означает что эта строка уже обработана (по времени)
	if (array_data[i][7]==False):
		#если строка не обработана, то переменной ID_2 присваиваем id этой строки
		ID_2=array_data[i][0]
		array_data[i][7]=True
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

				
				






for i in range(len(array_data)):
	print(array_data[i][0],array_data[i][9],array_data[i][10],array_data[i][5])
#	print(array_data[i+1][5]-array_data[i][5])			
print(len(array_data))

