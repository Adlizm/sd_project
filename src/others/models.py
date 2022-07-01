import json

class DataClient():
    def __init__(self, name, age):
        self.name = str(name)
        self.age = int(age)

    def to_string(self):
        return json.dumps(self.__dict__)
    
    staticmethod
    def from_string(data):
        obj = json.loads(data)
        return DataClient(obj['name'], obj['age'])


class DataTask():
    def __init__(self, description):
        self.description = str(description)

    def to_string(self):
        return json.dumps(self.__dict__)
    
    staticmethod
    def from_string(data):
        obj = json.loads(data)
        return DataTask(obj['description'])  
