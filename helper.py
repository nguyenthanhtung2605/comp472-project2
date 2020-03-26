import re
import string


def write_to_file(prefix, visited, path):
    solution_file = open(prefix + "_solution.txt", 'w')
    search_file = open(prefix + "_search.txt", 'w')

    if len(path) == 0:
        solution_file.write('no solution')
    else:
        for step in path:
            solution_file.write(step + '\n')

    solution_file.close()

    for step in visited:
        search_file.write(step + '\n')

    search_file.close()





def display_helps():
    print('bayes.py -V <Vocabulary> -s <size-of-n-grams> -d <smoothing value> -f <noise feature filtering> -n '
          '<training_filepath> -t <testing file_path>')

    vocab_text = '''
(-V) : Vocabulary
The program works at the character level (or words) and accounts for 3 types of vocabulary:
----------------
V : Significance
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


def filter_lower_only(tweet_content):
    return re.findall(r"[a-z]", tweet_content)


def filter_upper_lower(tweet_content):
    return re.findall(r"[a-z]|[A-Z]", tweet_content)


def filter_isalpha(tweet_content):
    return [x for x in tweet_content if str(x).isalpha()]


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
    '''
    tweet_filepath = 'OriginalDataSet/test-tweets-given.txt'
    tweet_list = read_tweet(tweet_filepath)

    for each in tweet_list:
        print(each)
    '''
    tweet_content = "http://t.co/jeDRtziT3S El amor se hizo para tener un motivo por el cual hacer muchísimas cosas deliciosas y absurdamente placenteras y decir que fue por amor. Seré @jordisunyer per carnaval tot s'hi val. #carnavalpda"

    # tokenize_tweet(tweet_content)
    #
    # tweet2 = "Seré un analfabeto musical, pero Paco de Lucía era tan bueno? 😕"
    # for letter in tweet2:
    #     print(letter + ':' + str(letter.isalpha()))

    filtering_pattern = r"[a-z]|[A-Z]"
    password = "SeréFa11con77YES"
    text = filter_upper_lower(password)
    print(text)
