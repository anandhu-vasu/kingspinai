from django.apps import AppConfig
from .exceptions import *

class Hoard(AppConfig):
    """ Temporay Global Memory Space for Django apps  """
    name = 'hoard'
    _hoard= {}
    
    @classmethod
    def _flatten_keys(cls,keys:list):
        return [k for s in keys for k in s.split('.')]

    @classmethod
    def set(cls,*keys:str,val)->None:
        """ Set value to key"""
        
        last_index =len(keys)-1
        if last_index < 0:
            raise EmptyKeysError()
        
        keys = cls._flatten_keys(keys)
        hoard = cls._hoard
        
        for i,key in enumerate(keys):
            if i<last_index:
                if key not in hoard:
                    hoard[key] = {}
                hoard = hoard[key]
            else:
                hoard[key] = val

    @classmethod
    def get(cls,*keys:str,safe:bool=True):
        """ Returns the value for the key.\n
            Default[safe=True] : Returns None if key doesn't exist.
        """
        
        last_index =len(keys)-1
        if last_index < 0:
            raise EmptyKeysError()
        
        keys = cls._flatten_keys(keys)
        hoard = cls._hoard
        for i,key in enumerate(keys):
            if safe:
                if key not in hoard:
                    return
            if i<last_index:
                hoard = hoard[key]
            else:
                return hoard[key]



    @classmethod
    def pop(cls,*keys:str,safe:bool=True)->None:
        """ Remove exact end key/value pair from hoard. """
        
        last_index =len(keys)-1
        if last_index < 0:
            raise EmptyKeysError()
        
        keys = cls._flatten_keys(keys)
        hoard = cls._hoard
        for i,key in enumerate(keys):
            if safe:
                if key not in hoard:
                    return
            if i<last_index:
                hoard = hoard[key]
            else:
                del hoard[key]
                
    @classmethod
    def rub(cls,*keys:str,safe:bool=True)->None:
        """ Remove key/value pair from hoard recursively from end until a non empty key is found. """
        
        last_index =len(keys)-1
        if last_index < 0:
            raise EmptyKeysError()
        
        keys = cls._flatten_keys(keys)
           
        def _rub(hoard,i=0):
            if safe:
                if keys[i] not in hoard:
                    return
            if i<last_index:
                _rub(hoard[keys[i]],i+1)
                if len(hoard[keys[i]]) == 0:
                    del hoard[keys[i]]
            else:
                del hoard[keys[i]]
        
        _rub(cls._hoard)
        
    @classmethod
    def dict(cls)->dict:
        """ Returns dictionary of hoard """
        return cls._hoard
        
    @classmethod
    def wipe(cls)->None:
        """ Clear the hoard """
        cls._hoard.clear()
