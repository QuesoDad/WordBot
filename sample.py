
import sys
import subprocess
import random
import string

#docker run -v '/dockerdata/:/root/wordbot/dockerdata' -ti kboruff/wordbot bash
#cd dockerdata/wordbot_testing

#Tuples containing setting names, note that additional variables can be added into the training arguments and sample options list and it will update the rest automatically
training_arguments = {'primetext' : "" , 'model': 'char', 'seed' : 123, 'sample': 1, 'length': 150, 'temperature': .4, 'gpuid': -1, 'opencl': 0, 'verbose': 1, 'skip_unk': 0, 'input_loop' : 0, 'word_level' : 0}
sample_options = (' -primetext', ' -model', ' -seed', ' -sample', ' -length', ' -temperature', ' -gpuid', ' -opencl', ' -verbose', ' -skip_unk', ' -input_loop', ' -word_level')
max_args = len(sample_options)
args = len(sys.argv)
arguments = []
sample_commandline = []

def rawParse (rawinput):
	args = len(rawinput.split())
	tempSplit = rawinput.split()
	for i in range(args):
		arguments.append(tempSplit[i])
	return args, arguments

def parseArguments (args, arguments):
	'''Parses all arguments entered, no matter the argument order, with or without a - delimiter prefixe, and enters all variables into the training_arguments dictionary'''
	if args == 1:
		print('No arguments detected. Defaults chosen')
	if args >= 2:
		''' Enters commandline arguments into a list'''
		try:
			for i in range(args):
				arguments.append(sys.argv[i])
			arguments.remove('sample.py')				
		except:
			pass
		args = len(arguments)
		#print(str(args) + ' arguments detected')		
		valid_argument_counter = 0
		primesequence = ''
		for i in range(args): #for every argument entered
			valid_argument_counter += 1
			if valid_argument_counter < max_args:
				for y in range(max_args): # for every element in the sample options list
					currentDictKey = sample_options[y].replace(' -', "")
					try:
						currentArg = arguments[i].replace(' -', "")
					except:
						break

					#correct commonly forgotten underscores
					if currentArg == 'wordlevel':
						currentArg = 'word_level'
					if currentArg == 'inputloop':
						currentArg = 'input_loop'
					if currentArg == 'skipunk':
						currentArg = 'skip_unk'
					
					#Catch any variable argument names left empty at the end of the string
					if currentArg == currentDictKey:
						try:
							nextArg = arguments[i+1].replace('-', "")
						except:
							print(str('-----------------Last argument is empty, skipping \'%s\'. ----------------'%arguments[i]).upper())
							break
					
					endofprimetext = False
					
					if currentArg != 'primetext' and currentArg == currentDictKey : #Run everything not primetext as a normal command
						#print('Entering ' + nextArg + ' into ' + currentDictKey)
						training_arguments[currentDictKey] = nextArg
						
					elif currentArg == 'primetext':					
						#increment to the next argument, grabbing all prime text until the next word is a default argument
						remainingArgs = args - i
						for t in range(remainingArgs): #t starts at current range of selections after the current selection
							if t > 0 and (i+t) <= args and endofprimetext == False:
								afterPrime = arguments[i+t].replace('-', "")
								#print('Working on ' + str(t+1) + ' argument past primetext, ' + afterPrime + '.')											
								for z in range(max_args):	
									#correct commonly forgotten underscores
									if afterPrime	 == 'wordlevel':
										afterPrime = 'word_level'
									if afterPrime == 'inputloop':
										afterPrime = 'input_loop'
									if afterPrime == 'skipunk':
										afterPrime = 'skip_unk'
									
									testOption = sample_options[z].replace(' -', "")
									if afterPrime == testOption:
										#print('It looks like ' + afterPrime + ' is the next default parameter.')
										#print('Prime text is set to ' + primesequence)
										training_arguments['primetext'] = primesequence
										i += t
										currentArg = arguments[i].replace(' -', "")
										endofprimetext = True
										break
									if z >= max_args -1 and primesequence == "":
										primesequence = afterPrime
									elif z >= max_args -1 and primesequence != "":
										primesequence = primesequence + " " + afterPrime
								#print('Prime sequences is now ' + primesequence)
								primesequence = str(primesequence)
						i += t
						
						training_arguments['primetext'] = '\"' + str(training_arguments['primetext']) + '\"' #Put quotations around the primetext
			else:
				print('Too many arguments. Skipping everything after %s Remember to put \"\" around your primetext'%arguments[i])
				break		
	return args, training_arguments

