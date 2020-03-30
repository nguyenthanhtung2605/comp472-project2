"""
Player library containing basic move operations.
"""

import getopt
import os

import helper
import sys

from classifier import TrainingClassifier, TestingClassifier
from lang_class import LanguageClass


def main(argv):
    vocabulary_type = 0
    ngram_type = 0
    smooth_value = 0
    filter_type = 0
    training_file = ''
    test_file = ''

    try:
        opts, args = getopt.getopt(argv, "hv:n:d:f:r:t:")

    except getopt.GetoptError:
        print('You have entered an invalid command. Below is the syntax of a valid command.')
        helper.display_helps()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('Below is the syntax of a valid command.')
            helper.display_helps()
            sys.exit()

        elif opt == "-r":
            if str(arg):
                training_file = str(arg)
            else:
                print('The training file location argument is not valid')
            if not os.path.exists(training_file):
                print('The training file you have entered does not exist.')
                sys.exit()

        elif opt == "-t":
            if str(arg):
                test_file = str(arg)
            else:
                print('The testing file location argument is not valid')
            if not os.path.exists(test_file):
                print('The test file you have entered does not exist.')
                sys.exit()

        elif opt == "-v":
            if int(arg) in [0, 1, 2]:
                vocabulary_type = int(arg)
            else:
                print('You have entered an invalid vocabulary type')

        elif opt == "-n":
            if int(arg) in [1, 2, 3, 4]:
                ngram_type = int(arg)
            else:
                print('You have entered an invalid size of n-grams')

        elif opt == "-f":
            if int(arg) in [0, 1, 2, 3, 4, 5, 6, 7]:
                filter_type = int(arg)
            else:
                print('You have entered an invalid noise filtering type')

        elif opt == "-d":
            try:
                if isinstance(float(arg), float) or isinstance(int(arg), int):
                    if 0 <= float(arg) <= 1:
                        smooth_value = float(arg)
                    else:
                        print('The smooth value you have entered is out of range [0:1]')
                else:
                    print('You have entered an invalid smooth value')
            except ValueError:
                print('You have entered an invalid smooth value')

    # training_file = 'OriginalDataSet/training-tweets.txt'

    # initialize language instances
    print('You have entered Vocabulary Value: {}'.format(vocabulary_type))
    print('You have entered Ngram Type Value: {}'.format(ngram_type))
    print('You have entered Smoothing Value: {}'.format(smooth_value))
    print('You have entered Filter Type Value: {}'.format(filter_type))
    print('You have entered Training File Location: {}'.format(training_file))
    print('You have entered Testing File Location: {}'.format(test_file))

    eu = LanguageClass('eu')
    ca = LanguageClass('ca')
    gl = LanguageClass('gl')
    es = LanguageClass('es')
    en = LanguageClass('en')
    pt = LanguageClass('pt')

    lang_classes = {'eu': eu, 'ca': ca, 'gl': gl, 'es': es, 'en': en, 'pt': pt}

    # initialize training classifier
    trained_data = TrainingClassifier(training_file=training_file, lang_classes=lang_classes,
                                      vocabulary_type=vocabulary_type, ngram_type=ngram_type,
                                      smooth_value=smooth_value, filter_type=filter_type)
    trained_data.classify_tweets()
    # test_file = 'OriginalDataSet/test-tweets-given.txt'

    # initialize testing
    test_data = TestingClassifier(test_file=test_file, trained_data=trained_data)
    test_data.set_priors()
    test_data.set_vocab_size()
    test_data.parse_tweets()
    test_data.classify_testing_tweets()
    test_data.evaluate_results()

    # print to file
    helper.write_to_file(test_data=test_data, vocabulary_type=vocabulary_type, ngram_type=ngram_type,
                         smooth_value=smooth_value, filter_type=filter_type)


if __name__ == "__main__":
    main(sys.argv[1:])
