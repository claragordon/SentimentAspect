#!/bin/bash

# run laptop tests

python2.7 src/py_main.py data/train/laptop--train.xml data/test/laptop--test.gold.xml

mallet import-file --input mallet_files/train --output mallet_files/train.mallet

mallet import-file --input mallet_files/test --output mallet_files/test.mallet  --use-pipe-from mallet_files/train.mallet

vectors2classify --training-file mallet_files/train.mallet --testing-file mallet_files/test.mallet --trainer NaiveBayes --trainer MaxEnt --trainer DecisionTree --trainer "new AdaBoostM2Trainer(new DecisionTreeTrainer())"  --report test:accuracy > mallet_files/laptop/"$1".out 

# run restaurant tests

python2.7 src/py_main.py data/train/restaurant--train.xml data/test/restaurant--test.gold.xml 
 
mallet import-file --input mallet_files/train --output mallet_files/train.mallet

mallet import-file --input mallet_files/test --output mallet_files/test.mallet  --use-pipe-from mallet_files/train.mallet

vectors2classify --training-file mallet_files/train.mallet --testing-file mallet_files/test.mallet --trainer NaiveBayes --trainer MaxEnt --trainer DecisionTree --trainer "new AdaBoostM2Trainer(new DecisionTreeTrainer())"  --report test:accuracy > mallet_files/restaurant/"$1".out 

