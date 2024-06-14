from .controlers.productcontroller import *

class Lipstick(ProductController):
    def __init__(self, genere) -> None:
        super().__init__(genere, 'batom')