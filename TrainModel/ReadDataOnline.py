class ReadDataOnlineAPI():

    def __init__(self):
        from nltk.corpus import PlaintextCorpusReader;
        import os;
        import re;
        import pandas as pd;
        from nltk.corpus import stopwords as sw;
        from nltk.stem.wordnet import WordNetLemmatizer;
        import string;
        from nltk.stem.porter import PorterStemmer;
        import wikipedia as wk;
        from time import time;
        import zipfile

        self.zipfile = zipfile;
        self.os = os;
        self.re = re;
        self.pd = pd;
        self.textReader = PlaintextCorpusReader
        self.stop = set(sw.words('english'))
        self.exclude = set(string.punctuation)
        self.lemma = WordNetLemmatizer()
        self.ps = PorterStemmer()
        self.wk = wk;
        self.time = time;

    def cleanSentence(self,doc):
        stop_free = " ".join([i for i in doc.lower().split() if i not in self.stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in self.exclude)
        #stemming is not required lemmatization is enough
        #normalized = " ".join(self.ps.stem(self.lemma.lemmatize(word)) for word in punc_free.split())
        normalized = " ".join(self.lemma.lemmatize(word) for word in punc_free.split())
        return normalized

    def checkPath(self,s):
        return self.os.path.exists(s)


    def read_from_zip(self,s,extendPath):
        data_path = s+"\\TextData.zip"
        zip = self.zipfile.ZipFile(data_path)

    def readFromFile(self,s,termList=[]):
        p = None
        if self.checkPath(s) is False:
            raise Exception('Path is not correct')
        print("ReadOnlineData->> paths is ",s)
        fileids = [w+".txt" for w in termList]
        wordlists = self.textReader(s, fileids)
        print("ReadOnlineData->> read worldlists",wordlists)
        print(wordlists.fileids())
        classY = list()
        for file in termList:
            p = wordlists.raw(file+".txt").split('\n')
            print(p)
            # term = self.re.search(r'([a-z_]*)', file.lower()).group(1);
            print("ReadOnlineData->> read terms", file)
            if len(classY) == 0:
                classY = [[self.cleanSentence(i), file] for i in p]
            else:
                classY.extend([[self.cleanSentence(i), file] for i in p])

        print('shape of p : ', len(p))
        # print('shape of classY : ',classY)

        data = self.pd.DataFrame(classY, columns=['Sentence', 'Class'])
        print("your dataset >>> ",data)
        return data.sample(frac=1).reset_index(drop=True)


    def readOnline(self,listOfWords=list()):
        if len(listOfWords) == 0:
            raise Exception('Input list of queries')

        p = self.pd.DataFrame(columns=['Sentence', 'Class']);
        # start reading from wikipedia
        t0 = self.time();
        print('Start reading from wiki : ',t0)
        suggestions = list()
        for word in listOfWords:
            suggestions = self.wk.search(word)
            p = p.append(self.pd.DataFrame([[self.cleanSentence(self.wk.summary(w)), word] for w in suggestions],
                                  columns=['Sentence', 'Class']), ignore_index=True)
            print('Reading wikipeadia for suggestion is done : ',suggestions)
        print('Time taken, reading from wiki : ', self.time() - t0)
        return p.sample(frac=1).reset_index(drop=True)
