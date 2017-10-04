import sample
import random


	
#print(lastChar[-1])

while lastChar.isalpha() == True:
	test = '-model word -length 10 -seed '+ str(seed) + ' -primetext ' + primetext
	seed = random.randint(0, 200)
	length = 5
	#length = random.randint(5, 20)
	#seed += 1
	print(seed)
	#print(test)
	
	
	args, arguments = sample.rawParse(test)
	#print(arguments)
	args, training_arguments = sample.parseArguments(args, arguments)
	#print(training_arguments)
	commandstring, commandlist = sample.commandLine()
	#print(commandstring)
	result, samplelist, numSampleList = sample.sample(training_arguments, commandlist)
	result = result.strip()
	#print(type(result))
	
	lastChar = (result.rstrip())[-1]
	#print('Lastchar is ' + lastChar[-1])

print(result)