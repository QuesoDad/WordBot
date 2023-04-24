from sample import rawParse, parseArguments, commandLine, sample
import random

def generate_text(primetext, length, seed):
    while primetext[-1].isalpha():
        args, arguments = rawParse(f'-model word -length {length} -seed {seed} -primetext {primetext}')
        args, training_arguments = parseArguments(args, arguments)
        commandstring, commandlist = commandLine()
        result, samplelist, numSampleList = sample(training_arguments, commandlist)
        result = result.strip()
        primetext = result[-length:]
    return result

seed = random.randint(0, 200)
primetext = 'R'
length = 10
result = generate_text(primetext, length, seed)
print(result)
