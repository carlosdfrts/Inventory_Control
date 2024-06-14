from .controlers.productcontroller import *

class Perfume(ProductController):
    def __init__(self, genere) -> None:
        super().__init__(genere, 'perfume')