arr = [[1, 2], [6, 7], [5, 6], [7, 8], [6, 7], [5, 6], [7, 8]]
area_arr = [2685721.0, 43449.5, 30452.0, 27034.5, 25995.5, 22223.0, 20987.5, 
18276.0, 12237.5, 12134.5, 10784.0, 8160.5, 6135.0, 5879.0, 5659.5, 5614.0, 
5154.0, 5081.0, 4941.0, 4859.5, 4702.0, 4544.0, 4439.5, 4387.5, 4280.5, 4257.0, 
3885.5, 3779.5, 3164.5, 2483.5, 2423.5, 2378.0, 2360.5, 1928.0, 1902.0, 1699.5]

def getIQ(arr, range):
	if not len(arr)%2:
		# even
		return (arr[(len(arr)/4*range)-1] + arr[len(arr)/4*range])/2.0
	else:
		# odd
		return arr[(len(arr)/4*range)]

def removeOutliers(arr):
	median = getIQ(arr, 2)
	IQ1 = getIQ(arr, 1)
	IQ3 = getIQ(arr, 3)
	IQR = IQ3 - IQ1
	lower_limit = IQ1 - IQR
	upper_limit = IQ3 + IQR

	for a in arr:
		if a<lower_limit or a>upper_limit:
			arr.remove(a)

	return arr

def isOutlier(d, arr):
	arr.sort()
	median = getIQ(arr, 2)
	IQ1 = getIQ(arr, 1)
	IQ3 = getIQ(arr, 3)
	IQR = IQ3 - IQ1
	lower_limit = IQ1 - IQR
	upper_limit = IQ3 + IQR

	print 'IQ3: ',IQ3
	print 'IQ1: ',IQ1

	return d<lower_limit or d>upper_limit

def getArea(d):
	return d[0]*d[1]

print 'area_arr:', len(area_arr)
print 'area_arr:'

print filter(lambda a: isOutlier(a, area_arr), area_arr)