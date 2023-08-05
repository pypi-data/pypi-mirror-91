import os, sys, json

class Settings:
    def __init__(self, path='settings.json', **kwargs):
        self.path = path
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                try:
                    self.json = json.load(f)
                except json.decoder.JSONDecodeError:
                    raise Exception(f'Given path for SettingsFile {self.path} is not a valid JSON.')
        else:
            self.json = {}
        self.file = open(self.path, 'w')
        self.file.seek(0)
        self.file.truncate()
        self.file.flush()

    
    def __getitem__(self, key, null=False):
        if null:
            return self.json(key, None)
        else:
            return self.json[key]
        
    
    def __setitem__(self, key, value):
        self.json[key] = value
        self.file.seek(0)
        self.file.truncate()
        json.dump(self.json, self.file)
        self.file.flush()
    
    def __dict__(self):
        return self.json

    def __str__(self):
        return repr(self)
    
    def __repr__(self):
        return f'ConfigFile ({self.path}){self.json!r}'
    
    def __getattr__(self, key):
        if key in ['json', 'file', 'path']:
            return super().__getattr__(key)
        return self.__getitem__(key)
    
    def __setattr__(self, key, value):
        if key in ['json', 'file', 'path']:
            return super().__setattr__(key, value)
        return self.__setitem__(key, value)
