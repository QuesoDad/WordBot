import os
import sys
import subprocess
import textwrap
import sample # BRING IN SAMPLE AND MAKE IT SO YOU CAN GET THE LAST THREE WORDS IN A LOOP

tweetFile = sys.argv[1]

def fileCheck(self):
	statinfo = os.stat(tweetFile)
	tweet = ""
	if statinfo.st_size == 0:
		print('tweetFile is empty.')
		tweet = 'File empty, please try again.'
	else:
		tweet = ""
		#Open the file, grab the first tweet, put it into a variable, remove it from the file, and close the file.
		try:
			tweet_File = open(tweetFile, 'r', encoding='UTF-8')
			while tweet == "": #Do this until the Tweet variable isn't a blank '\n' line or None
				with open(tweetFile, 'r') as fin:
					data = fin.read().splitlines(True) #open the file and stick it in a list
				with open(tweetFile, 'w') as fout: #reopen the file for writing
					i = 0
					for x in data:
						if (i > 0): #If the tweet isn't the first one, write it back to the file
							i =+ 1
							fout.write(x)
						else:
							tweet = x.strip() #If the tweet is the first one, stick it in the tweet variable
							i =+ 1
				fin.close()
				fout.close()
		except IOError:
			tweet_File = open(tweetFile, 'w', encoding='UTF-8')
			tweet = 'tweetFile.txt Created, please place tweets in it separated by \n newlines.'
		tweet_File.close()
	return tweet

def denormalize (tweet):
	tweet_clean = tweet.replace(" . ", ". ").\
						replace(" . . . ", "... ").\
						replace(" \ ? ", "? ").\
						replace(" ! ", "! ").\
						replace(" ' ", "'").\
						replace(" , ", ", ").\
						replace("- -", "--").\
						replace(" ; ", "; ").\
						replace(" # ", " #").\
						replace(" n't", "n't")
	return tweet_clean
	
tweet = fileCheck(tweetFile)
tweet_clean = denormalize(tweet)
print('Normalized tweet: %s'%(tweet_clean))

if len(tweet_clean) > 140: #Saves the parts of tweets over the 140 character limit at the end of the tweetFile for the next batch
	with open(tweetFile, 'a+') as tweetFile:
			cutLines = textwrap.wrap(tweet_clean, 100, break_long_words=False)
			print('The following are the separate tokens')
			print(cutLines)
			y = 0
			for i in cutLines:
				if (y == 0):
					tweet_clean = cutLines[0]
					y =+ 1
				else:
					tweetFile.write(i+ '\n \n')
	tweetFile.close()

finalCharacter = len(tweet_clean) - 1 #Finds final character
finalChar = tweet_clean[finalCharacter]

if finalChar.isalpha() == False and len(tweet_clean) <= 140 and finalChar != ",":
	print('The tweet is less than or equalt to 140 characters and ends with punctuation.'.upper())
	print(tweet_clean)

print(tweet_clean[-1])

tweetList = tweet_clean.split()
print('The last three words are %s %s %s'%(tweetList[-3], tweetList[-2], tweetList[-1]))
last3 = str((tweetList[-3] + tweetList[-2] + tweetList[-1]))

# sample.Sampler('E:\Github\Trump-bot\cv\char-rnn-trained.t7', 1, last3, 15, -1, -1, 1, 1, 0, 0, 0)

if finalChar.isalpha() == True or finalChar == ",":
	print('Tweet doesn\'t end with punctuation'.upper())

#subprocess.check_output(['ls','-l']) #all that is technically needed...
#subprocess.check_output(['python3','tweetReince.py', tweet_clean])

print(tweet_clean)
print(tweet_clean[finalCharacter]) #prints 140 character in string