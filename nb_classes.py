import re
import string


def filter_tweet(tweet, filter_type=0):
    url_pattern = r"http\S+"
    attag_pattern = r"@\S+"
    hashtag_pattern = r"#\S+"

    if filter_type == 0:
        return tweet
    elif filter_type == 1:
        return re.sub(url_pattern, "", tweet)
    elif filter_type == 2:
        return re.sub(attag_pattern, "", tweet)
    elif filter_type == 3:
        return re.sub(hashtag_pattern, "", tweet)
    elif filter_type == 4:
        combined_pat = r'|'.join((url_pattern, attag_pattern))
        return re.sub(combined_pat, "", tweet)
    elif filter_type == 5:
        combined_pat = r'|'.join((url_pattern, hashtag_pattern))
        return re.sub(combined_pat, "", tweet)
    elif filter_type == 6:
        combined_pat = r'|'.join((attag_pattern, hashtag_pattern))
        return re.sub(combined_pat, "", tweet)
    else:
        combined_pat = r'|'.join((url_pattern, attag_pattern, hashtag_pattern))
        return re.sub(combined_pat, "", tweet)


class Tweet:
    def __init__(self, id, user, language, content):
        self.id = id
        self.user = user
        self.language = language
        self.content = content
        self.letters = list()
        self.words = list

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


class LanguageClassifier:
    total_tweet = 0
    total_word = 0

    def __init__(self, classname):
        self.classname = classname
        self.indexer = dict()
        self.word_count = 0
        self.tweet_count = 0
        self.tweet_list = list()

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
        self.tweet_count += 1
        self.word_count += len(tweet.words)
        for each in tweet.words:
            if each in self.indexer:
                self.indexer[each] += 1
            else:
                self.indexer[each] = 1


if __name__ == '__main__':
    tweet_content = "http://t.co/jeDRtziT3S El amor se hizo para tener un motivo por el cual hacer muchísimas cosas " \
                    "deliciosas y absurdamente placenteras y decir que fue por amor. Seré @jordisunyer per carnaval " \
                    "tot s'hi val. #carnavalpda "

    tweet = Tweet(19860526, 'galford265', 'en', tweet_content)
    words = tweet.get_ngram_words(0, 4, 1)
    print(words)
    print(tweet.letters)
    print(tweet.words)
