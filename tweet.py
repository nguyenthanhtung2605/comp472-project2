import enum
import string
import re

from helper import filter_tweet


class PredictionResult(enum.Enum):
    correct = 'correct'
    wrong = 'wrong'


class Tweet:
    def __init__(self, id, user, language, content):
        self.id = id
        self.user = user
        self.language = language
        self.content = content
        self.letters = list()
        self.words = list
        self.tweet_score_by_class = None
        self.predicted_language = None
        self.prediction_result = None
        self.prediction_score = None

    def get_ngram_words(self, vocabulary_type=0, ngram_type=1, filter_type=0):

        filtered_tweet = filter_tweet(self.content, filter_type)

        if vocabulary_type == 0:

            self.letters = re.findall(r"[a-z]", str(filtered_tweet).lower())
        elif vocabulary_type == 1:
            self.letters = re.findall(r"[a-z]|[A-Z]", filtered_tweet)
        else:
            self.letters = [x for x in filtered_tweet if str(x).isalpha()]

        if ngram_type == 1:
            self.words = self.letters
            return self.words

        elif ngram_type == 2:
            self.words = ['{}{}'.format(self.letters[i], self.letters[i + 1]) for i in
                          range(len(self.letters) - 2)]
            return self.words

        elif ngram_type == 3:
            self.words = ['{}{}{}'.format(self.letters[i], self.letters[i + 1], self.letters[i + 2])
                          for i in range(len(self.letters) - 3)]
            return self.words

        else:
            # split into words by white space
            words = str(filtered_tweet).lower().split()

            # string of punctuation except for apostrophe
            punctuations = string.punctuation[0:6] + string.punctuation[8:32]

            # remove punctuation from each word
            table = str.maketrans('', '', punctuations)
            stripped = [w.translate(table) for w in words]

            # convert to lower case
            self.words = [word.lower() for word in stripped]
            return self.words

    def set_tweet_score_by_class(self, tweet_score_by_class: dict):
        self.tweet_score_by_class = tweet_score_by_class

    def set_predicted_language(self, predicted_language: str):
        self.predicted_language = predicted_language

    def set_prediction_result(self, prediction_result: PredictionResult):
        self.prediction_result = prediction_result

    def set_prediction_score(self, prediction_score):
        self.prediction_score = "{:E}".format(prediction_score)


if __name__ == '__main__':
    print('This is Tweet File')
