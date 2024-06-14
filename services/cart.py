from services.products import shampoo, lipstick, perfume

class Cart():
    """
    Classe Cart para gerenciar o carrinho de compras.
    
    Atributos:
    - items (list): Lista de dicionários contendo produtos, suas quantidades e preços.
    
    Métodos:
    - add_item(self, product, genere, quantity, price): Adiciona um item ao carrinho.
    - display_cart(self): Exibe o conteúdo do carrinho.
    - get_total(self): Calcula o total do carrinho.
    - checkout(self): Processa a finalização da compra, atualizando o estoque.
    """
    
    def __init__(self) -> None:
        self._items = []
    
    def add_item(self, product : str, quantity : int, price : float ) -> None:
        """
        Adiciona um item ao carrinho.
        
        Parâmetros:
        - product (str): O nome do produto.
        - genere (str): O gênero do produto.
        - quantity (int): A quantidade do produto.
        - price (float): O preço do produto.
        """
        self._items.append({
            'product': product,
            'quantity': quantity,
            'price': price
        })
    
    def get_list(self) -> list:
        """
        Retorna a lista de items do carrinho
        """
        return self._items

    def display_cart(self) -> None:
        """
        Exibe o conteúdo do carrinho.
        
        Retorna:
        - None
        """
        if not self._items:
            print("O carrinho está vazio.")
            return
        
        print("Produtos no carrinho:")
        for item in self._items:
            print(f"{item['product']} - Quantidade: {item['quantity']} - Preço: {item['price']} - Total: {item['quantity'] * item['price']}")
    
    def get_total(self) -> float:
        """
        Calcula o total do carrinho.
        
        Retorna:
        - float: O total do carrinho.
        """
        total = sum(item['quantity'] * item['price'] for item in self._items)
        return total
