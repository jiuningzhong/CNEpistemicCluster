from textblob.classifiers import NaiveBayesClassifier

# Loading Data and Creating a Classifier
train = [
     ('I love this sandwich.', 'pos'),
     ('this is an amazing place!', 'pos'),
     ('I feel very good about these beers.', 'pos'),
     ('this is my best work.', 'pos'),
     ("what an awesome view", 'pos'),
     ('I do not like this restaurant', 'neg'),
     ('I am tired of this stuff.', 'neg'),
     ("I can't deal with this", 'neg'),
     ('he is my sworn enemy!', 'neg'),
     ('my boss is horrible.', 'neg')
 ]

test = [
     ('the beer was good.', 'pos'),
     ('I do not enjoy my job', 'neg'),
     ("I ain't feeling dandy today.", 'neg'),
     ("I feel amazing!", 'pos'),
     ('Gary is a friend of mine.', 'pos'),
     ("I can't believe I'm doing this.", 'neg')
]

cl = NaiveBayesClassifier(train)

# Loading Data from Files
with open('train.json', 'r') as fp:
     cl = NaiveBayesClassifier(fp, format="json")

# Classifying Text
cl_result = cl.classify("This is an amazing library!")

print(cl_result)

prob_dist = cl.prob_classify("This one's a doozy.")
print(prob_dist.max())
print(round(prob_dist.prob("pos"), 2))
print(round(prob_dist.prob("neg"), 2))

# Classifying TextBlobs
from textblob import TextBlob
blob = TextBlob("The beer is good. But the hangover is horrible.", classifier=cl)
print(blob.classify())

for s in blob.sentences:
     print(s)
     print(s.classify())

# Evaluating Classifiers
print(cl.accuracy(test))

print(cl.show_informative_features(5))

# Updating Classifiers with New Data
new_data = [('She is my best friend.', 'pos'),
                  ("I'm happy to have a new friend.", 'pos'),
                  ("Stay thirsty, my friend.", 'pos'),
                  ("He ain't from around here.", 'neg')]

print(cl.update(new_data))
print(cl.accuracy(test))

def end_word_extractor(document):
     tokens = document.split()
     first_word, last_word = tokens[0], tokens[-1]
     feats = {}
     feats["first({0})".format(first_word)] = True
     feats["last({0})".format(last_word)] = False
     return feats

features = end_word_extractor("I feel happy")
assert features == {'last(happy)': False, 'first(I)': True}

cl2 = NaiveBayesClassifier(test, feature_extractor=end_word_extractor)
blob = TextBlob("I'm excited to try my new classifier.", classifier=cl2)
blob.classify()

# https://textblob.readthedocs.io/en/latest/api_reference.html#api-classifiers
