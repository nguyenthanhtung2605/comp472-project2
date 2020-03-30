# comp472-project2

## commands

### 1. display helps
To display helps enter
```
python bayes.py -h
```
### 2. run Professor's assigned models
To run Professor's assigned models
```
python bayes.py -v 0 -n 1 -d 0.1 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.txt
python bayes.py -v 0 -n 2 -d 0.2 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.tx
python bayes.py -v 0 -n 3 -d 0.3 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.tx

python bayes.py -v 1 -n 1 -d 0.4 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.tx
python bayes.py -v 1 -n 2 -d 0.5 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.tx
python bayes.py -v 1 -n 3 -d 0.6 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.tx

python bayes.py -v 2 -n 1 -d 0.7 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.tx
python bayes.py -v 2 -n 2 -d 0.8 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.tx
python bayes.py -v 2 -n 3 -d 0.9 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.tx

python bayes.py -v 0 -n 3 -d 1.0 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.tx

```

### 2. run my own models
To my own models
```
python bayes.py -v 0 -n 4 -d 0.1 -f 0 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.tx
python bayes.py -v 0 -n 4 -d 0.1 -f 1 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.tx
python bayes.py -v 0 -n 4 -d 0.1 -f 2 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.tx
python bayes.py -v 0 -n 4 -d 0.1 -f 4 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.tx
python bayes.py -v 0 -n 4 -d 0.1 -f 7 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.tx

python bayes.py -v 1 -n 4 -d 0.1 -f 7 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.tx
python bayes.py -v 2 -n 4 -d 0.1 -f 7 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.tx
```