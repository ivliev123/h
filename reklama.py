
#python3 reklama.py  -d 'da.pickle' -w 'ab'


from skimage import io
from imutils.video import VideoStream
from imutils import face_utils
from scipy.spatial import distance
import numpy as np
import datetime
import argparse
import imutils
import time
import dlib
import cv2
import datetime
import pickle



parser = argparse.ArgumentParser()

parser.add_argument('-d', action="store", dest="doc")
parser.add_argument('-w', action="store", dest="write")
args = parser.parse_args()

print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')  


def get_face_descriptor(imge):    # from image
    img = io.imread(imge)
    dets = detector(img, 1)
    for k, d in enumerate(dets):
        shape = predictor(img, d)
    face_descriptor = facerec.compute_face_descriptor(img, shape)
    return face_descriptor

def index_min(array, n): #массив и номер столбца
    array_new=[]
    for i in range(len(array)):
        array_new.append(array[i][n-1])
    minimym = min(array_new)
    index=array_new.index(minimym)
    return minimym, index


def rect_to_bb(rect):
	x = rect.left()
	y = rect.top()
	w = rect.right() - x
	h = rect.bottom() - y

	return (x, y, w, h)

def add_in_new(a):
	new_array=[a[0],"none",a[8],a[9],a[12],0,False]
	return new_array

#a = face_base.a

faceList_all=[]

#в этот массив будет записываться база лиц за все время
faceList=[]

#создаем пременную в которую будет записываться количество человек посмотревших, это число будет обновлться каждые сутки
faceCount=0


#for i in range(len(a)):
#    a[i][2]=get_face_descriptor(a[i][1])



#запуск камеры
print("[INFO] camera sensor warming up...")
vs = VideoStream(0).start()
time.sleep(2.0)

while True:
	frame = vs.read() 
	frame = imutils.resize(frame, width=600)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
	#определяем лица в видеопотоке
	rects = detector(gray, 0)
	#print(len(rects))
	#Сценарий 1
	if(len(faceList) == 0):
		#для каждого лица выполняем следующие действия 
		for rect in rects:
			
			shape_cam = predictor(gray, rect)
			shape = face_utils.shape_to_np(shape_cam)
			face_descriptor= facerec.compute_face_descriptor(frame, shape_cam)
        
			(x, y, w, h) = face_utils.rect_to_bb(rect)
			print("+++ В кадре детектировано новое лицо " +  str(faceCount))
			
			start =str( datetime.datetime.now())
			finish = 0
			facedata=[faceCount, x, y, w, h, True, False, 40, start , finish, False,False, face_descriptor,0 ]
			
			faceList.append(facedata)

			#facedata_all=add_in_new(facedata)
			
			#faceList_all.append(facedata_all)

			faceCount=faceCount+1


	#Сценарий 2
	if(len(faceList)<=len(rects)):
		used=np.zeros(len(rects), dtype=bool)
		j=0
		for f in range(len(faceList)):

			i=0
			rectangle_now=np.zeros((len(rects),6))
			for rect in rects:
				(x1, y1, w1, h1) = face_utils.rect_to_bb(rect)
				x2=faceList[j][1]
				y2=faceList[j][2]
				dist = np.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
				d=dist
				rectangle_now[i][0]=x1
				rectangle_now[i][1]=y1
				rectangle_now[i][2]=w1
				rectangle_now[i][3]=h1
				rectangle_now[i][4]=d
				i=i+1
			#поиск минимального расстояния
			minimym, index = index_min(rectangle_now, 5)
			#обновление массива
			faceList[j][1]=rectangle_now[index][0]
			faceList[j][2]=rectangle_now[index][1]
			faceList[j][3]=rectangle_now[index][2]
			faceList[j][4]=rectangle_now[index][3]
			faceList[j][7]=40
			#помечаем что квадрат с таким номеров обработке и добавления в базу не нуждается
			used[j]=True
			j=j+1		
	
		i=0
		for rect2 in rects:
			if (not used[i]):
				shape_cam = predictor(gray, rect2)
				shape = face_utils.shape_to_np(shape_cam)
        			
				face_descriptor= facerec.compute_face_descriptor(frame, shape_cam)
				
				(x, y, w, h) = face_utils.rect_to_bb(rect2)
				print("+++ В кадре детектировано новое лицо "  	 +  str(faceCount))
				
				start =str( datetime.datetime.now())
				#finish = 0
				facedata=[faceCount, x, y, w, h, True, False, 30, start , finish, False,False, face_descriptor, 0 ]

				faceList.append(facedata)
	
				#facedata_all=add_in_new(facedata)

				faceCount=faceCount+1
			i=i+1



	#Cценарий 3
	else:
		#метка разрешающая изменение
		
		for f1 in range(len(faceList)):
			faceList[f1][5] = True
		i=0
		for rect3 in rects:
			j=0
			faceList_now=np.zeros((len(faceList),6))
			for f in range(len(faceList)):
				(x1, y1, w1, h1) = face_utils.rect_to_bb(rect3)
				x2=faceList[i][1]
				y2=faceList[i][2]
				dist = np.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
				d=dist
				
				faceList_now[j][0]=x1
				faceList_now[j][1]=y1
				faceList_now[j][2]=w1
				faceList_now[j][3]=h1
				faceList_now[j][4]=d
				j=j+1	
			#поиск минимального расстояния
			minimym, index = index_min(faceList_now, 5)
			#обновление массива
			faceList[i][1]=faceList_now[index][0]
			faceList[i][2]=faceList_now[index][1]
			faceList[i][3]=faceList_now[index][2]
			faceList[i][4]=faceList_now[index][3]
			faceList[i][7]=40
			
			#метка запрещающая изменения, объект подтвержден что он на экране
			faceList[i][5] = False
			i=i+1

		
		#подготавливаем объект к удалению
		i=0
		for fd in range(len(faceList)):
			if (faceList[i][5] != False):
				faceList[i][7]=faceList[i][7]-1
				if (faceList[i][7]<0):
					finish=str(datetime.datetime.now())
					faceList[i][9]=finish
					facedata_all=add_in_new(faceList[i])
					#faceList_all.append(facedata_all)

					#открываем файл на дозапись
					with open(args.doc, args.write) as f:
						pickle.dump(facedata_all, f)
					faceList[i][6]=True
			i=i+1
		#print(faceList)

	i=0
	for fdel in range(len(faceList) ):
		if (faceList[i][6]==True):
			del faceList[i]
		i=i+1
			
	i=0
	for rec in range(len(faceList)):
		xr = int(faceList[i][1])
		yr = int(faceList[i][2])
		wr = int(faceList[i][3])
		hr = int(faceList[i][4])
		cv2.rectangle(frame, (xr, yr), (xr + wr, yr + hr), (0, 255, 0), 2)
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(frame,str(faceList[i][0]),(xr,yr), font, 1,(255,0,0),1,cv2.LINE_AA)
		i=i+1


	cv2.imshow("Frame", frame)


	key = cv2.waitKey(1) & 0xFF
    
    # if the `q` key was pressed, break from the loop
	if key == ord("q"):
		#print()
		#print(faceList_all)
		break
        # do a bit of cleanup
		cv2.destroyAllWindows()
		vs.stop()
