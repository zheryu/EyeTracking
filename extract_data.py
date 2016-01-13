def getData(file_name, fields = ["Time", "L Mapped Diameter [mm]", "R Mapped Diameter [mm]"]):
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
	results = []
	for j in range(i+2, len(data)):
		line = data[j].split('\t')
		if len(line) > 1 and line[type_index] == "SMP":
			results += [[line[x] for x in field_indexes]]
	return results






if __name__ == "__main__":
	print(getData('samples/atoms28-eye_data Samples.txt')[:5])