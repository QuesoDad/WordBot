import subprocess

command = 'th sample.lua char-rnn-trained.t7 -primetext R -seed 123 -sample 1 -length 150 -temperature 0.4 -gpuid -1 -opencl 0 -verbose 1 -skip_unk 0 -input_loop 0 -word_level 0'

result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)

print(result.stdout)
