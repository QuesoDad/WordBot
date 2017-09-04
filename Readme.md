# Word Bot
_Word bot_ simplifies training of corpus texts on Windows and keeps most database files in an easy to access shared folders. This is primarily based off all the hard work of rtlee9 using [word-level RNN](https://github.com/larspars/word-rnn) and [pre-trained](http://nlp.stanford.edu/projects/glove/) GloVe  word vectors. For more information see the original project this is forked from. For additional insight into what is occuring in this program, please see [this](https://eightportions.com/2016-11-03-Trump-bot/) Eight Portions blog post.


## Usage: training

1. Install Docker Tools for Windows.
2. Make a "/dockerdata" directory to use for holding the training files and corpus text files
3. Open Oracle VirtualBox (Installed with Docker Toolbox)
4. Make sure the "default" Virtual machine Docker installs is turned off
5. Go to the "default" machines Settings | Shared Folders
6. Add the "/dockerdata" directory as a shared named dockerdata. Set to automount and Full access.

7. Run the following commands from Docker Quick Start Terminal:

* docker-machine ssh default
* sudo mkdir /dockerdata
* sudo mount -t vboxsf /dockerdata /dockerdata
* Type "exit" and hit enter

The second /dockerdata in this line is for the local directory.

8. From the Docker Quick Start Terminal run: docker pull kboruff/wordbot
9. After download, run docker run -v '/dockerdata/:/root/wordbot/dockerdata' -ti kboruff/wordbot bash

10. Run "ls"

If everything went correctly, you should be in the /root/wordbot folder and a /dockerdata folder should be visible. A placeholder file named input.txt should be in the /root directory. To make sure everything is setup properly, we will move it into the dockerdata folder.

11. Run "mv ./input.txt ~/wordbot/dockerdata"

11. CD into the /dockerdata folder and run "ls" again.

12. You should see the input.txt file.

13. On the host system, go to the Dockerdata folder you made and you should see the input.txt file in it.

14. From Docker, run ./train_char.sh or ./train_word.sh

These will check if the GloVe pre-trained files have been downloaded already. If not, it downloads them into the /dockerdata folder /glove

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
