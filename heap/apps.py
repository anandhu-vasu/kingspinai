from django.apps import AppConfig
from .exceptions import *

class Heap(AppConfig):
    """ Temporay Global Memory Space for Django apps  """
    name = 'heap'
    _heap= {}
    
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
        heap = cls._heap
        
        for i,key in enumerate(keys):
            if i<last_index:
                if key not in heap:
                    heap[key] = {}
                heap = heap[key]
            else:
                heap[key] = val

    @classmethod
    def get(cls,*keys:str,safe:bool=True):
        """ Returns the value for the key.\n
            Default[safe=True] : Returns None if key doesn't exist.
        """
        
        last_index =len(keys)-1
        if last_index < 0:
            raise EmptyKeysError()
        
        keys = cls._flatten_keys(keys)
        heap = cls._heap
        for i,key in enumerate(keys):
            if safe:
                if key not in heap:
                    return
            if i<last_index:
                heap = heap[key]
            else:
                return heap[key]



    @classmethod
    def pop(cls,*keys:str,safe:bool=True)->None:
        """ Remove exact end key/value pair from Heap. """
        
        last_index =len(keys)-1
        if last_index < 0:
            raise EmptyKeysError()
        
        keys = cls._flatten_keys(keys)
        heap = cls._heap
        for i,key in enumerate(keys):
            if safe:
                if key not in heap:
                    return
            if i<last_index:
                heap = heap[key]
            else:
                del heap[key]
                
    @classmethod
    def rub(cls,*keys:str,safe:bool=True)->None:
        """ Remove key/value pair from Heap recursively from end until a non empty key is found. """
        
        last_index =len(keys)-1
        if last_index < 0:
            raise EmptyKeysError()
        
        keys = cls._flatten_keys(keys)
           
        def _rub(heap,i=0):
            if safe:
                if keys[i] not in heap:
                    return
            if i<last_index:
                _rub(heap[keys[i]],i+1)
                if len(heap[keys[i]]) == 0:
                    del heap[keys[i]]
            else:
                del heap[keys[i]]
        
        _rub(cls._heap)
        
    @classmethod
    def dict(cls)->dict:
        """ Returns dictionary of heap """
        return cls._heap
        
    @classmethod
    def wipe(cls)->None:
        """ Clear the Heap """
        cls._heap.clear()
