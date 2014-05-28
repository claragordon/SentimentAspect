#!/bin/sh

java -Xmx6g -cp "out/production/SentimentAspect/:/usr/local/bin/stanford-corenlp-full-2014-01-04/*" Main "$1" "$2"

mallet import-file --input mallet_files/train --output mallet_files/train.mallet

mallet import-file --input mallet_files/test --output mallet_files/test.mallet  --use-pipe-from mallet_files/train.mallet

vectors2classify --training-file mallet_files/train.mallet --testing-file mallet_files/test.mallet --trainer NaiveBayes --report test:accuracy >> mallet_files/"$3".out 2>> mallet_files/results.err

vectors2classify --training-file mallet_files/train.mallet --testing-file mallet_files/test.mallet --trainer MaxEnt --report test:accuracy >> mallet_files/"$3".out 2>> mallet_files/results.err
