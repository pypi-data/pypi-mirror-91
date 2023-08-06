import json
from .utils import is_vivp_file
"""
{
    'packageDetails': {
        'packageName' : '',
        'packageAuthors' : [],
    },
    'packageURL': '',
    'fileList': [],
    'testBench': [],
    'dependencyList': []
}
"""

class vPackage:
    """
    vPackage
    """
    def __init__(self, data=None, filePath=False, saveable=False, createNew=False):
        if filePath and not data:       # filePath is provided
            self.filePath = filePath
            self.saveable = saveable
            
            if is_vivp_file(filePath):    # load from filePath
                with open(filePath) as f:
                    self.data = json.load(f)
            elif createNew:             # create new
                self.data = self.getBlankPackageData()
                self.save()
            else:
                raise Exception("Not a vPackage")
        
        elif data and not filePath:     # data is provided
        
            if saveable:
                raise Exception("vPackage without filePath is not saveable")
            self.data = data
            self.filePath = False
            self.saveable = False
        else:
            raise Exception("vPackage initializes with either data or filePath, not both")
        pass

    def load(self):
        with open(self.filePath) as f:
            self.data = json.load(f)

    def save(self):
        if not self.saveable:
            raise Exception("Write attempt to write protected package")
        
        # Save to self.filePath
        with open(self.filePath, 'w') as json_file:
            json.dump(self.data, json_file)

    def getBlankPackageData(self):
        return {
            'packageDetails': {
                'packageName' : '',
                'packageAuthors' : [],
            },
            'packageURL': '',
            'fileList': [],
            'testBench': [],
            'dependencyList': []
        }
    
    def has_dependency(self, d):
        for dep in self.data['dependencyList']:
            if d == dep:
                return True
        return False

    def __repr__(self):
        return "vPackage()"
    
    def __str__(self):
        return json.dumps(self.data, indent=4, sort_keys=True)
        