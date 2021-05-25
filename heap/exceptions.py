class HeapError(Exception):
    """ Base class for Heap errors """
    pass

class EmptyKeysError(HeapError):
    """ Raise when keys are empty """
    def __init__(self, message="Keys not given"):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return self.message