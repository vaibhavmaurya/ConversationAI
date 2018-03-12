class TextClassificationModelTrain:
    def __init__(self,online=False):
        from FeatureExtraction import FeatureExtraction as fe
        from TrainModel import ReadDataOnline as rd
        import json
        import numpy as np
        import os;
        from sklearn.externals import joblib
        from sklearn.linear_model import SGDClassifier

        self.b_online = online
        self.fe = fe
        self.rd = rd
        self.np = np
        self.os = os
        self.joblib = joblib
        self.SGDClassifier = SGDClassifier
        self.CONFIG = None
        self.learnPath = None
        self.json = json

        with open(".\\config\\config.json") as data_file:
            self.CONFIG = json.load(data_file)

        with open(".\\config\\learnPath.json") as data_file:
            self.learnPath = json.load(data_file)

    def read_data(self,termList=[],extendPath=None):
        build_data = self.rd.ReadDataOnlineAPI();
        data = None;

        pathString = self.CONFIG["DATA_PATH"]

        if extendPath:
            pathString = pathString+"\\"+extendPath

        try:
            if self.b_online:
                # data = build_data.readOnline(['account balance', 'fixed deposit', 'payment'])
                data = build_data.readOnline(termList)
            else:
                print("read online data path : ",pathString)
                data = build_data.readFromFile(pathString, termList=termList)
        except Exception as ex:
           print(ex)
           raise Exception('Program Failed')

        f_extract = self.fe.ExtractFeature()
        f_extract.extract_feature(data=data, online=self.b_online, extendPath=extendPath)


    def train_model(self,termList=[],extendPath=None):
        n_samples = 2000
        n_features = 10000
        n_components = 10
        n_top_words = 20
        self.read_data(termList, extendPath=extendPath)
        s = ''
        p = ''

        pathString = ".\\FeatureExtraction\\Data"
        modelPath = ""
        if extendPath:
            pathString = pathString + "\\"+extendPath
            modelPath = "\\"+extendPath

        if self.b_online:
            s = 'O'
            p = 'Online'
        if self.os.path.exists(pathString):
            print("your path string is : ",pathString)
            print("your extended path string is : ",extendPath)
            vocab_count = len(self.os.listdir(pathString))
            X_train_tfidf = self.joblib.load(pathString+'\\X'+p+'.pkl')
            YClass = self.joblib.load(pathString+'\\Y'+p+'.pkl')
        else:
            raise Exception('Vocabulary directory does not exist')
        print('shape of tf-idf converted data is = ', X_train_tfidf.shape)
        clf_SGD = self.SGDClassifier(loss='hinge', penalty='l2',
                                alpha=1e-3, random_state=42,
                                max_iter=100, tol=None).fit(X_train_tfidf, YClass)
        predicted = clf_SGD.predict(X_train_tfidf)
        print('SGD performance = ', self.np.mean(predicted == YClass))

        if not self.os.path.exists('.\\Model' + modelPath):
            self.os.makedirs('.\\Model' + modelPath)

        if self.os.path.exists('.\\Model'+modelPath):
            self.joblib.dump(clf_SGD, '.\\Model'+modelPath+'\\SGDModelFromFile'+s+'.pkl')

    def print_top_words(model, feature_names, n_top_words):
        for topic_idx, topic in enumerate(model.components_):
            message = "Topic #%d: " % topic_idx
            message += " ".join([feature_names[i]
                                 for i in topic.argsort()[:-n_top_words - 1:-1]])
            print(message)
        print()


    def handle_learn_path(self):
        self.b_online = False
        for k,v in self.learnPath.items():
            if k == "topics":
                self.train_model(self.learnPath[k],extendPath=None)
            else:
                self.train_model(self.learnPath[k], extendPath=k+"_")
        self.CONFIG["MODEL_LEARNT"] = "X"
        with open(".\\config\\config.json","w") as data_file:
            self.json.dump(self.CONFIG, data_file, ensure_ascii=False)
        # self.learnPath
