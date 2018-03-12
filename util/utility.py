class utility_functions:
    def __init__(self):
        import os
        import shutil
        import json
        
        self.os = os
        self.shutil = shutil
        self.json = json
        self.CONFIG = None
        with open("./config/config.json") as config_file:
            self.CONFIG = self.json.load(config_file)

    def reset_folder(self,folder_path):
        if self.os.path.exists(folder_path):
            for file_object in self.os.listdir(folder_path):
                file_object_path = self.os.path.join(folder_path, file_object)
                if self.os.path.isfile(file_object_path):
                    self.os.unlink(file_object_path)
                else:
                    self.shutil.rmtree(file_object_path)

    def reset_models(self):
        self.reset_folder(self.CONFIG["DATA_PATH"])
        self.CONFIG["MODEL_LEARNT"] = ""
        with open("./config/config.json","w") as config_file1:
            self.json.dump(self.CONFIG, config_file1, ensure_ascii=False)
        # reset Vocabulary
        self.reset_folder("./Vocabulary")
        self.reset_folder("./Model")
        self.reset_folder("./FeatureExtraction/Data")
        self.reset_service()

    def reset_service(self):
        file_path = self.CONFIG["service path"]
        data = {"service":{}}
        if self.os.path.isfile(file_path):
            self.os.unlink(file_path)
        # with open(file_path,"w+") as service_file:
        #     self.json.dump(data, service_file, ensure_ascii=False)