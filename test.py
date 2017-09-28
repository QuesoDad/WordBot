import sample

test = 'primetext \"test me out\" model word'

args, arguments = sample.rawParse(test)
args, training_arguments = sample.parseArguments(args, arguments)
commandstring, commandlist = sample.commandLine()
result = sample.sample(training_arguments, commandlist)