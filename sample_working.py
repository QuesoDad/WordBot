import sys
import subprocess
import random
import string
import re

#docker run -v '/dockerdata/:/root/wordbot/dockerdata' -ti kboruff/wordbot bash
#cd dockerdata/wordbot_testing

#Tuples containing setting names, note that additional variables can be added into the training arguments and sample options list and it will update the rest automatically
training_arguments = {'primetext' : "" , 'model': 'char', 'seed' : 123, 'sample': 1, 'length': 150, 'temperature': .4, 'gpuid': -1, 'opencl': 0, 'verbose': 1, 'skip_unk': 0, 'input_loop' : 0, 'word_level' : 0}
sample_options = (' -primetext', ' -model', ' -seed', ' -sample', ' -length', ' -temperature', ' -gpuid', ' -opencl', ' -verbose', ' -skip_unk', ' -input_loop', ' -word_level')
max_args = len(sample_options)
args = len(sys.argv)
arguments = []
sample_commandline = []

def parseArguments (args, arguments):
	'''Parses all arguments entered taking into consideration "-" prefixes and enters all variables into the training_arguments dictionary overwriting defaults'''
	if args == 1:
		print('No arguments detected. Defaults chosen')
	if args >= 2:
		print('1 or more arguments detected')
		''' Enters commandline arguments into a list'''
		for i in range(args):
			arguments.append(sys.argv[i])
		arguments.remove('sample.py')				
		args = len(arguments)
		''' Take variables if they are given out of order or if only one variable in the defaults is supposed to be changed'''
		valid_argument_counter = 0
		for i in range(args): #for every argument entered
			valid_argument_counter += 1
			if valid_argument_counter < max_args:
				#print('valid_argument_counter is at %s'%valid_argument_counter)
				#print('checking %s'%arguments[i].replace('-', ""))
				for y in range(max_args): # for every element in the sample options list
					if len(arguments) > 0:
						#print('len(arguments) is now %s'%len(arguments))
						#print('check if ' + arguments[i].replace('-', "") + ' is equal to ' + sample_options[y].replace(' -', ""))
						if arguments[i].replace('-', "") == sample_options[y].replace(' -', ""):
							#print('Match found!')
							currentDictKey = sample_options[y].replace(' -', "")
							try:
								finalword = arguments[i+1]
								# print('entering %s'%arguments[i+1] + ' into ' + currentDictKey)
								isfinalword = False
								#print('Not the last word')
							except: 
								isfinalword = True
								# print('the last word')
								break
							if isfinalword != True:
								training_arguments[currentDictKey] = arguments[i+1] #take the next word in the sequence and add it to the training arguments dictionary as the currently option being checked
							#print('i is' + str(i))
							i += 1
							#print('i is' + str(i))
						#elif arguments[i].replace('-', "") != sample_options[y].replace(' -', ""):
							#print(arguments[i].replace('-', "") + ' is not accompanied by a proper argument. Proper arguments are \n')
							#for z in range(len(sample_options)):
							#	print('\r ' + sample_options[z])
							#currentDictKey = sample_options[y].replace(' -', "")
							#training_arguments[currentDictKey] = arguments[i]					
					else:
						print('Too many arguments. Skipping %s'%arguments[i])
			else:
				print('No more arguments')
	return args, training_arguments

