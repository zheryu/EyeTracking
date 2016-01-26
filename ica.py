import matplotlib.plot as plt

IDF_TXT_COLS = {
	"right": {
		"XDAT": "Time", "pd": "L Mapped Diameter [mm]", "hor": "R EPOS X", "vert": "R EPOS Y", "dist": "R EPOS Z"
	},
	"left": {
		"XDAT": "Time", "pd": "R Mapped Diameter [mm]", "hor": "L EPOS X", "vert": "L EPOS Y", "dist": "L EPOS Z"
	}
}
class Sample:
    def __init__(self, left_eye, right_eye):
        self.left = left_eye
        self.right = right_eye

class SampleEye:
    def __init__(self, pd, hor, vert, dist, XDAT):
		# data matrix is Nx6, composed of... (as rows)
        # pd=pupil diameter of current observation
        # hor=horizontal coordinate of current observation
        # vert=vertical coordinate of current observation
        # dist=distance from eye to screen (only for ASL files)
        # XDAT=a timing signal sent from the display software to the eye tracker
		# The XDAT signal can indicate change of display screen, subject keyboard response, or subject mouse response. The use of this variable depends upon the particular material being tracked.
        self.pd = pd
        self.hor = hor
        self.vert = vert
        self.dist = dist
        self.XDAT = XDAT




#this method ideally should have a little more case checking for different file types. But then again, I don't know what those files are
def extract_data(file_name):
    return getDataIdfTxt(file_name)



def clean():
    print("We're terribly sorry, but data cleaning isn't implemented yet. Operation skipped...")
    #print('cleaning data...				', end="")
    #print('[DONE]')
    return




IDF_TXT_COLS = {
	"right": {
		"XDAT": "Time", "pd": "L Mapped Diameter [mm]", "hor": "R EPOS X", "vert": "R EPOS Y", "dist": "R EPOS Z"
	},
	"left": {
		"XDAT": "Time", "pd": "R Mapped Diameter [mm]", "hor": "L EPOS X", "vert": "L EPOS Y", "dist": "L EPOS Z"
	}
}

def getDataIdfTxt(file_name, fields = ["Time", "L Mapped Diameter [mm]", "R Mapped Diameter [mm]"]):
    print('extracting data from {}...			'.format(file_name), end="")
    data = open(file_name, 'r').read()

    data = data.split('\r\n')
    i = 0
	#find the row with the column labels
    while data[i] != "## ":
        i += 1
	r_pd = []
	r_hor = []
	r_vert = []
	r_dist = []
	r_XDAT = []
	l_pd = []
	l_hor = []
	l_vert = []
	l_dist = []
	l_XDAT = []


	all_fields = data[i+1].split('\t')
	l_indexes = {val: all_fields.index(val) for val in IDF_TXT_COLS["left"].values()}
	r_indexes = {val: all_fields.index(val) for val in IDF_TXT_COLS["right"].values()}

	type_index = all_fields.index("Type")
	for j in range(i+2, len(data)):
		line = data[j].split('\t')
		if len(line) > 1 and line[type_index] == "SMP":
			r_pd += [r_indexes[IDF_TXT_COLS["right"]["pd"]]]
			r_hor += [r_indexes[IDF_TXT_COLS["right"]["hor"]]]
			r_vert += [r_indexes[IDF_TXT_COLS["right"]["vert"]]]
			r_dist += [r_indexes[IDF_TXT_COLS["right"]["dist"]]]
			r_XDAT += [r_indexes[IDF_TXT_COLS["right"]["XDAT"]]]
			l_pd += [l_indexes[IDF_TXT_COLS["left"]["pd"]]]
			l_hor += [l_indexes[IDF_TXT_COLS["left"]["hor"]]]
			l_vert += [l_indexes[IDF_TXT_COLS["left"]["vert"]]]
			l_dist += [l_indexes[IDF_TXT_COLS["left"]["dist"]]]
			l_XDAT += [l_indexes[IDF_TXT_COLS["left"]["XDAT"]]]

	left = SampleEye(l_pd, l_hor, l_vert, l_dist, l_XDAT)
	right = SampleEye(r_pd, r_hor, r_vert, r_dist, r_XDAT)

	print('[DONE]')
	return Sample(left, right)

def plotData(x, *y):
	colors = ["b","g","r","c","m","y","k"]

	plt.xlabel("timestamp")
	plt.ylabel("values")
	for i in range(len(y)):
		plt.plot(x, y[i], colors[i%7])
	plt.show()


if __name__ == "__main__":
	data = extract_data('samples/atoms28-eye_data Samples.txt')
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