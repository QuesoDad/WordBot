#print(os.stat(fileName).st_size) #Filesize of the current file
'''TO FIND AVERAGE: ADD ALL ITEMS TOGETHER AND THEN DIVIDE BY TOTAL NUMBER
	trains a model off a given text corpus, making suggested changes to train.lua commands based off file
	data and recommendations from char-rnn
	
	< 1mb is considdered very small
	if data is <2 mb, increase RNN size
	
	if data set is small, reduce batch size and sequence length

	
	
	Best model has lowest Validation loss.
	in lm_lstm_epoch0.95_2.0681.t7
	2.0681.t7 is the validation loss amount
	
	Compare this number to the training loss
		if training loss is much less than validation loss, network is overfitting
			decrease network size or increase dropout
		if training loss is about equal to validation, network is underfitting
			increase number of layers or number of neurons per layer
			
	Always use num_layers 2 oe 3
	
	Size of data set (1 mb ~= 100000 characters) should be same order of magnitude
		100 mb dataset with default batch and sequence settings works with 150K parameters
		100,000,000 characters > .15 million characters'''
		
		
Train multiple models and only continue with the one resulting in the best validation rate.


th train.lua -gpuid -1 -data_dir dockerdata/wordbot_testing -train_frac 0.96 -val_frac 0.04 -seq_length 10 -batch_size 10 -max_epochs 600 -word_level 1 -threshold 2 -print_every 10 -glove 1 -rnn_size 128 -num_layers 3 -dropout 0.8 -eval_val_every 500 -checkpoint_dir dockerdata/DH_word_128_b10S10_DO8_