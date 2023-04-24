import sys
import subprocess

# Default training arguments
training_arguments = {
    'primetext': "",
    'model': 'char',
    'seed': 123,
    'sample': 1,
    'length': 150,
    'temperature': .4,
    'gpuid': -1,
    'opencl': 0,
    'verbose': 1,
    'skip_unk': 0,
    'input_loop': 0,
    'word_level': 0
}

# Sample options
sample_options = {
    'primetext': '-primetext',
    'model': '-model',
    'seed': '-seed',
    'sample': '-sample',
    'length': '-length',
    'temperature': '-temperature',
    'gpuid': '-gpuid',
    'opencl': '-opencl',
    'verbose': '-verbose',
    'skip_unk': '-skip_unk',
    'input_loop': '-input_loop',
    'word_level': '-word_level'
}

def parse_arguments(arguments):
    """Parse arguments and update training arguments dictionary."""
    for arg in arguments:
        try:
            arg_key, arg_value = arg.split('=')
            arg_key = arg_key.replace('--', '')
            if arg_key in training_arguments:
                training_arguments[arg_key] = arg_value
        except ValueError:
            pass

def main():
    # Parse command line arguments
    parse_arguments(sys.argv[1:])

    # Build the command line
    cmd = ['docker', 'run', '-v', '/dockerdata/:/root/wordbot/dockerdata', '-ti', 'kboruff/wordbot', 'bash']
    cmd += ['cd', 'dockerdata/wordbot_testing']
    for key, value in training_arguments.items():
        cmd += [sample_options[key], str(value)]

    # Run the command line
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print(error)
    else:
        print(output.decode())

def commandLine():
	#Creates a sample.lua ready command line
	if training_arguments['primetext'] == "":
		training_arguments['primetext'] = random.choice(string.ascii_uppercase)
		print(training_arguments['primetext'] + ' is the primetext since one was not provided.')
	if training_arguments['model'] == 'word':
		training_arguments['model'] = 'word-rnn-trained.t7'
		#training_arguments['word_level'] = 1
		#training_arguments['temperature'] = .75
	elif training_arguments['model'] == 'char':
		training_arguments['model'] = 'char-rnn-trained.t7'
	else: # allows for people to submit any model and give it custom options
		pass
	commandstring, delimsample = sample_commandline()
	commandlist = delimsample.split('$$$$####') #make this split everything but the primetext
	return commandstring, commandlist


def sample(training_arguments, commandlist):
	result = ''
	result = subprocess.check_output(commandlist, stderr=None)
	
	samplestring = result.decode('UTF-8')
	result, samplelist, numSampleList = denormalize(samplestring)
	print('Result is ' + result)
	return result, samplelist, numSampleList

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
		replace("  ", " ").\
		replace(" !", "!").\
		replace(" .", ".").\
		replace(" ?", "?").\
		replace(" ? ", "? ").\
		replace(" ! ", "! ").\
		replace(" ' ", "'").\
		replace(" , ", ", ").\
		replace('\"', "").\
		replace("- -", "--").\
		replace(" ; ", "; ").\
		replace('\n\n', '\n').\
		replace('\t', '').\
		replace('\n \n ', "\n").\
		replace(' # ', " #").\
		replace(' 0 ', '0')
	sample_clean = re.sub(r'(?<=\d)\s+(?=\d)', '', sample_clean)
	sample_clean = sample_clean.replace(" n't", "n't")
	sample_clean = sample_clean.rstrip()
	#sample_clean = sample_clean.capitalize()
	samplelist = sample_clean.split('\n')
	samplelist = list(filter(None, samplelist)) #strip blank entries in samplelist
	numSampleList = [(str(i).zfill(6) + ' is ' + samplelist[i].capitalize()) for i in range(len(samplelist))]
	return sample_clean, samplelist, numSampleList

if __name__ == '__main__':
	if len(sys.argv) > 1:
		#print('sys args detected')
		#print(commandlist)
		#print(sample_commandline)
		args, training_arguments = (parseArguments(args, arguments))
		commandstring, commandlist = commandLine()
		result, samplelist, numSampleList = sample(training_arguments, commandlist)
		print(commandstring)
		print(result)
		#print(str(numSampleList[0]))

if __name__ == '__main__':
    main()
