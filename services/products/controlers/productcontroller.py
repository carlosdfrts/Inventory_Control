from .controller import *
from .productsexceptions import *

class ProductController(Controller):
    """
    Classe ProductController para gerenciar operações relacionadas a produtos.
    
    Esta classe herda de Controller e lida com produtos de diferentes gêneros,
    permitindo editar preços, aumentar e diminuir quantidades, adicionar novos produtos,
    verificar produtos com quantidade zero e listar todos os produtos e seus detalhes.

    Métodos:
    - __init__(self, gender, product): Inicializa o controlador com o gênero e o produto específicos.
    - show_price(self, type: str) -> float: Retorna o preço do produto
    - edit_price(self, type: str, price: float) -> bool: Edita o preço de um tipo de produto.
    - increase_quantity(self, type: str, quantity_increase: int) -> bool: Aumenta a quantidade de um tipo de produto.
    - decrease_quantity(self, type: str, quantity_decrease: int) -> bool: Diminui a quantidade de um tipo de produto.
    - add_product(self, type: str, quantity: int, price: float) -> bool: Adiciona um novo produto.
    - check_zero_quantity(self) -> bool: Verifica produtos com quantidade zero.
    - all_products(self) -> list: Retorna uma lista de todos os tipos de produtos.
    - all_products_details(self) -> list: Retorna uma lista com detalhes de todos os produtos.
    """
    
    def __init__(self, gender, product) -> None:
        """
        Inicializa o controlador com o gênero e o produto específicos.
        
        Parâmetros:
        - gender: O gênero do produto (masculino, feminino, etc.).
        - product: O tipo de produto (shampoo, perfume, etc.).
        """
        super().__init__()
        self._gender = gender  # Gênero do produto
        self._product = product  # Tipo de produto

    def show_price(self, type: str) -> float:
        """
        Retorna o preço de um produto.
        
        Parâmetros:
        - type: O tipo específico de produto (ex. "Shampoo Anti-Caspa").
        
        Retorna:
        - O preço do produto buscado
        
        Lança:
        - InvalidProduct se o produto não for encontrado.
        """

        data = self.load_json()  # Carrega os dados do arquivo JSON
        try:
            return data[self._product][self._gender][type]['preco'] # Retorna o preço do produto
        except InvalidProduct:
            raise InvalidProduct("Produto não encontrado!")  # Lança exceção se o produto não for encontrado

    def edit_price(self, type: str, price: float) -> bool:
        """
        Edita o preço de um tipo de produto.
        
        Parâmetros:
        - type: O tipo específico de produto (ex. "Shampoo Anti-Caspa").
        - price: O novo preço a ser definido.
        
        Retorna:
        - True se o preço foi editado com sucesso.
        
        Lança:
        - InvalidPrice se o preço for 0 ou menor.
        - InvalidProduct se o produto não for encontrado.
        """
        data = self.load_json()  # Carrega os dados do arquivo JSON
        try:
            if price > 0:
                data[self._product][self._gender][type]['preco'] = price  # Atualiza o preço do produto
                self.save_json(data)  # Salva os dados atualizados
                return True
            else:
                raise InvalidPrice("O preço não pode ser 0 ou menor!")  # Lança exceção se o preço for inválido
        except InvalidProduct:
            raise InvalidProduct("Produto não encontrado!")  # Lança exceção se o produto não for encontrado

    def increase_quantity(self, type: str, quantity_increase: int) -> bool:
        """
        Aumenta a quantidade de um tipo de produto.
        
        Parâmetros:
        - type: O tipo específico de produto (ex. "Shampoo Anti-Caspa").
        - quantity_increase: A quantidade a ser adicionada.
        
        Retorna:
        - True se a quantidade foi aumentada com sucesso.
        
        Lança:
        - InvalidProduct se o produto não for encontrado.
        """
        data = self.load_json()  # Carrega os dados do arquivo JSON
        try:
            data[self._product][self._gender][type]['quantidade'] += quantity_increase  # Atualiza a quantidade do produto
            self.save_json(data)  # Salva os dados atualizados
            return True
        except InvalidProduct:
            raise InvalidProduct("Produto não encontrado!")  # Lança exceção se o produto não for encontrado

    def decrease_quantity(self, type: str, quantity_decrease: int) -> bool:
        """
        Diminui a quantidade de um tipo de produto.
        
        Parâmetros:
        - type: O tipo específico de produto (ex. "Shampoo Anti-Caspa").
        - quantity_decrease: A quantidade a ser removida.
        
        Retorna:
        - True se a quantidade foi diminuída com sucesso.
        
        Lança:
        - InvalidProduct se o produto não for encontrado.
        """
        data = self.load_json()  # Carrega os dados do arquivo JSON
        try:
            current_quantity = data[self._product][self._gender][type]['quantidade']  # Quantidade atual do produto
            if quantity_decrease >= current_quantity:
                # Se a quantidade a ser removida for maior ou igual à quantidade atual, define a quantidade como 0
                data[self._product][self._gender][type]['quantidade'] = 0
                self.save_json(data)  # Salva os dados atualizados
                return True
            else:
                # Caso contrário, subtrai a quantidade a ser removida
                data[self._product][self._gender][type]['quantidade'] -= quantity_decrease
                self.save_json(data)  # Salva os dados atualizados
                return True
        except InvalidProduct:
            raise InvalidProduct("Produto não encontrado!")  # Lança exceção se o produto não for encontrado

    def add_product(self, type: str, quantity: int, price: float) -> bool:
        """
        Adiciona um novo produto.
        
        Parâmetros:
        - type: O tipo específico de produto (ex. "Shampoo Anti-Caspa").
        - quantity: A quantidade inicial do produto.
        - price: O preço do produto.
        
        Retorna:
        - True se o produto foi adicionado com sucesso.
        
        Lança:
        - ExistingProduct se o produto já existir.
        - InvalidProduct se o produto não for encontrado.
        """
        data = self.load_json()  # Carrega os dados do arquivo JSON
        try:
            if type not in data[self._product][self._gender]:
                # Adiciona o novo produto se ele ainda não existir
                data[self._product][self._gender][type] = {'quantidade': quantity, 'preco': price}
                self.save_json(data)  # Salva os dados atualizados
                return True
            else:
                raise ExistingProduct("Já existe este produto, tente adicionar quantidade ao estoque!")  # Lança exceção se o produto já existir
        except InvalidProduct:
            raise InvalidProduct("Produto inválido!")  # Lança exceção se o produto não for encontrado

    def check_zero_quantity(self) -> list:
        """
        Verifica produtos com quantidade zero.
        
        Retorna:
        - Uma lista de produtos com quantidade zero.
        
        Lança:
        - InvalidProduct se o produto não for encontrado.
        """
        data = self.load_json()  # Carrega os dados do arquivo JSON
        zero_products = []
        try:
            # Itera sobre os produtos para verificar se a quantidade é zero
            for product_type, product_info in data[self._product][self._gender].items():
                if product_info['quantidade'] == 0:
                    zero_products.append(product_type)
            return zero_products
        except:
            raise InvalidProduct("Produto não encontrado!")  # Lança exceção se o produto não for encontrado

    def all_products(self) -> list:
        """
        Retorna uma lista de todos os tipos de produtos.
        
        Retorna:
        - Uma lista de strings, onde cada string é um tipo de produto.
        """
        data = self.load_json()  # Carrega os dados do arquivo JSON
        products = []
        # Adiciona todos os tipos de produtos na lista
        for product_type in data[self._product][self._gender]:
            products.append(product_type)
        return products

    def all_products_details(self) -> list:
        """
        Retorna uma lista com detalhes de todos os produtos.
        
        Retorna:
        - Uma lista de tuplas, onde cada tupla contém o tipo de produto e suas informações.
        """
        data = self.load_json()  # Carrega os dados do arquivo JSON
        products = []
        # Adiciona os detalhes de todos os produtos na lista
        for product_type in data[self._product][self._gender].items():
            products.append(product_type)
        return products
