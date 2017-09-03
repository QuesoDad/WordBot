#!/bin/bash

curl -s http://nlp.stanford.edu/data/glove.840B.300d.zip | bash
fastjar xvf glove.840B.300d.zip
mkdir util/glove
cp glove.840B.300d.txt util/glove/vectors.840B.300d.txt
