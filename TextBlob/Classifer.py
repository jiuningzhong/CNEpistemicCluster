from textblob.classifiers import NaiveBayesClassifier
from textblob.classifiers import NLTKClassifier
from nltk.classify import SklearnClassifier
from nltk.classify import DecisionTreeClassifier
from sklearn.naive_bayes import BernoulliNB
 # The implementation is based on libsvm.
from sklearn.svm import SVC
# liblinear
from sklearn.svm import LinearSVC
import nltk

class MyClassifier(NLTKClassifier):
    # nltk_class = SklearnClassifier(BernoulliNB())                                                       # accuracy:  0.45454545454545453
    # nltk_class = SklearnClassifier(SVC()) # , sparse=False                                            # accuracy:  0.8181818181818182
    nltk_class = SklearnClassifier(LinearSVC(penalty='l2', C=1.0, max_iter=1000 , random_state=0))    # accuracy:  0.8484848484848485
    # https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html
    # , sparse=False            , class_weight='balanced', tol=1e-05
    # nltk_class = nltk.classify.decisiontree.DecisionTreeClassifier # accuracy:  0.7272727272727273

# Loading Data from Files
with open('train.csv', 'r', encoding='utf8') as train:
     cl = MyClassifier(train, format="csv")
     # cl = NaiveBayesClassifier(train, format="csv") # accuracy:  0.7831325301204819

accuracy = 0
with open('test.csv', 'r', encoding='utf8') as test:
     accuracy = cl.accuracy(test, format="csv")
# cl.classify_many
# cl.classify
print('accuracy: ', accuracy)
