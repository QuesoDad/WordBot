import os
import sys
import subprocess
import textwrap
from common import fileCheck, denormalize
import sample
import string
import random

tweet_file = sys.argv[1]
tweet = fileCheck(tweet_file)
tweet_clean = denormalize(tweet)
print('Normalized tweet: %s'%(tweet_clean))

def fitTweet(tweet_clean, tweet_file):
	i=0
	while len(tweet_clean) > 140 or ((tweet_clean[-1:]).isalpha()) == True:
		print('Tweet is currently ' + str(len(tweet_clean)) + ' characters long.')
		if len(tweet_clean) > 140:
		#Saves the parts of tweets over 100 characters at the end of the tweet_file
			original_tweet = 0
			if original_tweet == 1:
				with open(tweet_file, 'a+') as record_file:
					cut_Lines = textwrap.wrap(tweet_clean, 100, break_long_words=False)
					# print('The following are the separate tokens')
					# print(cut_Lines)
					y = 0
					for i in cut_Lines: #grabs the first line, returns everything else to file
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
		y = y + 10
		arguments = []
		seed = ' -seed ' + y
		primetext = ' -primetext ' + last3
		length = ' -length ' + 3
		model = ' -model word'
		temperature = ' -temperature .1'
		arglength = len((seed + primetext + length + model + temperature).split()
		arguments.append(seed, primetext, length, model, temperature)
		newending = sample.parseArguments(10, arguments)
		newtweet = tweet_clean + newending
		
		
		print('last three are: ' + last3)
		#print(sampler.get_sample(last3, y))
		print('the value of y is: ' + str(y))
		
		
		
		
		last3 = sample.parseArguments(3, )
		#print(last3)
		#if (last3[-1:]).isalpha() == True:
		#	last3 = str((tweetList[-3] + " " + tweetList[-2] + " " + tweetList[-1]))
	return last3


print(fitTweet(tweet_clean, tweet_file))