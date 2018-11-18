class Util:
	def writeToFile(self, list, fileName):
		outfile = open(fileName+'.txt', 'w') # open a file in write mode
		for item in list:    # iterate over the list items
		   outfile.write(str(item) + '\n') # write to the file
		outfile.close()   # close the file 