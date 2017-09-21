import sys
import subprocess
import random
import string

#docker run -v '/dockerdata/:/root/wordbot/dockerdata' -ti kboruff/wordbot bash
#cd dockerdata/wordbot_testing

#Tuples containing setting names, note that additional variables can be added into the training arguments and sample options list and it will update the rest automatically
training_arguments = {'primetext' : "" , 'model': 0, 'seed' : 0, 'sample': 0, 'length': 0, 'temperature': 0, 'gpu': 0, 'opencl': 0, 'verbose': 0, 'skip_unk': 0, 'input_loop' : 0, 'wordlevel' : 0}
sample_options = (' -primetext', ' -model', ' -seed', ' -sample', ' -length', ' -temperature', ' -gpuid', ' -opencl', ' -verbose', ' -skip_unk', ' -input_loop', ' -wordlevel')
max_args = len(sample_options)
args = len(sys.argv)
arguments = []
sample_commandline = []

def parseArguments (args, arguments):

	'''add a step to match -names in the commandline for explicitly given variables here'''
	if args == 1:
		print('No arguments detected. Defaults chosen')
	if args >= 2:
		print('1 or more sys args detected')
	''' Enters commandline arguments into a list'''
	for i in range(args):
		arguments.append(sys.argv[i])
	arguments.remove('sample.py')				
	print(arguments)
	args = len(arguments)
	
	''' loop through every argument, see if it is in the default argument list, then enter it into the correct option in the dictionary, so people have individual non-sequence locked variable flexibility'''
	
	for i in range(len(arguments)): #for every argument entered
		for z in range(max_args):
			for y in range(max_args): # for every element in the sample options list
				if len(arguments) > 0:
					print(str(len(arguments)) + ' remaining.')
					currentOpt = sample_options[y].replace(' -', "")
					if str(arguments[i].replace('-', "")) == currentOpt:
						training_arguments[currentOpt] = arguments[i+1]
						del arguments[i]
						del arguments[i]
					else:
						training_arguments[currentOpt] = arguments[i]
						del arguments[i]

	
	''' correct problem where entering variables like wordlevel first means a bad index range is returned. '''
	
	args = len(arguments)
	
	if args > max_args:
		'''Truncates args to the maximum arguments possible in sampling'''
		print('Actually, too many arguments detected. Truncating to %s.'%max_args)
		args = max_args + 1			
	
	return args, arguments, training_arguments

def commandLine(args, sample_commandline):
	'''Creates a sample.lua ready command line'''
	sample_commandline= 'th sample.lua '
	for i in range(args):
		sample_commandline= sample_commandline+ " " + sample_options[i] + " " + arguments[i]
	return sample_commandline

print(training_arguments.items)

args, arguments, training_arguments = (parseArguments(args, arguments))
print('Current length is %s'%len(arguments))
print(args)
print(commandLine(args,arguments))

''' create an iteration that will fill detected arguments into the default dictionary '''

print(training_arguments.items())


'''
def sample(primetext, length, model = 'word', seed = '123', sample = 1, temperature = 1, gpu = -1, opencl = 0, verbose = 1, skip_unk = 0, input_loop = 0, wordlevel = 1):
	print(primetext, length, model, seed, sample, temperature, gpu, opencl, verbose, skip_unk, input_loop, wordlevel)
	
	if primetext == "":
		primetext = random.choice(string.ascii_uppercase)
		print(primetext)
	
	return None
'''

'''
if __name__ == '__main__':
	if len(sys.argv) > 1:
		print('sys args detected')
		sampler = sampler(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
	else:
		sampler = sampler()
'''

'''
class Sampler():

	def __init__(self, seed_text=None, char_temperature=.4, word_temperature=.75):
		# Generate random character for the seed if none provided
		if seed_text is None:
			seed_text = random.choice(string.ascii_uppercase)
		if seed_text[-1:] == ' ':
			seed_text_trimmed = seed_text.strip() + ' '
		else:
			seed_text_trimmed = seed_text.strip()
		self.seed = seed_text_trimmed
		self.char_temperature = char_temperature
		self.word_temperature = word_temperature

	def get_sample_raw(self, model_type, seed, temperature, length):
		# Generate random character if none provided
		if seed is None:
			seed = random.choice(string.ascii_uppercase)

		# Get model name
		if model_type == 'word':
			model_name = 'lm_lstm_autosave__epoch167.86_3.4929.t7'
		elif model_type == 'char':
			model_name = 'lm_lstm_autosave__epoch167.86_3.4929.t7'
		else:
			raise ValueError('Model type {} not supported'.format(model_type))

		# Sample from the model using provided seed
		sample = subprocess.check_output([
			'th', 'sample.lua',
			model_name,
			'-temperature', str(temperature),
			'-length', str(length),
			'-gpuid', '-1',
			'-primetext', seed
		])

		# Return cleaned sampled text
		return self.denormalize(sample)

	# Denormalize sampled text
	def denormalize(self, sample):
		sample_clean = str(sample).split("--------------------------")[1]
		sample_clean = sample_clean.replace(" . . . ", "... ")
		sample_clean = sample_clean.\
			replace(" . ", ". ").\
			replace(" \ ? ", "? ").\
			replace(" ! ", "! ").\
			replace(" ' ", "'").\
			replace(" , ", ", ").\
			replace("- -", "--").\
			replace(" ; ", "; ")
		sample_clean = sample_clean.replace(" n't", "n't")
		return sample_clean

	# Sample text from model
	def get_sample(self):

		if self.seed.strip()[-1:] != '.':
			# If seed is not a full sentence

			# Sample from character model
			char_sample = self.get_sample_raw(
				'char', self.seed, self.char_temperature, 300)

			# Remove start and end newlines
			char_sample = char_sample.split('\n')[1]

			# Remove extra spacing
			char_sample_clean = ' '.join([
				word.replace(' ', '')
				for word in char_sample.split('   ')]).strip()

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