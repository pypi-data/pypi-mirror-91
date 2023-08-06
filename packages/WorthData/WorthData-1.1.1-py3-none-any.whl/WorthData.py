import os
from os import path
import json

class databaseError(Exception):
    pass

class get():
    
    def __init__(self, dby_file):
        self.wd = wd_file
        
    def create(self):
        """
        Create a wd file
        """
        if path.exists(f'{self.wd}.wd'):
            raise databaseError('Database already exist')
        else:
            with open(f'{self.wd}.wd','w') as f:
                f.write('{}')

    def access(self):
        """
        Return all data from wd database
        in dict
        """
        if not path.exists(f'{self.wd}.wd'):
            raise databaseError('Database not exist')
        else:
            try:
                with open(f'{self.wd}.wd','r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                with open(f'{self.wd}.wd','w') as f:
                    f.write('{}')
                with open(f'{self.wd}.wd','r') as f:
                    return json.load(f)
    
    def keep(self, data):
        """
        Save data to wd database
        """
        if not path.exists(f'{self.wd}.wd'):
            raise databaseError('Database not exist')
        else:
            try:
                with open(f'{self.wd}.wd','w') as f:
                    json.dump(data,f)
            except json.JSONDecodeError:
                with open(f'{self.wd}.wd','w') as f:
                    f.write('{}')
                    json.dump(data,f)
            return data