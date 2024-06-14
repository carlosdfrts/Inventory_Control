'''Criação de erros personalizados para produtos'''

class InvalidProduct(Exception):
    pass

class ExistingProduct(Exception):
    pass

class InvalidPrice(Exception):
    pass