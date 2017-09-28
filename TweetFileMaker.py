import os
import sys
import subprocess
import textwrap
import sample
import string
import random


def fileCheck(fileName):
	# Checks if a file exists and creates it, if it doesn't
	record = ""
	#Open the file, grab the first record, put it into a variable, remove it from the file, and close the file.
	try:
		record_File = open(fileName, 'r', encoding='UTF-8')
		statinfo = os.stat(fileName)
		while record == "" and statinfo.st_size != 0: #Do this until the record variable isn't a blank '\n' line or None and while the file isn't empty
			with open(fileName, 'r') as fin:
				data = fin.read().splitlines(True) #open the file and stick it in a list
			with open(fileName, 'w') as fout: #reopen the file for writing
				i = 0
				for x in data:
					if (i > 0): #If the record isn't the first one, write it back to the file
						i =+ 1
						fout.write(x)
					else:
						record = x.strip() #If the record is the first one, stick it in the record variable
						i =+ 1
			fin.close()
			fout.close()
		if statinfo.st_size == 0:
			print('%s exists, but it is empty.'%(fileName))
	except IOError:
		record_File = open(fileName, 'w', encoding='UTF-8')
		record = '%s Created, please place records in it separated by \n newlines.'%(fileName)
		record_File.close()
	return record

def fitTweet(tweet):
	#reduces the current tweet to less than 140 characters, generates new words from last3 sampling until the tweet is a complete sentence.
	i=0
	while len(tweet) > 140 or ((tweet[-1:]).isalpha()) == True:
		print('Tweet is currently ' + str(len(tweet)) + ' characters long.')
		if len(tweet) > 140:
		#Saves the parts of tweets over 100 characters at the end of the tweet_file
			with open(tweet_file, 'a+') as record_file:
				cut_Lines = textwrap.wrap(tweet, 100, break_long_words=False)
				# print('The following are the separate tokens')
				# print(cut_Lines)
				y = 0
				for i in cut_Lines: #grabs the first line, returns everything else to file
					if (y == 0):
						tweet = cut_Lines[0]
						y =+ 1
					else:
						record_file.write(i+ '\n \n')
				record_file.close()
			cut_Lines = textwrap.wrap(tweet, 100, break_long_words=False)
			tweet = cut_Lines[0]
			print('Tweet is currently ' + str(len(tweet)) + ' characters long.')
			print('Tweet is currently : ' + tweet)

		if str((tweet[-1:])).isalpha() == False and ((tweet[-1:]) != ","):
			print('The tweet ends with punctuation. \n'.upper())
			return tweet
			
		if tweet != "":#If the file isn't empty, get the last three words
			tweetList = tweet.split()
			last3 = str((tweetList[-3] + " " + tweetList[-2] + " " + tweetList[-1]))
			print('The last three words are %s'%last3)

		if (tweet[-1:]).isalpha() == True or ((tweet[-1:]) == ","):
			print('Tweet doesn\'t end with punctuation, creating new ending'.upper())
			tweet = tweet + last3Sample(last3)
		print(tweet)
		
		tweet = tweet + last3Sample(last3)
	return tweet

def last3Sample(last3):
	''' samples from the last three words of the text until it gets a punctuation mark '''
	y = 0
	print('Does last3args end with a punctuation?')
	while (last3[-1:]).isalpha() == True:
		print('last3 doesn\'t end with a punctuation')
		y = y + 10
		print(str(y))
		arguments = []
		seed = ' seed ' + str(y)
		primetext = ' primetext "' + str(last3) + '\"'
		length = ' length 3'
		model = ' model word'
		temperature = ' temperature 2'
		wordlevel = 'wordlevel turcky butt'
		last3args = primetext + length + model + seed + temperature + wordlevel
		print('Last three args = ' + last3args)
		args, arguments = sample.rawParse(last3args)
		args, training_arguments = sample.parseArguments(args, arguments)
		commandstring, commandlist = sample.commandLine()
		print(str(commandstring))
		newending = str(sample.sample(training_arguments, commandlist))
		newtweet = tweet + newending
		print('The new tweet is ' + str(newtweet))
		print('last three are now: ' + last3)
		#print(sampler.get_sample(last3, y))
		#print('the value of y is: ' + str(y))
		if (newtweet[-1:]).isalpha() == True:
			last3 = newtweet
	return last3




if __name__ == '__main__':
	if len(sys.argv) >= 1:
		tweet_file = sys.argv[1]
		tweet = fileCheck(tweet_file)
		tweet = fitTweet(tweet)
		#print(tweet)
else:
	if len(sys.argv) >= 1:
		tweet_file = sys.argv[1]
		tweet = fileCheck(tweet_file)
		