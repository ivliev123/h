import numpy as np
a=[1,1,1,5,5,5,5,6,6,6,55,55,5,55,55,555,55,55,55,55]
bc = np.bincount(a)
x= bc.argmax()
print(x)
print(a[2])
