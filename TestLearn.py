from time import time

import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
import os;
from sklearn.externals import joblib
from sklearn.linear_model import SGDClassifier


n_samples = 2000
n_features = 10000
n_components = 10
n_top_words = 20


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()


if os.path.exists(".\\FeatureExtraction"):
    vocab_count = len(os.listdir(".\\FeatureExtraction"))
    X_train_tfidf = joblib.load('.\\FeatureExtraction\\X.pkl')
    YClass = joblib.load('.\\FeatureExtraction\\Y.pkl')
    X_train_tfidfO = joblib.load('.\\FeatureExtraction\\XOnline.pkl')
    YClassO = joblib.load('.\\FeatureExtraction\\YOnline.pkl')
else:
    raise Exception('Vocabulary directory does not exist')

print('shape of tf-idf converted data is = ',X_train_tfidf.shape)


clf_SGD = SGDClassifier(loss='hinge', penalty='l2',
                                           alpha=1e-3, random_state=42,
                                            max_iter=100, tol=None).fit(X_train_tfidf,YClass)


predicted = clf_SGD.predict(X_train_tfidf)
print('SGD performance = ',np.mean(predicted == YClass))

clf_SGDO = SGDClassifier(loss='hinge', penalty='l2',
                                           alpha=1e-3, random_state=42,
                                            max_iter=100, tol=None).fit(X_train_tfidfO,YClassO)


predicted = clf_SGDO.predict(X_train_tfidfO)
print('SGD performance for online data = ',np.mean(predicted == YClassO))

if os.path.exists('.\\Model'):
    joblib.dump(clf_SGD,'.\\Model\\SGDModelFromFile.pkl')
    joblib.dump(clf_SGDO, '.\\Model\\SGDModelFromFileO.pkl')
