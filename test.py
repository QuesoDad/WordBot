import sample

test = '"test me out"'

args, arguments = sample.rawParse(test)
args, training_arguments = sample.parseArguments(args, arguments)
commandstring, commandlist = sample.commandLine()
result = sample.sample(training_arguments, commandlist)