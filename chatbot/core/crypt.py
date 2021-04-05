import base64
import string
import random
from math import ceil

class Crypt:

    _default_glyphs = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    _default_key = "7umMxvi9DTQFSGdXEhasHNJ5OlbeyPrf2jAIBZocp40LnUWwzCVkgRt6K8q13Y"
    
    def __init__(self, text:str,key:str=_default_key,glyphs:str=_default_glyphs,encoding:str='utf-8'):
        self._text = str(text)
        self._key = key
        self._glyphs = glyphs
        self._encoding = encoding

    def __call__(self)->str:
        return self._text

    def __str__(self)->str:
        return self._text

    def key(self,key):
        self._key = key
        return self

    def glyphs(self,glyphs):
        self._glyphs = glyphs
        return self

    def random(self,length=6,idx=None):
        ran = ''.join(random.choices(string.ascii_letters + string.digits, k = length))
        self._text = self._text+ran if idx ==None else self._text[:idx]+ran+self._text[idx:]
        return self
    @property 
    def prependrandom(self): return self.random(idx=0)
    @property
    def appendrandom(self): return self.random()
    @property 
    def appendrandom10(self): return self.random(idx=0,length=10)
    @property
    def prependrandom10(self): return self.random(length=10)

    def removestr(self,length=6,idx=None):
        self._text=self._text[:-length] if idx==None else self._text[:idx]+self._text[idx+length:]
        return self
    @property 
    def removestrstart(self): return self.removestr(idx=0)
    @property
    def removestrend(self): return self.removestr()
    @property 
    def removestrstart10(self): return self.removestr(idx=0,length=10)
    @property
    def removestrend(self): return self.removestr(length=10)

    @property
    def hash(self):
        self._text = str(abs(hash(tuple(self._text))))
        return self
    
    
class Encrypt(Crypt):

    def _base64(self,url=False,strip=False):
        self._text = base64.urlsafe_b64encode(self._text.encode(self._encoding)).decode(self._encoding) if url else base64.b64encode(self._text.encode(self._encoding)).decode(self._encoding)
        if strip: self._text = self._text.rstrip('=')
        return self

    @property
    def base64(self): return self._base64()
    @property
    def base64strip(self): return self._base64(strip=True)
    @property
    def base64url(self): return self._base64(url=True)
    @property
    def base64urlstrip(self): return self._base64(url=True,strip=True)

    @property
    def substitution(self):
        keyMap = dict(zip(self._glyphs, self._key))
        self._text = ''.join(keyMap.get(c, c) for c in self._text)
        return self
    

class Decrypt(Crypt):

    def _base64(self,url=False,strip=False):
        if strip: self._text = self._text.ljust(ceil(len(self._text) / 4) * 4, '=') #unstriped
        self._text = base64.urlsafe_b64decode(self._text).decode(self._encoding) if url else base64.b64decode(self._text).decode(self._encoding)
        return self
    
    @property
    def base64(self): return self._base64()
    @property
    def base64strip(self): return self._base64(strip=True)
    @property
    def base64url(self): return self._base64(url=True)
    @property
    def base64urlstrip(self): return self._base64(url=True,strip=True)

    @property
    def substitution(self):
        keyMap = dict(zip(self._key, self._glyphs))
        self._text = ''.join(keyMap.get(c, c) for c in self._text)
        return self