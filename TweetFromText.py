import os
import sys
import subprocess
import textwrap
from common import fileCheck, denormalize
import sample
import string
import random

print(random.choice(string.ascii_uppercase))

sampler = sample.Sampler()
tweet_file = sys.argv[1]

tweet = fileCheck(tweet_file)
tweet_clean = denormalize(tweet)
print('Normalized tweet: %s'%(tweet_clean))

print(((tweet_clean[-1:]).isalpha() == True))
print((tweet_clean[-1:]))
print(len(tweet_clean))

def fitTweet(tweet_clean, tweet_file):
	i=0
	while len(tweet_clean) > 140 or ((tweet_clean[-1:]).isalpha()) == True:
		if len(tweet_clean) > 140:
		#Saves the parts of tweets over 100 characters at the end of the tweet_file
			original_tweet = 0
			if original_tweet == 1:
				with open(tweet_file, 'a+') as record_file:
					cut_Lines = textwrap.wrap(tweet_clean, 100, break_long_words=False)
					# print('The following are the separate tokens')
					# print(cut_Lines)
					y = 0
					for i in cut_Lines:
						if (y == 0):
							tweet_clean = cut_Lines[0]
							y =+ 1
						else:
							record_file.write(i+ '\n \n')
				record_file.close()
			cut_Lines = textwrap.wrap(tweet_clean, 100, break_long_words=False)
			tweet_clean = cut_Lines[0]
			original_tweet =+1
		
		if str((tweet_clean[-1:])).isalpha() == False and ((tweet_clean[-1:]) != ","):
			print('The tweet ends with punctuation. \n'.upper())
			return tweet_clean
			
		if tweet_clean != "":#If the file isn't empty, get the last three words
			tweetList = tweet_clean.split()
			last3 = str((tweetList[-3] + " " + tweetList[-2] + " " + tweetList[-1]))
			print('The last three words are %s.'%last3)

		if (tweet_clean[-1:]).isalpha() == True or ((tweet_clean[-1:]) == ","):
			print('Tweet doesn\'t end with punctuation'.upper())
			tweet_clean = tweet_clean + last3Sample(last3)
		print(tweet_clean)
		
		tweet_clean = tweet_clean + last3Sample(last3)
	return tweet_clean

def last3Sample(last3):
	''' samples from the last three words of the text until it gets a punctuation mark '''
	y = 0
	while (last3[-1:]).isalpha() == True:
		y = y + 1
		print('test here')
		#print('last three are: ' + last3)
		print(sampler.get_sample(last3, y))
		print('the value of y is: ' + str(y))
		#last3 = sampler.get_sample_raw('char', last3, y, 3)
		#print(last3)
		#if (last3[-1:]).isalpha() == True:
		#	last3 = str((tweetList[-3] + " " + tweetList[-2] + " " + tweetList[-1]))
	return last3

	#subprocess.check_output(['ls','-l']) #all that is technically needed...


print(fitTweet(tweet_clean, tweet_file))