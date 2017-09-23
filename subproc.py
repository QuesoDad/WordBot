import subprocess

'''
here = ['df', '-h']
print(here)
henry = subprocess.call([here[0], here[1]])
print(henry)
'''

#p = subprocess.Popen(['echo', 'hello world'], stdout=subprocess.PIPE)

#print(p.communicate())

# host = input("Enter a host to ping: ")

command = 'th sample.lua char-rnn-trained.t7 -primetext R -seed 123 -sample 1 -length 150 -temperature 0.4 -gpuid -1 -opencl 0 -verbose 1 -skip_unk 0 -input_loop 0 -word_level 0'
commandlist = command.split()

sample = subprocess.Popen([(commandlist[0]), commandlist[1], commandlist[2], commandlist[3],commandlist[4], commandlist[5], commandlist[6], commandlist[7], commandlist[8], commandlist[9], commandlist[10], commandlist[11], commandlist[12], commandlist[13], commandlist[14], commandlist[15], commandlist[16], commandlist[17], commandlist[18], commandlist[19], commandlist[20], commandlist[21], commandlist[22], commandlist[23], commandlist[24]], stdout=subprocess.PIPE)
print((commandlist[0]), commandlist[1], commandlist[2], commandlist[3],commandlist[4], commandlist[5], commandlist[6], commandlist[7], commandlist[8], commandlist[9], commandlist[10], commandlist[11], commandlist[12], commandlist[13], commandlist[14], commandlist[15], commandlist[16], commandlist[17], commandlist[18], commandlist[19], commandlist[20], commandlist[21], commandlist[22], commandlist[23], commandlist[24])
#p1 = subprocess.Popen(], stdout=subprocess.PIPE)

output = sample.communicate()

print(output)