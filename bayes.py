"""
Player library containing basic move operations.
"""

import getopt
import os

import helper
import sys


def main(argv):
    input_file = ''
    search_algorithm = 'DFS'

    try:
        opts, args = getopt.getopt(argv, "hV:n:d:f:r:t:")
        print(opts)

    except getopt.GetoptError:
        print('You have entered an invalid command. Below is the syntax of a valid command.')
        helper.display_helps()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('Below is the syntax of a valid command.')
            helper.display_helps()
            sys.exit()

        if opt == "-r":
            training_file = arg
            if not os.path.exists(training_file):
                print('The training file you have entered does not exist.')
                sys.exit()

        if opt == "-t":
            test_file = arg
            if not os.path.exists(test_file):
                print('The test file you have entered does not exist.')
                sys.exit()

        if opt == "-V":
            if arg in [0, 1, 2]:
                vocabulary_type = arg
            else:
                print('You have entered an invalid vocabulary type')

        if opt == "-n":
            if arg in [1, 2, 3, 4]:
                ngram_type = arg
            else:
                print('You have entered an invalid size of n-grams')

        if opt == "-f":
            if arg in [0, 1, 2, 3, 4, 5, 6, 7]:
                filter_type = arg
            else:
                print('You have entered an invalid noise filtering type')


if __name__ == "__main__":
    main(sys.argv[1:])
