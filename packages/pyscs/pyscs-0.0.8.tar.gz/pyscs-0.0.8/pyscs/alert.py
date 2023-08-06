# encoding=utf-8
from pyscs.script import AlertTo

class Alert():
    def __init__(self):
        self.title = ""
        self.pname = ""
        self.name = ""
        self.reason = ""
        self.broken = False
        self.interval = 10
        self.to = AlertTo()
        
        
    def dump(self):
        alert = self.__dict__
        alert["to"] = self.to.__dict__
        # self.to = self.to.__dict__
        return alert
        # return json.dumps(self.__dict__)
    