def commandLine():
	'''Creates a sample.lua ready command line'''
	if training_arguments['primetext'] == "":
		training_arguments['primetext'] = random.choice(string.ascii_uppercase)
		#print(training_arguments['primetext'] + ' is the primetext since one was not provided.')
	if training_arguments['model'] == 'word':
		training_arguments['model'] = 'word-rnn-trained.t7'
		training_arguments['word_level'] = 1
		training_arguments['temperature'] = .75
		#print(training_arguments['model'] + ' is the selected model. Word_level is set to ' + str(training_arguments['word_level']) + ".")
	elif training_arguments['model'] == 'char':
		training_arguments['model'] = 'char-rnn-trained.t7'
		#print(training_arguments['model'] + ' is the selected model.')
	else: # allows for people to submit any model and give it custom options
		#print(training_arguments['model'] + ' is the selected model.')
		pass
		
	sample_commandline= 'th sample.lua ' + training_arguments['model']
	#print(training_arguments)
	for i in range(max_args): # go through the proper commandline order and pull the appropriate value from the dictionary
		if sample_options[i].replace(' -', '') == 'model' :
			i += 2
			#print('skip')
			pass
		else:
			sample_commandline = sample_commandline + sample_options[i] + " " + str(training_arguments[sample_options[i].replace(' -', '')])
	commandlist = sample_commandline.split()
	#print(commandlist)
	return sample_commandline, commandlist

def sample(training_arguments):
	#print('Submitting command')
	result = subprocess.Popen([(commandlist[0]), commandlist[1], commandlist[2], commandlist[3],commandlist[4], commandlist[5], commandlist[6], commandlist[7], commandlist[8], commandlist[9], commandlist[10], commandlist[11], commandlist[12], commandlist[13], commandlist[14], commandlist[15], commandlist[16], commandlist[17], commandlist[18], commandlist[19], commandlist[20], commandlist[21], commandlist[22], commandlist[23], commandlist[24]], stdout=subprocess.PIPE)
	#print('requesting result')
	sample = result.communicate()
	#sample = result.stdout.readline()
	#print('Printing out result:')
	result = str(sample[0].decode('utf-8'))
	result = denormalize(result)
	print(result)
	return result

# Denormalize sampled text
def denormalize(sample):
	sample_clean = sample
	if training_arguments['model'] == 'char-rnn-trained.t7':
		# Remove extra spacing
		sample_clean = ' '.join([
			word.replace(' ', '')
			for word in sample.split('   ')]).strip()
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
		replace('\n \n ', "\n")
	sample_clean = sample_clean.replace(" n't", "n't")
	samplelist = sample_clean.split('\n').decode('utf-8')
	print('Sample list is ' + str(samplelist))
	return sample_clean, samplelist


if __name__ == '__main__':
	if len(sys.argv) > 1:
		#print('sys args detected')
		#print(commandlist)
		#print(sample_commandline)
		args, training_arguments = (parseArguments(args, arguments))
		sample_commandline, commandlist = commandLine()
		sample(training_arguments)
		
	else:
		args, training_arguments = (parseArguments(args, arguments))
		sample_commandline, commandlist = commandLine()
		sample(training_arguments)



'''
class Sampler():

		Sample from the model using provided seed
		sample = subprocess.check_output(['th', 'sample.lua',model_name,'-temperature', str(temperature),'-length', str(length),'-gpuid', '-1','-primetext', seed])
		# Return cleaned sampled text
		denormalize(sample)


	# Sample text from model
	def get_sample(self):

		if self.seed.strip()[-1:] != '.':
			# If seed is not a full sentence

			# Sample from character model
			char_sample = self.get_sample_raw(
				'char', self.seed, self.char_temperature, 300)

			

			

			# Preserve initial spacing if relevant
			if char_sample[0] != char_sample_clean[0]:
				char_sample_clean = ' ' + char_sample_clean.strip()
			else:
				char_sample_clean = char_sample_clean.strip()

			# Take only the first sentence from the char-level sample
			sample_starter = self.seed + \
				char_sample_clean.split('.')[0] + '.'

		else:
			# Seed is a full sentence, so skip char-level model
			sample_starter = self.seed

		# Sample from the word-level model
		word_sample = self.get_sample_raw(
			'word', sample_starter, self.word_temperature, 500)

		# Join char-level sample with word-level sample
		sample_clean = sample_starter + ' ' + word_sample

		return ' '.join(sample_clean.split())


	#print sampler.get_sample()
'''