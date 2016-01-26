from matplotlib import pyplot as plt

# Ripped straight from patent doc:
#
# pd=pupil diameter of current observation
#
# hor=horizontal coordinate of current observation
#
# vert=vertical coordinate of current observation
#
# dist=distance from eye to screen (only for ASL files)
#
# XDAT=a timing signal sent from the display software to the eye tracker
#
# The XDAT signal can indicate change of display screen, subject keyboard response, or subject mouse response. The use of this variable depends upon the particular material being tracked.
#
# Each of these vectors will be of size (nxl) where n is the number of total observations in the file.



REL_COLS = ["Time", "pd", "hor", "vert", "dist", "XDAT"]

IDF_COL_MAP = {"Time": "Time", "pd": "Mapped Diameter [mm]", "dist": ""}

def getData(file_name)



def getDataIdfTxt(file_name, fields = ["Time", "L Mapped Diameter [mm]", "R Mapped Diameter [mm]"]):
	print ('file name: {}'.format(file_name))
	data = open(file_name, 'r').read()

	data = data.split('\r\n')
	i = 0
	#find the row with the column labels
	while data[i] != "## ":
		i += 1
	field_indexes = [] #this holds the indexes of the columns we care about
	all_fields = data[i+1].split('\t')
	for field in fields:
		field_indexes += [all_fields.index(field)]
	type_index = all_fields.index("Type")
	results = [[] for field in fields]
	for j in range(i+2, len(data)):
		line = data[j].split('\t')
		if len(line) > 1 and line[type_index] == "SMP":
			for k in range(len(field_indexes)):
				results[k] += [line[field_indexes[k]]]
	return results

def plotData(x, *y):
	colors = ["b","g","r","c","m","y","k"]

	plt.xlabel("timestamp")
	plt.ylabel("values")
	for i in range(len(y)):
		plt.plot(x, y[i], colors[i%7])
	plt.show()


if __name__ == "__main__":
	data = getData('samples/atoms28-eye_data Samples.txt')
	plotData(data[0][1:], data[1][1:], data[2][1:])	#note the first observation is probably unreliable. Weird values yo.
	
	# l_zeros = []
	# r_zeros = []
	# for i in range(len(data)):
	# 	if float(data[i][1]) < 1:
	# 		l_zeros += [i]
	# 	if float(data[i][2]) < 1:
	# 		r_zeros += [i]
	# print('l_zeros: {}'.format(l_zeros))
	# print('r_zeros: {}'.format(r_zeros))