import sys
import subprocess
import random
import string

#docker run -v '/dockerdata/:/root/wordbot/dockerdata' -ti kboruff/wordbot bash
#cd dockerdata/wordbot_testing

#Tuples containing setting names, note that additional variables can be added into the training arguments and sample options list and it will update the rest automatically
training_arguments = ('model', 'seed', 'sample', 'prime_text', 'length', 'temperature', 'gpu', 'opencl', 'verbose', 'skip_unk', 'input_loop', 'word_level')
sample_options = (' -seed ', ' -sample ', '-primetext ', ' -length ', ' -temperature ', ' -gpuid', ' -opencl ', ' -verbose ', ' -skip_unk ', ' -input_loop ', ' -word_level ')
max_args = 13
args = len(sys.argv)

def parseArguments (args):
	arguments = []
	if args >= 1:
		print('%s sys args detected'%args)
	if args > max_args:
		'''Truncates args to the maximum arguments possible in sampling'''
		print('Actually, too many arguments detected. Truncating to 12.')
		args = max_args
	if args == 0:
		print('No arguments detected')
	''' Enters commandline arguments into a list'''
	for i in range(args):
		arguments.append(sys.argv[i])
	arguments.remove(sys.argv[0])
	args = len(arguments)
	return args, arguments
	
print(str(parseArguments(args,arguments)))
'''
def commandLine(args)
Prints out a sample command line
	sample_command = 'th sample.lua '
	for i in range(args):
		if i <= 0 and i < len(sample_options):
			sample_command = sample_command + " " + str(arguments[i])
		elif i >= 1 and i <= len(sample_options):
			sample_command = sample_command + " " + sample_options[i-1] + " " + arguments[i]
		else:
			sample_command = sample_command + " " + str(arguments[i])
	return sample_command
'''
'''
def sampler(primetext, length, model = 'word', seed = '123', sample = 1, temperature = 1, gpu = -1, opencl = 0, verbose = 1, skip_unk = 0, input_loop = 0, word_level = 1):
	print(primetext, length, model, seed, sample, temperature, gpu, opencl, verbose, skip_unk, input_loop, word_level)
	
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