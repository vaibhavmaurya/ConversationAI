class TextLexicalParser:
    def __init__(self):
        import json
        import ServiceHandler.HandleDataType as hd
        import os

        self.handle_type = hd.HandleDataType()
        self.CONFIG = None
        self.service_data = None
        self.service_name = ""
        self.service_obj = None
        self.operation = ""
        self.service_ops = None
        self.service_atts_vals = {}
        self.no_service = False
        self.os = os
        self.json = json

        type_list = ["integer","decimal","string","date","expression"]
        with open(".\\config\\config.json") as config_file:
            self.CONFIG = json.load(config_file)
            if self.os.path.exists(self.CONFIG["service path"]):
                with open(self.CONFIG["service path"]) as service_file:
                    self.service_data = json.load(service_file)
                    self.no_service = True
            else:
                self.no_service = False

    def reload_service(self):
        if self.os.path.exists(self.CONFIG["service path"]):
            print("reload_service->> File is there")
            with open(self.CONFIG["service path"]) as service_file:
                self.service_data = self.json.load(service_file)
        else:
            print("reload_service->> File is there")
            self.service_data = data = {"service":{}}

    def set_service_handler(self,name):
        if not self.no_service:
            return False
        self.service_name = name
        if name not in self.service_data["service"]:
            return False
        self.service_obj = self.service_data["service"][name]
        if len(self.service_obj["operations"]) == 1:
            self.operation = self.service_obj["operations"][0]
        if self.operation is not "":
            print("self.operation is : ",self.operation)
            self.service_ops = self.service_obj[self.operation]
        return True

    def set_service_atts(self,atts):
        self.service_atts_vals = atts

    def get_service_ops(self):
        return self.service_ops

    def _extend_service(self):
        if self.service_obj["inherits"] in self.service_data["service"]:
            obj_parent = self.service_data["service"][self.service_obj["inherits"]]
            self.service_obj["keys"] = list(set(self.service_obj["keys"]+obj_parent["keys"]))
            self.service_obj["attributes"].update(obj_parent["attributes"])

    def parse_text(self,text):
        if not self.service_obj:
            return {}
        l_attributes = list(self.service_obj["attributes"])
        l_keys = self.service_obj["keys"]
        if self.service_obj["inherits"] is not None:
            self._extend_service()
        return {
            "keys":self.service_obj["keys"],
            "attributes":self.service_obj["attributes"]
        }
        # if self.service_atts_vals == {}:
        #     self.service_atts_vals = {w:None for w in l_attributes}
        # for p in l_keys:
        #     if self.service_atts_vals[p] is None or not self.service_atts_vals["solved"]:
        #        self.service_atts_vals[p] = self._extract_attribute_val(p,text)

    # def _extract_attribute_val(self,att,text):
    #     # basic work is here
    #     att_obj = self.service_ops["attributes"][att]
    #     att_response = {"solved": False, "value": None, "query statement":att_obj["query statement"]}
    #     if att_response["type"] is not "expression":
    #         att_response["value"] = self.handle_type.get_type_default(att_response["type"])
    #     # Here is the complexity
    #     if att_response["multipleValues"] == "False":
    #         if att_response["type"] == "expression":