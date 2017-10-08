import os
import sys
import subprocess
import textwrap
import sample
import string
import random

tweet = ''
tweetlength = 0

def fileCheck(filename):
	# Checks if a file exists and creates it, if it doesn't
	record = ""
	#Open the file, grab the first record, put it into a variable, remove it from the file, and close the file.
	try:
		record_File = open(filename, 'r', encoding='UTF-8')
		statinfo = os.stat(filename)
		while record == "" and statinfo.st_size != 0: #Do this until the record variable isn't a blank '\n' line or None and while the file isn't empty
			with open(filename, 'r') as fin:
				data = fin.read().splitlines(True) #open the file and stick it in a list
			with open(filename, 'w') as fout: #reopen the file for writing
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
			print('%s exists, but it is empty.'%(filename))
	except IOError:
		record_File = open(filename, 'w', encoding='UTF-8')
		record = '%s Created, please place records in it separated by \n newlines.'%(filename)
		record_File.close()
	return record

def parseFile(filename):
	# Checks if a file exists and creates it, if it doesn't
	record = ""
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
				fout.write(tweet + '\n \n')
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
	while tweetlength > 120 or tweetlength < 75 or ((tweet[-1:]).isalpha()) == True:
		#print('Tweet is currently ' + str(len(tweet)) + ' characters long.')
		if tweetlength > 120:
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
			tweetlength = len(tweet)
			#print('Tweet is currently ' + str(len(tweet)) + ' characters long.')
			#print('Tweet is currently : ' + tweet)
		if str((tweet[-1:])).isalpha() == False and (((tweet[-1:]) != ",") or ((tweet[-1:]) != "'") or ((tweet[-1:]) != "@") or ((tweet[-1:]) != "#")):
			print('The tweet ends with punctuation. \n'.upper())
			return tweet
		if tweet != "":#If the file isn't empty, get the last three words
			tweetList = tweet.split()
			last3 = str((tweetList[-3] + " " + tweetList[-2] + " " + tweetList[-1])).rstrip()
			tweetlength = len(tweet)
			print('The last three words are %s'%last3)
		if (tweet[-1:]).isalpha() == True or ((tweet[-1:]) == ","):
			print('Tweet doesn\'t end with punctuation, creating new ending'.upper())
			tweet = tweet + " " + last3Sample(last3).strip()
			tweet = tweet.strip().replace('\n', "")
			tweetlength = len(tweet)
		if tweetlength < 75: #If the tweet is too short, it will make it longer.
			print(tweet)
			print('Tweet is ' + str(tweetlength) + ' characters. Elongating tweet.')
			tweet = lengthenTweet(tweet, tweetlength).strip()
			tweet = tweet.strip().replace('\n', "")
			tweetlength = len(tweet)
		
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
		command = '-model word -temperature 2 -length 1 -seed '+ str(seed) + ' -primetext ' + tweet
		seed += 1
		args, arguments = sample.rawParse(command)
		args, training_arguments = sample.parseArguments(args, arguments)
		commandstring, commandlist = sample.commandLine()
		result, samplelist, numSampleList = sample.sample(training_arguments, commandlist)
		result = result.strip()
		tweet = tweet + ' ' + result
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
	taggedTweetWord = ""
	
	for i in range(len(tweet)):
		hashtagged = False
		
		#print(tweet[i] + ' is ' + str(len(tweet[i])))
		for item in tweet:
			firstChar = item.strip()[0]
			print(firstChar)
			
		if len(tweet[i]) > 7 and firstChar != '#':
			hashtagged = bool(random.getrandbits(1))
		
		if hashtagged == True:
			taggedTweetWord = '#' + str(tweet[i])
			print('Hashtagged ' + taggedTweetWord)
		elif firstChar == '#':
			taggedTweetWord = tweet[i]
			print('We can\'t hashtag ' + taggedTweetWord)
		else:
			taggedTweetWord = tweet[i]
		newTweet = newTweet + " " + taggedTweetWord
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
		tweet = fileCheck(tweet_file)
		tweet = parseFile(tweet_file)
		print(tweet)
		print('Final tweet length is ' + str(len(tweet)))
else:
	print('I\'m NOT MAIN')
	if len(sys.argv) >= 1:
		tweet_file = sys.argv[1]
		outputfilename = str(tweet_file) + "_output.txt"
		tweet = fileCheck(tweet_file)
		
		