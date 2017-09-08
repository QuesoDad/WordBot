import sys
import subprocess
import random
import string


class Sampler():

    def __init__(self, model_type, maxSample, primeText, length, temperature, gpuid, opencl, verbose, skipUnk, inputLoop, wordLevel, primeText=None,
                 char_temperature=.4, word_temperature=.75):
        # Generate random character for the seed if none provided
        if primeText is None: #If no text is given and the answer is the overloaded one
            primeText = random.choice(string.ascii_uppercase) #returns the ascii uppercase result. Better than .uppercase() because of locale issues
        if primeText[-1:] == ' ': #[-1:] is to make sure it doesn't get an index error from an empty string
            primeTextTrimmed = primeText.strip() + ' ' #makes sure that if the last character is a space, that it's only one space
        else:
            primeTextTrimmed = primeText.strip()
        self.primeText = primeTextTrimmed
        self.char_temperature = char_temperature
        self.word_temperature = word_temperature
''' Sample from Character RNN:

th sample.lua -primetext "Community is " -length 150 -temperature 1 -gpuid -1 -opencl 0 -verbose 1 -skip_unk 0 -input_loop 0 -word_level 0 

Sample from Word RNN:

th sample.lua -primetext "Community is " -length 150 -temperature 1 -gpuid -1 -opencl 0 -verbose 1 -skip_unk 0 -input_loop 0 -word_level 1
'''		
    def get_sample_raw(self, model_type, maxSample, primeText, length, temperature, gpuid, opencl, verbose, skipUnk, inputLoop, wordLevel):
        # Generate random character if none provided
        if primeText is None:
            primeText = random.choice(string.letters).upper()

        # Get model name
        if model_type == 'word':
            model_name = 'dockerdata/word-rnn-trained.t7'
			wordLevel = 1
        elif model_type == 'char':
            model_name = 'dockerdata/char-rnn-trained.t7'
			wordLevel = 0
        else:
            raise ValueError('Model type {} not supported'.format(model_type))

        sample = subprocess.check_output([
        # Sample from the model using provided seed
            'th', 'sample.lua',
            model_name,
			'-sample', str(maxSample),
			'-primetext ', str(primeText),
			'-length ', str(length), 
            '-temperature ', str(temperature),
            '-gpuid ', str(gpuid),
			'-opencl ', str(opencl,
			'-verbose ', str(verbose),
			'-skip_unk ', str(skipUnk),
			'-input_loop ', str(inputLoop),
			'-word_level ', str(wordLevel)
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

if __name__ == '__main__':
    if len(sys.argv) > 1:
        sampler = Sampler(sys.argv[1])
    else:
        sampler = Sampler()
    print sampler.get_sample()
