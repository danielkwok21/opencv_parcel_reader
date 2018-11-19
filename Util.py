import numpy
from matplotlib import pyplot as plt


class Util:
	def writeToFile(self, list, fileName):
		outfile = open(fileName+'.txt', 'w') # open a file in write mode
		for item in list:    # iterate over the list items
		   outfile.write(str(item) + '\n') # write to the file
		outfile.close()   # close the file 

	def getCol(self, list, col_num):
		matrix = numpy.array(list)
		col = matrix.transpose()[col_num][0]
		return col
