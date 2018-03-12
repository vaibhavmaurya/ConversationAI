class ClassifyText:
    def __init__(self, list_of_texts: object, online: object) -> object:
        from sklearn.externals import joblib
        from TrainModel import ReadDataOnline
        import json

        self.joblib = joblib
        self.ReadDataOnline = ReadDataOnline
        self.cVectorization = None
        self.cTfidfVectorization = None
        self.clfSGD = None
        self.list_of_texts = list_of_texts
        self.learnPath = ""
        self.datapath = ""
        self.modelpath = ""
        self.online = online
        self.prediction = None
        self.decision_class = {}
        self.CONFIG = None
        with open(".\\config\\config.json") as data_file:
            self.CONFIG = json.load(data_file)

        with open(".\\config\\learnPath.json") as data_file:
            self.learnPath = json.load(data_file)
            self.datapath = ".\\FeatureExtraction\\Data"
            self.modelpath = ".\\Model"
        if self.CONFIG["MODEL_LEARNT"] == "X":
            self.setClassifier()

    def setClassifier(self,extend_path=None):
        if extend_path:
            self.datapath = self.datapath+"\\"+extend_path
            self.modelpath = self.modelpath+"\\"+extend_path

        print("ClassifyText->> new datapath : ", self.datapath)
        print("ClassifyText->> new modelpath : ", self.modelpath)
        if self.online:
            print('From online data')
            self.cVectorization = self.joblib.load(self.datapath+"\\CountVectorizationOnline.pkl")
            self.cTfidfVectorization = self.joblib.load(self.datapath+"\\TfIdfVectorizationOnline.pkl")
            self.clfSGD = self.joblib.load(self.modelpath+"\\SGDModelFromFileO.pkl")
        else:
            print('Not From online data')
            self.cVectorization = self.joblib.load(self.datapath+"\\CountVectorization.pkl")
            self.cTfidfVectorization = self.joblib.load(self.datapath+"\\TfIdfVectorization.pkl")
            self.clfSGD = self.joblib.load(self.modelpath+"\\SGDModelFromFile.pkl")


    def classify_text(self):

        if self.CONFIG["MODEL_LEARNT"] == "":
            return ""
        rd = self.ReadDataOnline.ReadDataOnlineAPI()
        # testDoc = ['I want to transfer money', 'What is my account balance', '']
        cleanTestDoc = [rd.cleanSentence(doc) for doc in self.list_of_texts]

        print('After cleaning: ', cleanTestDoc)
        tfDoc = self.cTfidfVectorization.transform(self.cVectorization.transform(cleanTestDoc))
        prediction = self.clfSGD.predict(tfDoc).tolist()
        self.decision_class[prediction[0]] = self.clfSGD.decision_function(tfDoc)
        print('Prediction not online : ', prediction)
        self.prediction = prediction
        e = self.learnPath.get(prediction[0])
        if e:
           print("ClassifyText->> found further class : ",e)
           self.setClassifier(extend_path=prediction[0]+"_")
           self.prediction = self.classify_text()
        print("ClassifyText->> you prediction : ",self.prediction)
        return self.prediction

    def get_decision_function(self):
        return self.decision_class

    def get_class_params(self):
        return self.clfSGD.classes_