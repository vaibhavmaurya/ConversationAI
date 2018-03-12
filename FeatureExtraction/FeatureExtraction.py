class ExtractFeature():
    def __init__(self):
        from time import time
        from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
        import os;
        from sklearn.externals import joblib

        self.time = time;
        self.TfidfTransformer = TfidfTransformer;
        self.CountVectorizer = CountVectorizer;
        self.os = os;
        self.joblib = joblib;

    def extract_feature(self, save_feature=True, data=None, n_features=10000, n_grams=(1, 2), online=False, extendPath=None):
        tf_vectorizer = self.CountVectorizer(max_df=0.95, min_df=0, analyzer='word',
                                             max_features=n_features,
                                             stop_words='english'
                                             , ngram_range=n_grams
                                             )

        t0 = self.time()
        tf = tf_vectorizer.fit_transform(data['Sentence'])
        print("done in %0.3fs." % (self.time() - t0))
        print(tf.shape)
        print('After learning', tf_vectorizer.vocabulary_)

        tf_transformer = self.TfidfTransformer(use_idf=False).fit(tf)
        X_train_tfidf = tf_transformer.transform(tf)
        pathString = ".\\FeatureExtraction\\Data"
        vocab_path = ".\\Vocabulary"
        if extendPath:
            pathString = pathString+"\\"+extendPath
            vocab_path = vocab_path+"\\"+extendPath

        pathS = ''
        if online:
            pathS = 'Online'
        if save_feature:
            if not self.os.path.exists(pathString):
                self.os.makedirs(pathString)

            if self.os.path.exists(pathString):
                vocab_count = len(self.os.listdir(pathString))
                self.joblib.dump(X_train_tfidf, pathString+'\\X' + pathS + '.pkl')
                self.joblib.dump(data['Class'], pathString+'\\Y' + pathS + '.pkl')
                self.joblib.dump(tf_vectorizer, pathString+'\\CountVectorization' + pathS + '.pkl')
                self.joblib.dump(tf_transformer, pathString+'\\TfIdfVectorization' + pathS + '.pkl')
                print('Collected Features:', tf_vectorizer.get_feature_names())

                if not self.os.path.exists(vocab_path):
                    self.os.makedirs(vocab_path)

                self.joblib.dump(tf_vectorizer.get_feature_names(), vocab_path+'\\FeatureNames' + pathS + '.pkl')
                print('Build Vocabulary is : ', tf_vectorizer.vocabulary_)

                self.joblib.dump(tf_vectorizer.vocabulary_, vocab_path+'\\Vocabulary' + pathS + '.pkl')
            else:
                raise Exception('ExtractFeature->extract_feature->Vocabulary directory does not exist')

        return X_train_tfidf, data['Class']
