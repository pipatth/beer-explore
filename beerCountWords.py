import pandas as pd
import re
import time
import sys

def countMatchedWords(text, pos_corp, neg_corp):
    reg = re.compile("[^\w']")
    text = text.lower()
    text = reg.sub(' ', text).split()
    return [len(text), sum([w in pos_corp for w in text]), sum([w in neg_corp for w in text])]

def formatCategories(x):
    return x.strip("[").strip("]").split(", ")

def addCategories(list_catdata, catname):
    if (catname in list_catdata):
        return True
    else:
        return False

def main(argv):
    dir = './'
    filename = argv[1]

    # load positive, negative words
    with open(dir + 'positive-words.txt') as f:
        pos = f.read().split()[213:]

    with open(dir + 'negative-words.txt') as f:
        neg = f.read().split()[213:]

    # load csv file
    df = pd.read_csv(dir + filename)
    print "The file has " + str(len(df.index)) + " reviews"

    # count positive, negative words
    start = time.time()
    df['count_match'] = df.apply(lambda row: countMatchedWords(row['note'], pos, neg), axis=1)
    A = df['count_match'].tolist()
    B = zip(*A)
    df['token_length'] = B[0]
    df['num_pos'] = B[1]
    df['num_neg'] = B[2]
    df['net'] = df['num_pos'] - df['num_neg']
    df.drop('count_match', 1, inplace=True)
    end = time.time()
    print "Running time " + str(end - start)
    df.to_csv(dir + filename, index=False, encoding='utf-8')

if __name__ == '__main__':
    main(sys.argv)
