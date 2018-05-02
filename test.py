faceList=[[1,False],[55,False],[77,True]]


i=0
while i < len(faceList):
	if(faceList[i][1]==True):
		del faceList[i]
	else:
		i +=1
		print(i)
print(faceList)
