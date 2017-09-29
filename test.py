import sample

test = '-model word -length 70 -seed 69 -wordlevel 1 -primetext test me out'

args, arguments = sample.rawParse(test)
args, training_arguments = sample.parseArguments(args, arguments)
commandstring, commandlist = sample.commandLine()
result = sample.sample(training_arguments, commandlist)
print(result)