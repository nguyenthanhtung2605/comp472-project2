from nb_classes import LanguageClassifier, Tweet


def read_tweet(input_file):
    tweet_list = list()

    with open(input_file, 'r') as file:
        entry_id = 1
        for each in file:
            tweet = dict()
            if each.find('	') > -1:
                parts = str(each).split('	')
                tweet['entry_id'] = entry_id
                tweet['id'] = parts[0]
                tweet['user'] = parts[1]
                tweet['language'] = parts[2]
                tweet['content'] = parts[3].strip()
                entry_id += 1
            else:
                continue
            tweet_list.append(tweet)

    return tweet_list


def classify_language(training_file, vocabulary_type=0, ngram_type=1, filter_type=0):
    tweet_list = read_tweet(training_file)

    eu = LanguageClassifier('eu')
    ca = LanguageClassifier('ca')
    gl = LanguageClassifier('gl')
    es = LanguageClassifier('es')
    en = LanguageClassifier('en')
    pt = LanguageClassifier('pt')

    lang_classes = {'eu': eu, 'ca': ca, 'gl': gl, 'es': es, 'en': en, 'pt': pt}

    for each in tweet_list:
        tweet = Tweet(each['id'], each['user'], each['language'], each['content'])
        tweet.get_ngram_words(vocabulary_type=vocabulary_type, ngram_type=ngram_type, filter_type=filter_type)

        if each['language'] in lang_classes:
            lang_classes[each['language']].add_new_tweet(tweet)

    print(eu.tweet_count)
    print(eu.word_count)
    print(eu.total_tweet)
    print(eu.total_word)

    print(eu.indexer)
    print(ca.indexer)
    print(gl.indexer)
    print(es.indexer)
    print(en.indexer)
    print(pt.indexer)
    return lang_classes


def get_priors(lang_classes):
    eu = lang_classes['eu'].tweet_count / lang_classes['eu'].total_tweet
    ca = lang_classes['ca'].tweet_count / lang_classes['ca'].total_tweet
    gl = lang_classes['gl'].tweet_count / lang_classes['gl'].total_tweet
    es = lang_classes['es'].tweet_count / lang_classes['es'].total_tweet
    en = lang_classes['en'].tweet_count / lang_classes['en'].total_tweet
    pt = lang_classes['pt'].tweet_count / lang_classes['pt'].total_tweet

    priors = {'eu': eu, 'ca': ca, 'gl': gl, 'es': es, 'en': en, 'pt': pt}
    print(priors)
    return priors


if __name__ == '__main__':
    training_file = 'OriginalDataSet/training-tweets.txt'
    tweet_list = read_tweet(training_file)
    print(tweet_list)
    vocabulary_type = 0
    ngram_type = 4
    filter_type = 0
    lang_classes = classify_language(training_file, vocabulary_type, ngram_type, filter_type)
    get_priors(lang_classes)
