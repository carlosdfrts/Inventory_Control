from .controlers.productcontroller import *

class Shampoo(ProductController):
    def __init__(self, genere) -> None:
        super().__init__(genere, 'shampoo')
