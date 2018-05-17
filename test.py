# python3 make_id.py  -f 'da.pickle' -m 'w' -t 'ID.txt'

import pickle
import argparse
import dlib
from skimage import io
from scipy.spatial import distance


ap = argparse.ArgumentParser()
ap.add_argument("-f", "--filefrom",type=str, default="",
	help="использование pi камеры")
ap.add_argument("-t", "--fileto", type=str, default="ID.txt",
	help="выбор файла")
ap.add_argument("-m", "--metod", type=str, default="w",
	help="выбор- открытие файла для чтения, записи, дозаписи")
args = vars(ap.parse_args())


ID=0

with open(args["filefrom"], "rb") as f:
    array_data = []
    try:
        while True:
            array_data.append(pickle.load(f))
    except (EOFError, pickle.UnpicklingError):
        pass

for i in range(len(array_data)):
	print(array_data[i])
	print()
#print(array_data)


mass=[1,2]
print(len(mass))
