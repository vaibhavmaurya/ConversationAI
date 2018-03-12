class HandleDataType:
    def __init__(self):
        import datetime
        self.datetime = datetime
        self.type_list = ["string","decimal","integer","date","expression"]

    def handle_string(self):
        return ""

    def handle_decimal(self):
        return 0.0

    def handle_integer(self):
        return 0

    def handle_date(self):
        self.datetime.datetime.today().strftime("%Y%m%d")

    def get_type_default(self,types):
        return self["handle_"+types]()