def sample_commandline():
	
	sample_commandline= 'th sample.lua ' + training_arguments['model']
	
	for i in range(max_args): # go through the proper commandline order, after primetext, and pull the appropriate value from the dictionary
		if sample_options[i].replace(' -', '') == 'model' :
			i += 2
			#skips past model and primetext which are already in the list
			pass
		else:
			sample_commandline = sample_commandline + sample_options[i] + " " + str(training_arguments[sample_options[i].replace(' -', '')])	
	delim_sample_commandline = 'th$$$$####sample.lua$$$$####' + training_arguments['model']
	
	for i in range(max_args): # go through the proper commandline order, adding delimiter $$$$#### into every space between items
		if sample_options[i].replace(' -', '') == 'model' :
			i += 2
			pass
		else:
			delim_sample_commandline = delim_sample_commandline + '$$$$####' + sample_options[i].replace(' ', '') + '$$$$####' + str(training_arguments[sample_options[i].replace(' -', '')])	
	return sample_commandline, delim_sample_commandline

			
def commandLine():
	#Creates a sample.lua ready command line
	if training_arguments['primetext'] == "":
		training_arguments['primetext'] = random.choice(string.ascii_uppercase)
		#print(training_arguments['primetext'] + ' is the primetext since one was not provided.')
	if training_arguments['model'] == 'word':
		training_arguments['model'] = 'word-rnn-trained.t7'
		training_arguments['word_level'] = 1
		training_arguments['temperature'] = .75
	elif training_arguments['model'] == 'char':
		training_arguments['model'] = 'char-rnn-trained.t7'
	else: # allows for people to submit any model and give it custom options
		pass
	commandstring, delimsample = sample_commandline()
	
	commandlist = delimsample.split('$$$$####') #make this split everything but the primetext
	return commandstring, commandlist


def sample(training_arguments, commandlist):
	try :
		result = subprocess.check_output(commandlist, stderr=None)
	except:
		result = ''
	samplestring = result.decode('UTF-8')
	result = denormalize(samplestring)
	return result

# Denormalize sampled text
def denormalize(sample):
	sample_clean = sample
	if training_arguments['model'] == 'char-rnn-trained.t7':
		# Remove extra spacing
		sample_clean = ' '.join([
			word.replace(' ', '')
			for word in sample.split('   ')]).strip()	
#Make conditional to catch "invalid argument:" or /root/torch/install/bin/luajit: sample.lua:165: attempt to index global 'prediction' (a nil value) stack traceback:
	sample_clean = sample_clean.split("--------------------------")[1]
	sample_clean = sample_clean.replace(" . . . ", "... ")
	sample_clean = sample_clean.\
		replace(" . ", ". ").\
		replace(" \ ? ", "? ").\
		replace(" ! ", "! ").\
		replace(" ' ", "'").\
		replace(" , ", ", ").\
		replace("- -", "--").\
		replace(" ; ", "; ").\
		replace('\n\n', '\n').\
		replace('\t', '').\
		replace('\n \n ', "\n")
	sample_clean = sample_clean.replace(" n't", "n't")
	samplelist = sample_clean.split('\n')
	samplelist = list(filter(None, samplelist)) #strip blank entries in samplelist
	for i in range(len(samplelist)):
		print(str(i).zfill(6) + ' is ' + samplelist[i])
	return sample_clean, samplelist

if __name__ == '__main__':
	if len(sys.argv) > 1:
		#print('sys args detected')
		#print(commandlist)
		#print(sample_commandline)
		args, training_arguments = (parseArguments(args, arguments))
		commandstring, commandlist = commandLine()
		sample(training_arguments, commandlist)
		
		
	else:
		args, training_arguments = (parseArguments(args, arguments))
		commandstring, commandlist = commandLine()
		sample(training_arguments, commandlist)
		
		
		
		



