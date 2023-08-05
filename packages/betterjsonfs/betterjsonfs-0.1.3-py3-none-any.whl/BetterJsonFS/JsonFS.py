from pathlib import Path
import json
import time
import base64
from functools import reduce
import operator
import re
import sys
import copy
import gc

#Exceptions
class FileTooBig(Exception): pass # for actual file
class VirtualFileTooBig(Exception): pass # for self.FsJson
class FileNotJson(Exception): pass # if the file is not json readable
class FileNotFound(Exception): pass # file not found in self.FsJson 
class FileCorrupted(Exception): pass
class WriteError(Exception): pass
class ReadOnly(Exception): pass


#actual stuff
class jsonfs:
    """
    do setup stuff

    :FsFile: path to FileSystem json file
    :MaxSize: maximum acceptable size of FsFile in MiB; Set to -1 for unlimited
    :ReadOnly: if FileSystem is to be read only
    """    
    
    def __init__(self, FsFile:str="FS.json", MaxSize:int=32, ReadOnly:bool=False):
        if MaxSize == -1:
            self.MaxSize = float("inf")
            MaxSize = float("inf")
        else: self.MaxSize = int(MaxSize * 1.049e+6)
        self.FsJson = self.Internal.loadFS(self.Internal, FsFile, self.MaxSize)
        self.FsFileName = FsFile
        self.ReadOnly = ReadOnly

    class Internal:
        #stolen from https://stackoverflow.com/a/53705610
        def get_obj_size(self, obj):
            marked = {id(obj)}
            obj_q = [obj]
            sz = 0
            while obj_q:
                sz += sum(map(sys.getsizeof, obj_q))
                all_refr = ((id(o), o) for o in gc.get_referents(*obj_q))
                new_refr = {o_id: o for o_id, o in all_refr if o_id not in marked and not isinstance(o, type)}
                obj_q = new_refr.values()
                marked.update(new_refr.keys())
            return sz

        def loadFS(self, FsFile:str, MaxSize):
            if not Path(FsFile).is_file():
                with open(FsFile, "w") as f:
                    f.write(json.dumps({
                        "jsonfs":{
                            "version":0.2
                        },
                        "FS":{}
                    }))
                    f.close()
            if Path(FsFile).stat().st_size > MaxSize: #if file is bigger than maxsize
                raise FileTooBig("File size over " + str(MaxSize) + "MiB File size: " + str(Path(FsFile).stat().st_size))
            try: return json.loads(open(FsFile, "r").read())
            except json.decoder.JSONDecodeError:
                raise FileNotJson

        def saveFS(self, FsFile:str, FsJson:dict, ReadOnly:bool):
            if ReadOnly:
                raise ReadOnly
            try:
                with open(FsFile, "w") as f:
                    f.write(json.dumps(FsJson))
            except IOError: raise WriteError

        def saveInJson(self, FsJson, path, content):
            if type(content) == str:
                content = content.encode()
            FsJson["FS"][path] = base64.b64encode(content)

        def getPathFromJson(self, FsJson, path):
            return base64.b64decode(FsJson["FS"][
                base64.b64encode(path.encode()).decode() # encode the path into base64 and decode it back into a normal string
                ].encode())

    def read(self, path:str):
        """
        Read file from filesystem
        """
        try: return self.Internal.getPathFromJson(self.Internal, self.FsJson, path)
        except KeyError:
            raise FileNotFound
        except base64.binascii.Error:
            raise FileCorrupted

    
    def write(self, path:str, content):
        """
        Write to the filesystem
        """
        FsJsontemp = copy.deepcopy(self.FsJson)
        if type(content) == str: content = content.encode()
        FsJsontemp["FS"][base64.b64encode(path.encode()).decode()] = base64.b64encode(content).decode()
        if self.Internal.get_obj_size(self.Internal, FsJsontemp) > self.MaxSize:
            raise VirtualFileTooBig
        self.FsJson = FsJsontemp
        self.Internal.saveFS(self.Internal, self.FsFileName, self.FsJson, self.ReadOnly)

    def remove(self, path:str):
        """
        Remove from the filesystem
        """
        try: self.FsJson["FS"].pop(base64.b64encode(path.encode()).decode())
        except KeyError: raise FileNotFound
        self.Internal.saveFS(self.Internal, self.FsFileName, self.FsJson, self.ReadOnly)
    
    def checkifexists(self, path:str):
        """
        check if path exists
        """
        try:
            if base64.b64encode(path.encode()).decode() in self.FsJson["FS"]:
                return True
            return False
        except KeyError:
            raise FileNotFound