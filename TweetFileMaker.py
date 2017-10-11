import os
import sys
import subprocess
import textwrap
import sample
import string
import random

tweet = ''
tweetlength = 0


def parseFile(filename):
	# Checks if a file exists and creates it, if it doesn't
	record = ""
	tweetid = 0
	#Open the file, grab the first record, put it into a variable, remove it from the file, and close the file.
	try:
		record_File = open(filename, 'r', encoding='UTF-8')
		statinfo = os.stat(filename)
		
		with open(filename, 'r') as fin:
			data = fin.read().splitlines(True) #open the file and stick it in a list
					
		with open(outputfilename, 'a+') as fout: #reopen the file for writing
			for x in data:
				tweet = fitTweet(x)
				tweet = cleanTweet(tweet)
				tweet = addHashtag(tweet)
				tweet = cleanTweet(tweet)
				tweetid += 1
				tweet = str(tweetid).zfill(6) + " " + tweet
				fout.write(tweet + '\n')
			fout.close()
			
		fin.close()
		if statinfo.st_size == 0:
			print('%s exists, but it is empty.'%(filename))
	except IOError:
		record_File = open(filename, 'w', encoding='UTF-8')
		record = '%s Created, please place records in it separated by \n newlines.'%(filename)
		record_File.close()
	return record
	
def fitTweet(tweet):
	#reduces the current tweet to less than 140 characters, generates new words from last3 sampling until the tweet is a complete sentence.
	#print('Currently tweet is ' + tweet)
	i=0
	tweetlength = len(tweet)	
	punctuationadded = False
	while tweetlength > 120 or tweetlength < 75 or punctuationadded == False:
		print('NEW TWEET \n \n \nTweet is currently ' + str(len(tweet)) + ' characters long.')
		print('Tweet complete tweet is : ' + tweet)
		if tweetlength > 120:
		#Saves the parts of tweets over 100 characters at the end of the tweet_file
			with open(trimfilename, 'a+') as record_file:
				cut_Lines = textwrap.wrap(tweet, 100, break_long_words=False)
				#print('The following are the separate tokens')
				#print(cut_Lines)
				y = 0
				for i in cut_Lines: #grabs the first line, returns everything else to file
					if (y == 0):
						tweet = cut_Lines[0]
						y =+ 1
					else:
						record_file.write(i+ '\n')
				record_file.close()
			tweetlength = len(tweet)
			print('Tweet is currently ' + str(len(tweet)) + ' characters long.')
			print('Tweet has been trimmed to : ' + tweet)
		#Adds to tweets under 25 characters long
		elif tweetlength < 25: #If the tweet is too short, it will make it longer.
			print(tweet)
			print('Tweet is ' + str(tweetlength) + ' characters. Elongating tweet.')
			tweet = lengthenTweet(tweet, tweetlength).strip()
			tweet = tweet.strip().replace('\n', "")
			tweetlength = len(tweet)
			
		lastChar = (tweet.rstrip()[-1:])
		print('Last char is ' + lastChar + ' and it says (lastChar).isalpha() is '+ str((lastChar).isalpha()))	
		if lastChar == '?' or lastChar == '!' or lastChar == '.' or lastChar == '"':
			print('The tweet ends with some form of punctuation. \n'.upper())
			print(tweet[-1:])
			punctuationadded = True
			return tweet
		elif lastChar != '?' or lastChar != '!' or lastChar != '.' or lastChar != '"':
			print('Tweet doesn\'t end with punctuation, creating new ending'.upper())
			tweetList = tweet.split()
			last3 = str((tweetList[-3] + " " + tweetList[-2] + " " + tweetList[-1])).rstrip()
			tweetlength = len(tweet)
			print('The last three words are %s'%last3)
			tweet = tweet + " " + last3Sample(last3).strip()
			tweet = tweet.strip().replace('\n', "")
			tweetlength = len(tweet)
			print('Tweet with new ending is ' + tweet)
		#print(tweet)
		#tweet = tweet + last3Sample(last3)
	return tweet

