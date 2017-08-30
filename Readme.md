# Word Bot
_Word bot_ simplifies training of corpus texts on Windows and other Docker friendly environments through shared folders. This is primarily based off all the hard work of rtlee9 using [word-level RNN](https://github.com/larspars/word-rnn) and [pre-trained](http://nlp.stanford.edu/projects/glove/) GloVe  word vectors. For more information see the original project this is forked from. For additional insight into what is occuring in this program, please see [this](https://eightportions.com/2016-11-03-Trump-bot/) Eight Portions blog post.


## Usage: training

1. Install Docker Tools for Windows.

* Pull docker image: `docker pull rtlee/t-bot:train`
* Run docker container: `docker run -t -i rtlee/t-bot:train /bin/bash`
* Update the git repo: `git pull origin master`
* Train models
	* Modify training scripts as necessary: `train_char.sh` and `train_word.sh`
	* Run training scripts: `./train_char.sh` and `./train_word.sh`
* Identify the best word and character level models and move to `/cv/`, replacing the existing files corresponding to the appropriate model type
* Sample from models: `python sample.py "I will build a"`


## Usage: sampling


* Pull docker image: `docker pull rtlee/t-bot:sample`
* Run docker container: `docker run -t -i rtlee/t-bot:sample /bin/bash`
* Update the git repo: `git pull origin master`
* Sample from models: `python sample.py "I will build a"`



## Credits, inspiration and similar projects
This is a fork of Lars Hiller Eidnes' [word-rnn](https://github.com/larspars/word-rnn), which is based on Andrej Karpathy's [char-rnn](https://github.com/karpathy/char-rnn).

* [Auto-Generating Clickbait With Recurrent Neural Networks](https://larseidnes.com/2015/10/13/auto-generating-clickbait-with-recurrent-neural-networks/)
* [DeepDrumpf: Twitterbot](https://www.csail.mit.edu/deepdrumpf)
* [RoboTrumpDNN: Generating Donald Trump Speeches with Word2Vec and LSTM](https://github.com/ppramesi/RoboTrumpDNN)
