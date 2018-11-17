class Util:
	def writeToFile(self, list):
		outfile = open('contours.txt', 'w') # open a file in write mode
		for item in list:    # iterate over the list items
		   outfile.write(str(item) + ',') # write to the file
		outfile.close()   # close the file 