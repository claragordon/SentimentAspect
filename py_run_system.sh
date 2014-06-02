#!/bin/bash

python2.7 src/py_main.py "$@"

mallet import-file --input mallet_files/train --output mallet_files/train.mallet

mallet import-file --input mallet_files/test --output mallet_files/test.mallet  --use-pipe-from mallet_files/train.mallet

vectors2classify --training-file mallet_files/train.mallet --testing-file mallet_files/test.mallet --trainer NaiveBayes --trainer MaxEnt --report test:accuracy > mallet_files/"$3".out 2> mallet_files/results.err

