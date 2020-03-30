class LanguageClass:
    total_tweet = 0
    total_word = 0

    def __init__(self, classname):
        self.classname = classname
        self.indexer = dict()
        self.word_count = 0
        self.training_tweet_count = 0
        self.testing_tweet_count = 0
        self.tweet_list = list()
        self.cell_of_match_count: int = 0
        self.row_of_predicted_count: int = 0
        self.column_of_actual_count: int = 0

        self.precision_value = 0
        self.recall_value = 0
        self.f1_measure = 0

    @classmethod
    def increment_total_tweet(cls):
        cls.total_tweet += 1

    @classmethod
    def increment_total_word(cls, tweet):
        cls.total_word += len(tweet.words)

    def add_new_tweet(self, tweet):
        self.increment_total_tweet()
        self.increment_total_word(tweet)
        self.tweet_list.append(tweet)
        self.training_tweet_count += 1
        self.word_count += len(tweet.words)
        for each in tweet.words:
            if each in self.indexer:
                self.indexer[each] += 1
            else:
                self.indexer[each] = 1

    def increment_predicted_count(self):
            self.row_of_predicted_count += 1

    def increment_actual_count(self):
        self.column_of_actual_count += 1

    def increment_match_count(self):
        self.cell_of_match_count += 1

    def increment_testing_tweet_count(self):
            self.testing_tweet_count += 1

    def compute_precision(self):
        # print(self.classname)
        if self.cell_of_match_count == 0:
            precision = 0
        else:
            precision = self.cell_of_match_count / self.row_of_predicted_count

        # print('precision is {}'.format(precision))
        self.precision_value = precision
        return precision

    def compute_recall(self):
        if self.cell_of_match_count == 0:
            recall = 0
        else:
            recall = self.cell_of_match_count / self.column_of_actual_count

        # print('recall is {}'.format(recall))
        self.recall_value = recall
        return recall

    def compute_f1_measure(self):
        if self.cell_of_match_count == 0:
            f1_measure = 0
        else:
            precision = self.cell_of_match_count / self.row_of_predicted_count
            recall = self.cell_of_match_count / self.column_of_actual_count
            f1_measure = 2*(precision * recall)/(precision + recall)

        # print('f1_measure is {}'.format(f1_measure))
        self.f1_measure = f1_measure
        return f1_measure