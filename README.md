https://github.com/nguyenthanhtung2605/comp472-project2
# Comp472 - Project 2 -  Naive Bayes classiﬁcation

## Team ***MeSolo***
```
- Thanh Tung Nguyen: 40042891 <Leader>
```

## To run the program

### 1. display helps
To display helps enter
```
python bayes.py -h
```
### 2. run Professor's assigned models
To run Professor's assigned models

```python3 bayes.py -v <vocabulary_type> -n <ngram_type> -d <smooth_value>```

```
python bayes.py -v 0 -n 1 -d 0.0 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.txt
python bayes.py -v 1 -n 2 -d 0.5 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.txt
python bayes.py -v 1 -n 3 -d 1.0 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.txt

python bayes.py -v 2 -n 2 -d 0.3 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.txt
python bayes.py -v 1 -n 2 -d 0.5 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.txt
python bayes.py -v 1 -n 3 -d 0.6 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.txt

python bayes.py -v 2 -n 1 -d 0.7 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.txt
python bayes.py -v 2 -n 2 -d 0.8 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.txt
python bayes.py -v 2 -n 3 -d 0.9 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.txt

python bayes.py -v 0 -n 3 -d 1.0 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.txt

```

### 2. run my own models
To my own models

```python3 bayes.py -v <vocabulary_type> -n <ngram_type> -d <smooth_value> -f <filter_type>```

```
python bayes.py -v 0 -n 4 -d 0.1 -f 0 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.txt
python bayes.py -v 0 -n 4 -d 0.1 -f 1 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.txt
python bayes.py -v 0 -n 4 -d 0.1 -f 2 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.txt
python bayes.py -v 0 -n 4 -d 0.1 -f 4 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.txt
python bayes.py -v 0 -n 4 -d 0.1 -f 7 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.txt

python bayes.py -v 1 -n 4 -d 0.1 -f 7 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.txt
python bayes.py -v 2 -n 4 -d 0.1 -f 7 -r ./OriginalDataSet/test-tweets-given.txt -t ./OriginalDataSet/training-tweets.txt
```

## Dev envirionment
MacOS and Pycharm