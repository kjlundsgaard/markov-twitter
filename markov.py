import os

import twitter

# from sys import argv

from random import choice

from random import sample


api = twitter.Api(consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
                  consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
                  access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
                  access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

print api.VerifyCredentials()

def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    with open(file_path) as file_object:

        poem = file_object.read()


    return poem


def make_chains(text_string, n=2):
    """Takes input text as string; returns _dictionary_ of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """

    chains = {}

    words = text_string.split()

    # len(words) -n so we avoid indexerror by trying to append out of avail index 
    for i in range(len(words) - n):
        # slicing words list with i up to i+n, converting to tuple 
        ngram = tuple(words[i:i+n])
        if ngram in chains:
            # if ngram already in dict, then append the next value at ngramth key
            chains[ngram].append(words[i+n])
        else:
            # if not in dict, then assigning a list with value to dict at ngramth key 
            chains[ngram] = [words[i+n]]

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""
    uppercase_letters = set()
    ending_punctuation = set()
    # use isupper() to check str index 0 of the first element in tuple
    # use isalpha() to check str index -1 of the last element in the tuple
    keys = chains.keys()
    for t in keys:
        if t[0][0].isupper():
            uppercase_letters.add(t)
        elif t[-1][-1].isalpha() == False:
            ending_punctuation.add(t)

    # initialize key ngram by selecting a random choice of chain key
    # sample is like choice but for sets, must give arg of how many returned
    # indexed at zero b/c returns list and we don't want it in list form
    key_ngram = sample(uppercase_letters, 1)[0] 
    # initalize text by joining strings in key ngram to make first string
    text = " ".join(key_ngram)

    while key_ngram in chains and len(text) < 140:
        # get a random choice value from chains at the key_ngramth element
        random_value = choice(chains[key_ngram])
        # now text is equal to old text but new random value
        text = text + " " + random_value
        # slicing a tuple from index 1 to the end and then adding rand.value to end
        key_ngram = key_ngram[1:] + (random_value,)

        # think about: len text < 140 characters 


    return text



input_path = "green-eggs.txt"
# input_path = argv[1]
# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text)

# Produce random text
random_text = make_text(chains)

# status = api.PostUpdate(random_text)
# print status.text


def go_tweet(chain):
    print chain
    go_again = raw_input("Enter to tweet again [q to quit]> ")

    while go_again != "q":
        print chain
        go_again = raw_input("Enter to tweet again [q to quit]> ")
    return 
go_tweet(random_text)
        
        




