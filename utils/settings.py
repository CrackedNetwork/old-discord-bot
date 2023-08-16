import json
import os

class Settings:
    def __init__(self):
        if not os.path.exists("./settings.json"):
            with open("./settings.json", "w") as f:
                f.write("{}")
        self.settings = json.load(open("./settings.json", "r"))
    
    def get(self, key: str):
        keys = key.split('.')
        obj = self.settings
        for k in keys:
            obj = obj.get(k, None)
            if obj is None:
                break
        return obj
    
    def set(self, key: str, value):
        keys = key.split('.')
        obj = self.settings
        for k in keys[:-1]:
            if k not in obj:
                obj[k] = {}
            obj = obj[k]
        obj[keys[-1]] = value
        json.dump(self.settings, open("./settings.json", "w"), indent=4)

