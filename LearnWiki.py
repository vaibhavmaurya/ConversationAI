import wikipedia as wk;
from nltk.corpus import stopwords as sw;
from nltk.stem.wordnet import WordNetLemmatizer;
import string;
from time import time

from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer


from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier

n_samples = 2000
n_features = 10000
n_components = 10
n_top_words = 20



stop = set(sw.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()


def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


doc_complete = [];
doc_complete.append(clean(wk.page('fund transfer').content));
doc_complete.append(clean(wk.page('account balance').content));
print('wikipedia reading done');


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()


'''
Each word is given an ID and frequency of each important is calculated now.
x[i,j] frequency of word j in the document i
'''


tf_vectorizer = CountVectorizer(max_df=0.95, min_df=0,
                                max_features=n_features,
                                stop_words='english')

t0 = time()
tf = tf_vectorizer.fit_transform(doc_complete)
print("done in %0.3fs." % (time() - t0))
print(tf.shape)

'''

But counting frequency is not enough. Since larger document can dominate, so divide by total frequency = tf term frequencies
Another refinement on top of tf is to downscale weights for words that occur in many documents in the corpus and are 
therefore less informative than those that occur only in a smaller portion of the corpus
reference material is below
http://www.tfidf.com/

'''
tf_transformer = TfidfTransformer(use_idf=False).fit(tf)
X_train_tfidf = tf_transformer.transform(tf)
'''
can be used as below
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
'''
print('shape of tf-idf converted data is = ',X_train_tfidf.shape)

'''
It is time to learn. Just using MultinomialNB where NB stands for Naive Bayes Classifier 

'''

clf_NB = MultinomialNB().fit(X_train_tfidf,['fund transfer', 'account balance'])

clf_SGD = SGDClassifier(loss='hinge', penalty='l2',
                                           alpha=1e-3, random_state=42,
                                            max_iter=5, tol=None).fit(X_train_tfidf,['fund transfer', 'account balance'])
print('classification successful');


'''
pipeline also can be done 
 reference material is below
 http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
'''

'''
performance testing is missing ?????????????
'''

'''
Let's test our model

'''

docs_new = ['I want to do online payment','I want to check my account balance','transfer money','what is the balance']

normalized_doc = [];
for doc in docs_new:
    normalized_doc.append(clean(doc))

print('here is your question : ',normalized_doc)
X_new_counts = tf_vectorizer.transform(normalized_doc)
X_new_tfidf = tf_transformer.transform(X_new_counts)

predicted = clf_NB.predict(X_new_tfidf)

print('NB prediction is here: ',predicted);

clf_SGD.predict(X_new_tfidf)
print('SGD prediction is here: ',predicted);
