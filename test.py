import sample

test = 'primetext this is a test of the sampling system. model word seed 123'
arguments = []

arguments = test.split()
args = len(arguments)

args, trainingArguments = parseArguments(args, arguments)
sample_commandline, commandlist = commandLine()
sample(training_arguments)

for i in commandlist:
	print(commandlist[i])