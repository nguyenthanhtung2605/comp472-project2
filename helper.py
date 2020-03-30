import os
import re
import string

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def read_tweet(input_file):
    tweet_list = list()

    with open(input_file, 'r', encoding="utf8") as file:
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


def write_to_file(test_data, vocabulary_type, ngram_type, smooth_value, filter_type=0, prefix: str = 'trace'):
    data_folder = os.path.join(ROOT_DIR, 'ResultFiles')

    # filelist = [f for f in os.listdir(data_folder) if f.endswith(".txt")]
    # for f in filelist:
    #     os.remove(os.path.join(data_folder, f))

    if filter_type == 0 and ngram_type != 4:
        trace_file_path = os.path.join(data_folder,
                                       '{}_{}_{}_{}.txt'.format(prefix, vocabulary_type, ngram_type, smooth_value))
        evaluation_file_path = os.path.join(data_folder,
                                            'eval_{}_{}_{}.txt'.format(vocabulary_type, ngram_type, smooth_value))
    else:
        trace_file_path = os.path.join(data_folder,
                                       'myModel_{}_{}_{}_{}_filter{}.txt'.format(prefix, vocabulary_type,
                                                                                 ngram_type, smooth_value, filter_type))
        evaluation_file_path = os.path.join(data_folder, 'eval_myModel_{}_{}_{}_filter{}.txt'.format(vocabulary_type,
                                                                                                     ngram_type,
                                                                                                     smooth_value,
                                                                                                     filter_type))
    print('\n=============== Testing Resutls ===============')
    with open(trace_file_path, 'w', encoding="utf8") as trace_file:
        for tweet in test_data.tweets_to_predict:
            line = '{}  {}  {}  {}  {}'.format(tweet.id, tweet.language, tweet.prediction_score,
                                               tweet.predicted_language,
                                               tweet.prediction_result.name)
            print(line)
            trace_file.write(line + '\n')

    print('\n=============== Testing Evaluation ===============')
    with open(evaluation_file_path, 'w') as evaluation_file:

        eu_P = test_data.per_class_precision['eu']
        ca_P = test_data.per_class_precision['ca']
        gl_P = test_data.per_class_precision['gl']
        es_P = test_data.per_class_precision['es']
        en_P = test_data.per_class_precision['en']
        pt_P = test_data.per_class_precision['pt']

        eu_R = test_data.per_class_recall['eu']
        ca_R = test_data.per_class_recall['ca']
        gl_R = test_data.per_class_recall['gl']
        es_R = test_data.per_class_recall['es']
        en_R = test_data.per_class_recall['en']
        pt_R = test_data.per_class_recall['pt']

        eu_F = test_data.per_class_f1_measure['eu']
        ca_F = test_data.per_class_f1_measure['ca']
        gl_F = test_data.per_class_f1_measure['gl']
        es_F = test_data.per_class_f1_measure['es']
        en_F = test_data.per_class_f1_measure['en']
        pt_F = test_data.per_class_f1_measure['pt']

        line_accuracy = '{:.4f}'.format(test_data.accuracy_value)
        line_cls_precision = '{:.4f}  {:.4f}  {:.4f}  {:.4f}  {:.4f}  {:.4f}'.format(eu_P, ca_P, gl_P, es_P, en_P, pt_P)
        line_cls_recall = '{:.4f}  {:.4f}  {:.4f}  {:.4f}  {:.4f}  {:.4f}'.format(eu_R, ca_R, gl_R, es_R, en_R, pt_R)
        line_cls_f1_ms = '{:.4f}  {:.4f}  {:.4f}  {:.4f}  {:.4f}  {:.4f}'.format(eu_F, ca_F, gl_F, es_F, en_F, pt_F)
        line_macro_and_weighed_average_f1 = '{:.4f}  {:.4f}'.format(test_data.macro_f1_value,
                                                                    test_data.weighed_average_f1)

        print(line_accuracy)
        print(line_cls_precision)
        print(line_cls_recall)
        print(line_cls_f1_ms)
        print(line_macro_and_weighed_average_f1)

        evaluation_file.write(line_accuracy + '\n')
        evaluation_file.write(line_cls_precision + '\n')
        evaluation_file.write(line_cls_recall + '\n')
        evaluation_file.write(line_cls_f1_ms + '\n')
        evaluation_file.write(line_macro_and_weighed_average_f1 + '\n')


def display_helps():
    print('bayes.py -V <Vocabulary> -s <size-of-n-grams> -d <smoothing value> -f <noise feature filtering> -n '
          '<training_filepath> -t <testing file_path>')

    vocab_text = '''
(-v) : Vocabulary
The program works at the character level (or words) and accounts for 3 types of vocabulary:
----------------
v : Significance
----------------
0 : Fold the corpus to lowercase and use only the 26 letters of the alphabet [a-z]
1 : Distinguish up and low cases and use only the 26 letters of the alphabet [a-z, A-Z]
2 : Distinguish up and low cases and use all characters accepted by the built-in isalpha() method
----------------'''

    n_gram_size = '''
(-n) : Size of n-grams
The program works with 3 types of character-based n-grams as features::
----------------
n : Significance
----------------
1 : character uni-grams
2 : character bi-grams
3 : character tri-grams
4 : lower-case words separated by space
----------------'''

    smoothing_value = '''
(-d) : additive smoothing value (add-delta)
The value of delta will be a real in the interval [0 . . . 1].'''

    noise_filtering = '''
(-f) : Noise features to be removed
The program filters 4 types of noise feature filtering:
----------------
f : Significance
----------------
0 : no noises
1 : URL links
2 : @user tags
3 : #hashtags
4 : URL links and @user tags
5 : URL links and #hashtags
6 : @user tags and #hashtags
7 : all noises
----------------'''

    print(vocab_text)
    print(n_gram_size)
    print(smoothing_value)
    print(noise_filtering)


def tokenize_tweet(tweet_content):
    # remove URL links and @tag from Twitter tweet
    url_pattern = r"http\S+"
    attag_pattern = r"@\S+"
    combined_pat = r'|'.join((url_pattern, attag_pattern))

    sanitized_tweet = re.sub(combined_pat, "", tweet_content)

    # split into words by white space
    words = sanitized_tweet.split()

    # string of punctuation except for apostrophe
    punctuations = string.punctuation[0:6] + string.punctuation[8:32]

    # remove punctuation from each word
    table = str.maketrans('', '', punctuations)
    stripped = [w.translate(table) for w in words]

    # convert to lower case
    tokens = [word.lower() for word in stripped]
    print(tokens)
    return tokens


if __name__ == '__main__':
    print('This is Help File')