def lengthenTweet(tweet, tweetLength):
	''' samples from the entire tweet until it gets a long enough tweet. '''
	arguments = []
	seed = random.randint(0, 200)
	result = 'placeholder'
		
	while tweetLength <= 100:
		print('Tweet too long')
		print('Tweet is ' + tweet + ' and it is ' + str(tweetLength) + ' characters long.')
		tweet = textwrap.wrap(tweet, 120, break_long_words=False)
		tweet = tweet[0]
		lengthTarget = 120 - len(tweet)
		tweetLength = len(tweet)
		command = '-model word -temperature 1 -length 1 -seed '+ str(seed) + ' -primetext ' + tweet
		seed += 1
		args, arguments = sample.rawParse(command)
		args, training_arguments = sample.parseArguments(args, arguments)
		commandstring, commandlist = sample.commandLine()
		result, samplelist, numSampleList = sample.sample(training_arguments, commandlist)
		result = result.strip()
		tweet = tweet + ' ' + result
		print('Tweet is ' + tweet + ' and it is ' + str(tweetLength) + ' characters long.')
	return tweet

def cleanTweet(tweet):
	tweet = tweet.replace('@ ', '#').\
		replace('\n ', '\n').\
		replace(' ? ', '? ').\
		replace(' , ', ', ').\
		replace(' : ', ': ').\
		replace('##', '#').\
		replace(' _ ', '_').\
		strip('\n')
	return tweet

def addHashtag(tweet):
	tweet = tweet.split()
	newTweet = ""
	currentTweetWord = ""
	
	for word in range(len(tweet)): #for each word in tweet
		currentTweetWord = tweet[word]
		print('Working on ' + str(word))
		hashtagged = False
		print(currentTweetWord + ' is ' + str(len(currentTweetWord)) + ' characters long.')
		#print('Full tweet is ' + str(tweet))
		
		firstChar = tweet[word].strip()[0]
		print('The first char in ' + str(tweet[word]) + ' is ' + firstChar)
		
		if len(currentTweetWord) > 7 and firstChar != '#':
			print(currentTweetWord + ' is longer than 7 characters and doesn\'t start with #.')
			hashtagged = bool(random.getrandbits(1))
			print('hashtagged is set to ' + str(hashtagged))
			if hashtagged == True:
				currentTweetWord = '#' + currentTweetWord
				print('Hashtagged ' + currentTweetWord)
		elif firstChar == '#':
			print('Looks like ' + str(tweet[word]) + ' starts with #, already.')
			hashtagged = False
		elif len(tweet[word]) < 7:
			print(tweet[word] + ' is not longer than 7 characters.')
		newTweet = newTweet + " " + currentTweetWord
		print('newTweet is currently + ' + newTweet)
	print(newTweet)
	return newTweet
	
def last3Sample(last3):
	''' samples from the last three words of the text until it gets a punctuation mark '''
	y = 0
	arguments = []
	seed = random.randint(0, 200)
	result = 'placeholder'
	lastChar = (result.rstrip())[-1]
	tweetLength = random.randint(3, 9)
	
	while lastChar.isalpha() == True:
		test = '-model word -wordlevel 1 -temperature 2 -length ' + str(tweetLength) + ' -seed '+ str(seed) + ' -primetext ' + last3
		seed += 1
		args, arguments = sample.rawParse(test)
		args, training_arguments = sample.parseArguments(args, arguments)
		commandstring, commandlist = sample.commandLine()
		result, samplelist, numSampleList = sample.sample(training_arguments, commandlist)
		result = result.strip()
		lastChar = (result.rstrip())[-1]
	return result

if __name__ == '__main__':
	#main is imported by another file
	if len(sys.argv) >= 1:
		tweet_file = sys.argv[1]
		outputfilename = str(tweet_file) + "_output.txt"
		trimfilename = str(tweet_file) + "_trim.txt"
		tweet = parseFile(tweet_file)
		print(tweet)
		print('Final tweet length is ' + str(len(tweet)))
else:
	print('I\'m NOT MAIN')
	if len(sys.argv) >= 1:
		tweet_file = sys.argv[1]
		outputfilename = str(tweet_file) + "_output.txt"
		tweet = fileCheck(tweet_file)
		
		