import argparse
import textwrap
from common import fileCheck, denormalize
import sample


def fit_tweet(tweet_clean):
    """Takes a tweet string and returns a tweet that is 140 characters or less."""
    while len(tweet_clean) > 140 or tweet_clean[-1:].isalpha():
        print(f'Tweet is currently {len(tweet_clean)} characters long.')

        if len(tweet_clean) > 140:
            # Saves the parts of tweets over 100 characters at the end of the tweet_file
            with open(args.tweet_file, 'a+') as record_file:
                cut_lines = textwrap.wrap(tweet_clean, 100, break_long_words=False)
                tweet_clean = cut_lines[0]
                for line in cut_lines[1:]:
                    record_file.write(line + '\n\n')
            record_file.close()

        if tweet_clean != "":
            # If the file isn't empty, get the last three words
            tweet_list = tweet_clean.split()
            last3 = ' '.join(tweet_list[-3:])

            if last3[-1:].isalpha() or last3[-1:] == ',':
                # Tweet doesn't end with punctuation
                tweet_clean += last3_sample(last3)
            else:
                # Tweet ends with punctuation
                return tweet_clean

    return tweet_clean


def last3_sample(last3):
    """Takes the last three words of a string and samples from them until a punctuation mark is found."""
    y = 0
    while last3[-1:].isalpha():
        y += 10
        seed = f'-seed {y}'
        primetext = f'-primetext {last3}'
        length = '-length 3'
        model = ' -model word'
        temperature = ' -temperature .1'
        arguments = [seed, primetext, length, model, temperature]
        new_ending = sample.sample(arguments)
        tweet_clean += new_ending
        last3 = ' '.join(tweet_clean.split()[-3:])

    return last3


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fit a tweet to 140 characters or less.')
    parser.add_argument('tweet_file', type=str, help='The file containing the tweet.')
    args = parser.parse_args()

    tweet = fileCheck(args.tweet_file)
    tweet_clean = denormalize(tweet)
    print(f'Normalized tweet: {tweet_clean}')
    print(fit_tweet(tweet_clean))
