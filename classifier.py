import math
import operator
from math import log

from helper import read_tweet, write_to_file
from lang_class import LanguageClass
from tweet import Tweet, PredictionResult


class TrainingClassifier:
    def __init__(self, training_file: str, lang_classes, vocabulary_type=0, ngram_type=1,
                 smooth_value=1, filter_type=0):
        self.training_file = training_file
        self.lang_classes = lang_classes
        self.vocabulary_type = vocabulary_type
        self.ngram_type = ngram_type
        self.filter_type = filter_type
        self.smooth_value = smooth_value

    def classify_tweets(self):
        tweet_list = read_tweet(self.training_file)
        for each in tweet_list:
            tweet = Tweet(each['id'], each['user'], each['language'], each['content'])
            tweet.get_ngram_words(vocabulary_type=self.vocabulary_type, ngram_type=self.ngram_type, filter_type=self.filter_type)

            if each['language'] in self.lang_classes:
                self.lang_classes[each['language']].add_new_tweet(tweet)


class TestingClassifier:
    def __init__(self, test_file: str, trained_data: TrainingClassifier):
        self.test_file = test_file
        self.trained_data = trained_data
        self.tweets_to_predict = list()
        self.priors = dict()
        self.vocab_size = 0
        self.accuracy_value = 0
        self.macro_f1_value = 0
        self.weighed_average_f1 = 0
        self.per_class_precision = None
        self.per_class_recall = None
        self.per_class_f1_measure = None

    def set_priors(self):
        self.priors['eu'] = self.trained_data.lang_classes['eu'].training_tweet_count / self.trained_data.lang_classes[
            'eu'].total_tweet
        self.priors['ca'] = self.trained_data.lang_classes['ca'].training_tweet_count / self.trained_data.lang_classes[
            'ca'].total_tweet
        self.priors['gl'] = self.trained_data.lang_classes['gl'].training_tweet_count / self.trained_data.lang_classes[
            'gl'].total_tweet
        self.priors['es'] = self.trained_data.lang_classes['es'].training_tweet_count / self.trained_data.lang_classes[
            'es'].total_tweet
        self.priors['en'] = self.trained_data.lang_classes['en'].training_tweet_count / self.trained_data.lang_classes[
            'en'].total_tweet
        self.priors['pt'] = self.trained_data.lang_classes['pt'].training_tweet_count / self.trained_data.lang_classes[
            'pt'].total_tweet

    def set_vocab_size(self):
        if self.trained_data.vocabulary_type == 1:
            # lower cases plus upper cases characters
            no_of_letter = 26 * 2

        elif self.trained_data.vocabulary_type == 2:
            # max number of characters are the sum of 26 normal characters plus 16 special characters
            # this number of letters is applied for isalpha() function
            # lower cases plus upper cases characters

            no_of_letter = (26 + 16) * 2
        else:
            # lower cases only
            no_of_letter = 26

        if self.trained_data.ngram_type == 2:
            vocab_size = no_of_letter ** 2

        elif self.trained_data.ngram_type == 3:
            vocab_size = no_of_letter ** 3

        elif self.trained_data.ngram_type == 1:
            vocab_size = no_of_letter

        else:
            # based on wiki list of dictionaries by number of words
            # we only consider single words and exclude compound words
            # we also take into account names. We refer to wikipedia to get
            # List_of_dictionaries_by_number_of_words
            # https: // en.wikipedia.org / wiki / List_of_dictionaries_by_number_of_words
            # Catalan: 69988
            # Galician: 59999
            # Spanish: 93000
            # French: 100000
            # Portuguese: 442000
            # English: 470000
            # We're taking the max
            vocab_size = 470000

        self.vocab_size = vocab_size * self.trained_data.smooth_value

    def parse_tweets(self):
        tweet_list = read_tweet(self.test_file)
        for each in tweet_list:
            tweet = Tweet(each['id'], each['user'], each['language'], each['content'])
            tweet.get_ngram_words(vocabulary_type=self.trained_data.vocabulary_type,
                                  ngram_type=self.trained_data.ngram_type, filter_type=self.trained_data.filter_type)
            self.tweets_to_predict.append(tweet)

    def get_word_likelihood(self, word: str, classname: str):
        if word in self.trained_data.lang_classes[classname].indexer:
            word_predictor_value = self.trained_data.lang_classes[classname].indexer[word] + self.trained_data.smooth_value
        else:
            word_predictor_value = self.trained_data.smooth_value
        class_num_of_words = self.trained_data.lang_classes[classname].total_word + self.vocab_size
        if self.trained_data.smooth_value == 0:
            likelihood = -math.inf
        else:
            likelihood = log(word_predictor_value / class_num_of_words, 10)
        return likelihood

    def predict_tweet_language(self, tweet_instance: Tweet):
        tweet_score_by_class = dict()
        for key, value in self.priors.items():
            tweet_score_by_class[key] = log(value, 10)
            for word in tweet_instance.words:
                tweet_score_by_class[key] += self.get_word_likelihood(word, key)

        tweet_instance.set_tweet_score_by_class(tweet_score_by_class)

        predicted_language = max(tweet_score_by_class.items(), key=operator.itemgetter(1))[0]
        tweet_instance.set_predicted_language(predicted_language)
        prediction_score = tweet_score_by_class[predicted_language]
        tweet_instance.set_prediction_score(prediction_score)
        if predicted_language == tweet_instance.language:
            # print('{} - {}: correct with score of {}'.format(tweet_instance.language, predicted_language, prediction_score))
            tweet_instance.set_prediction_result(PredictionResult.correct)
        else:
            # print('{} - {}: wrong with score of {}'.format(tweet_instance.language, predicted_language, prediction_score))
            tweet_instance.set_prediction_result(PredictionResult.wrong)

        return predicted_language

    def classify_testing_tweets(self):
        # print(self.trained_data.lang_classes)
        for tweet_instance in self.tweets_to_predict:
            predicted_language = self.predict_tweet_language(tweet_instance)

            for language in self.trained_data.lang_classes.values():
                language.increment_testing_tweet_count()
                if (tweet_instance.language == predicted_language) and (predicted_language == language.classname):
                    language.increment_match_count()
                if tweet_instance.language == language.classname:
                    language.increment_actual_count()
                if predicted_language == language.classname:
                    language.increment_predicted_count()

    def evaluate_results(self):
        per_class_precision = dict()
        per_class_recall = dict()
        per_class_f1_measure = dict()
        for each in self.trained_data.lang_classes.values():
            class_precision = each.compute_precision()
            class_recall = each.compute_recall()
            class_f1_measure = each.compute_f1_measure()
            print('{}_precision: {}'.format(each.classname,class_precision))
            print('{}_recall: {}'.format(each.classname, class_recall))
            print('{}_f1_measure: {}'.format(each.classname, class_f1_measure))
            per_class_precision[each.classname] = class_precision
            per_class_recall[each.classname] = class_recall
            per_class_f1_measure[each.classname] = class_f1_measure

        self.compute_accuracy()
        self.compute_macro_f1_measure()
        self.compute_weighted_average_f1_measure()

        self.per_class_precision = per_class_precision
        self.per_class_recall = per_class_precision
        self.per_class_f1_measure = per_class_precision
        return

    def compute_accuracy(self):
        sum_of_diagonal_match_count = 0
        for each in self.trained_data.lang_classes.values():
            sum_of_diagonal_match_count += each.cell_of_match_count
        total_test_cases = next(iter(self.trained_data.lang_classes.values())).testing_tweet_count
        accuracy = sum_of_diagonal_match_count / total_test_cases
        print('accuracy is {}'.format(accuracy))
        self.accuracy_value = accuracy
        return accuracy

    def compute_macro_f1_measure(self):
        sum_of_f1_measure_of_each_class = 0
        for each in self.trained_data.lang_classes.values():
            sum_of_f1_measure_of_each_class += each.f1_measure
        total_num_of_classes = len(self.trained_data.lang_classes)
        macro_f1_measure = sum_of_f1_measure_of_each_class / total_num_of_classes
        print('macro_f1_measure is {}'.format(macro_f1_measure))
        self.macro_f1_value = macro_f1_measure
        return macro_f1_measure

    def compute_weighted_average_f1_measure(self):
        sum_of_f1_of_each_class_multiply_weight = 0
        for each in self.trained_data.lang_classes.values():
            sum_of_f1_of_each_class_multiply_weight += (each.f1_measure * each.column_of_actual_count)
        total_test_cases = next(iter(self.trained_data.lang_classes.values())).testing_tweet_count
        weighted_average_f1_measure = sum_of_f1_of_each_class_multiply_weight / total_test_cases
        print('weighted_average_f1_measure is {}'.format(weighted_average_f1_measure))
        self.weighed_average_f1 = weighted_average_f1_measure
        return weighted_average_f1_measure


if __name__ == '__main__':
    print('This is Classifier File')

