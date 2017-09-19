import sys
import os

fileName = sys.argv[1]

def denormalize (text_dirty):
	text_clean = text_dirty.replace(" . ", ". ").\
						replace(" . . . ", "... ").\
						replace(" \ ? ", "? ").\
						replace(" ! ", "! ").\
						replace(" ' ", "'").\
						replace(" , ", ", ").\
						replace("- -", "--").\
						replace(" ; ", "; ").\
						replace(" # ", " #").\
						replace(" n't", "n't")
	return text_clean

def fileCheck(fileName):
	# Checks if a file exists and creates it, if it doesn't
	record = ""
	#Open the file, grab the first record, put it into a variable, remove it from the file, and close the file.
	try:
		record_File = open(fileName, 'r', encoding='UTF-8')
		statinfo = os.stat(fileName)
		print(os.stat(fileName).st_size)
		while record == "" and statinfo.st_size != 0: #Do this until the record variable isn't a blank '\n' line or None and while the file isn't empty
			with open(fileName, 'r') as fin:
				data = fin.read().splitlines(True) #open the file and stick it in a list
			with open(fileName, 'w') as fout: #reopen the file for writing
				i = 0
				for x in data:
					if (i > 0): #If the record isn't the first one, write it back to the file
						i =+ 1
						fout.write(x)
					else:
						record = x.strip() #If the record is the first one, stick it in the record variable
						i =+ 1
			fin.close()
			fout.close()
		if statinfo.st_size == 0:
			print('%s exists, but it is empty.'%(fileName))
	except IOError:
		record_File = open(fileName, 'w', encoding='UTF-8')
		record = '%s Created, please place records in it separated by \n newlines.'%(fileName)
		record_File.close()
	return record
	