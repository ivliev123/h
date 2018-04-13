import dlib
from skimage import io
from scipy.spatial import distance
import cv2
import pickle


def get_face_descriptor(imge):    # from image
    img = io.imread(imge)
    dets = detector(img, 1)
    for k, d in enumerate(dets):
        shape = predictor(img, d)
    face_descriptor = facerec.compute_face_descriptor(img, shape)
    return face_descriptor


print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')    

a=[]


face_descriptor1=get_face_descriptor('Ивлиев_Е_А.jpg')
face_descriptor2=get_face_descriptor('Ивлиев_В_А.jpg')

a.append(face_descriptor1)
a.append(face_descriptor2)

#print(face_descriptor1)
print(a)

with open('data.pickle', 'ab') as f:
	pickle.dump(a, f)

#temp_lst = [1,2,3,4,5]
#global_lst = []

#for i in range(4):
#    global_lst.append(temp_lst)

#f = open('test.txt', 'w') #аттрибут a - будет открывать файл на дозапись, w - на перезапись
#f.write(str(face_descriptor1))
#f.close()
