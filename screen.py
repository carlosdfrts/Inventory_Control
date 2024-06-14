from services import cart
from services.products import shampoo, lipstick, perfume
from screenexceptions import *
from view import *
import time

class Screen():
    """
    Classe Screen para gerenciar interações com o usuário relacionadas a produtos.

    Esta classe lida com a exibição de menus e a coleta de entrada do usuário para 
    diferentes operações em produtos, como aumentar ou diminuir estoque, adicionar 
    novos produtos, alterar preços e verificar produtos com estoque zero.

    Métodos:
    - __init__(self): Inicializa a classe Screen.
    - initial_menu(self): Exibe o menu inicial e gerencia a escolha do usuário.
    - _product_menu(self): Exibe o menu de seleção de produtos.
    - _genere_menu(self, product: int): Exibe o menu de seleção de gênero do produto.
    - _print_products(self, genere: str) -> list: Exibe a lista de produtos de um gênero específico.
    - _print_products_details(self, genere: str) -> list: Exibe detalhes de todos os produtos de um gênero específico.
    - _increase_product(self, genere: str): Aumenta a quantidade de um produto.
    - _decrease_stock(self, genere): Diminui a quantidade de um produto.
    - _create_product(self, genere: str): Adiciona um novo produto.
    - _change_product_price(self, genere: str): Altera o preço de um produto.
    - _handle_crud(self, genere: str): Gerencia operações de CRUD com base na escolha inicial do usuário.
    - _handle_unisex(self): Lida com operações em produtos unissex.
    - _handle_male(self): Lida com operações em produtos masculinos.
    - _handle_female(self): Lida com operações em produtos femininos.
    - _handle_child(self): Lida com operações em produtos infantis.
    - _handle_choice(self, genere: int): Chama a função apropriada com base na escolha do usuário.
    - _check_zero_products(self) -> list: Verifica quais produtos estão com quantidade zero.
    - _handle_cart(self): Gerencia o processo de adição de produtos ao carrinho.
    - _add_products_cart(self, genere: str): Adiciona um produto ao carrinho.
    """

    def __init__(self) -> None:
        """
        Inicializa a classe Screen, definindo produtos, variáveis de escolha, e o carrinho.

        Este construtor configura as classes de produtos, inicializa as variáveis de 
        escolha do usuário, configura o mapeamento de ações baseadas nas escolhas e 
        inicializa o objeto do carrinho e a lista de itens do carrinho.
        """
        # Inicializa as classes de produtos
        self._shampoo = shampoo.Shampoo
        self._perfume = perfume.Perfume
        self._lipstick = lipstick.Lipstick

        # Inicializa variáveis de escolha do usuário
        self._initial_choice: int
        self._product_choice: int
        self._genere_choice: int
        self._save_product: object

        # Mapeia escolhas do usuário para os métodos correspondentes
        self._choice_actions = {
            0: self._handle_unisex,
            1: self._handle_male,
            2: self._handle_female,
            3: self._handle_child
        }

        # Inicializa o carrinho de compras
        self._cart = cart.Cart()

         # Lista para armazenar itens do carrinho (produto e gênero) para identificação de filtros pre definidos e localizar o produto
        self._list_cart = []  # Exemplo: [{'product': <produto>, 'genere': <gênero>}]

        self._view = View()


    # Método para exibir o menu de produtos e capturar a escolha do usuário
    def _product_menu(self) -> None:
        itens = ('Shampoo', 'Perfume', 'Batom')
        """
        Exibe o menu de seleção de produtos e gerencia a escolha do usuário.
        """

        while True:
            try:
                self._view.display_header('\033[34mPRODUTO\033[m')
                c = 1
                for item in itens:
                    print(f'''\033[32m{c} - \033[34m{item}\033[m''')
                    c += 1
                print(self._view.draw_line())
                product_choice = int(input("\033[33mDigite sua opção: \033[m"))
                os.system("cls")

                # Verifica se a escolha é válida
                if product_choice not in [1, 2, 3]:
                    raise InvalidChoice("\033[31mOpção inválida! Tente novamente!\033[m")

                # Chama o menu de gênero com base na escolha do produto
                self._genere_menu(product_choice)

                return
            except (InvalidChoice, ValueError):
                print("\033[31mOpção inválida! Tente novamente!\033[m")

    # Método para exibir o menu de gêneros e capturar a escolha do usuário
    def _genere_menu(self, product: int) -> None:
        opcoes = ('Masculino', 'Feminino', 'Infantil')
        """
        Exibe o menu de seleção de gênero do produto e gerencia a escolha do usuário.
        
        Parâmetros:
        - product: O tipo de produto escolhido pelo usuário.
        """

        while True:
            try:
                if product == 1:
                    os.system("cls")
                    self._view.display_header('\033[34mSELECIONE O GENÊRO\033[m')
                    c = 1
                    for item in opcoes:
                        print(f'\033[32m{c} - \033[34m{item}\033[m')
                        c += 1
                    self._save_product = self._shampoo
                    print(self._view.draw_line())
                    genere_choice = int(input("\033[33mDigite sua opção: \033[m"))
                    os.system("cls")
                    if genere_choice not in [1,2,3]: # array com opções válidas
                        raise InvalidChoice("\033[31mOpção inválida! Tente novamente!\033[m")

                elif product == 2:
                    os.system("cls")
                    self._view.display_header('\033[34mSELECIONE A OPÇÃO\033[m')
                    c = 1
                    for item in opcoes:
                        print(f'\033[32m{c} - \033[34m{item}\033[m')
                        c += 1
                    self._save_product = self._perfume
                    print(self._view.draw_line())
                    genere_choice = int(input("\033[33mDigite sua opção: \033[m"))
                    os.system("cls")
                    if genere_choice not in [1,2,3]: # array com opções válidas
                        raise InvalidChoice("\033[31mOpção inválida! Tente novamente!\033[m")

                elif product == 3:
                    self._save_product = self._lipstick
                    genere_choice = 0

                # Processa a escolha do gênero
                self._handle_choice(genere_choice)

                return
            except (InvalidChoice, ValueError):
                raise InvalidChoice("Opção inválida! Tente novamente!")

    # Método para exibir os produtos e capturar a escolha do usuário
    def _print_products(self, genere: str) -> list:
        """
        Exibe a lista de produtos de um gênero específico e coleta a escolha do usuário.
        
        Parâmetros:
        - genere: O gênero dos produtos a serem exibidos.
        
        Retorna:
        - Uma lista com os produtos disponíveis e a escolha do usuário.
        
        Lança:
        - InvalidChoice se a escolha for inválida.
        """
        action = self._save_product(genere)
        list_products = action.all_products()
        index = 0
        self._view.display_header("\033[34mEscolha um produto\033[m")
        for product in list_products:
            index += 1
            print(f'''\033[32m{index} - \033[34m{product}\033[m''')
        try:
            print(self._view.draw_line())
            choice = int(input("\033[33mDigite aqui sua opção: \033[m"))
            if choice <= index and choice > 0:
                return list_products, choice - 1  # retornando a lista e a escolha -1 (array comeca em 0)
            raise InvalidChoice("\033[31mOpção inválida! Tente novamente!\033[m")
        except (InvalidChoice, ValueError):
            raise InvalidChoice("\033[31mOpção inválida! Tente novamente!\033[m")

    # Método para exibir os detalhes dos produtos
    def _print_products_details(self, genere: str) -> list:
        """
        Exibe detalhes de todos os produtos de um gênero específico.
        
        Parâmetros:
        - genere: O gênero dos produtos.
        
        Retorna:
        - Uma lista com detalhes dos produtos.
        """

        action = self._save_product(genere)
        list_products = action.all_products_details()
        return list_products

    # Método para aumentar a quantidade de um produto no estoque
    def _increase_product(self, genere: str):
        """
        Aumenta a quantidade de um produto.
        
        Parâmetros:
        - genere: O gênero do produto.
        """
        
        action = self._save_product(genere)
        products, choice = self._print_products(genere)
        products_details = self._print_products_details(genere)
        os.system("cls")
        self._view.display_header(f"\033[34mDetalhes do produto {products[choice]}\033[m")
        print(products_details[choice])
        while True:
            try:
                print(self._view.draw_line())
                add_quantity = int(input("\033[33mDigite a quantidade que deseja adicionar: \033[m"))
                validate = action.increase_quantity(products[choice], add_quantity)
                if validate:
                    print("\033[32mQuantidade adicionada!\033[m")
                    products_details = self._print_products_details(genere)
                    self._view.display_header(f"\033[34mNovo total: {products_details[choice]}\033[m")
                    sleep(2)
                    os.system("cls")
                    return
            except:
                raise ValueError("Valor inválido, digite um valor válido!")

    def _add_products_cart(self, genere: str) -> None:
        """
        Adiciona um produto ao carrinho de compras com a quantidade especificada.

        Este método permite ao usuário selecionar um produto de um gênero específico,
        visualizar seus detalhes e adicionar uma quantidade desejada ao carrinho. 
        Ele também armazena informações necessárias para atualizar o estoque 
        após a confirmação da compra.

        Parâmetros:
        - genere: O gênero do produto a ser adicionado ao carrinho.

        Lança:
        - ValueError: Se a quantidade fornecida não for válida.
        """
        action = self._save_product(genere)  # Instancia o objeto do produto com base no gênero
        products, choice = self._print_products(genere)  # Exibe os produtos e obtém a escolha do usuário
        products_details = self._print_products_details(genere)  # Obtém os detalhes dos produtos
        os.system("cls")
        self._view.display_header(f"\033[34mDetalhes do produto {products[choice]}\033[m")  # Mostra os detalhes do produto escolhido
        print(products_details[choice])

        while True:
            try:
                cart = self._cart  # Obtém o objeto carrinho
                print(self._view.draw_line())
                quantity = int(input("\033[33mDigite a quantidade que deseja do produto: \033[m"))  # Solicita a quantidade desejada
                price = action.show_price(products[choice])  # Obtém o preço do produto
                cart.add_item(products[choice], quantity, price)  # Adiciona o item ao carrinho
                self._list_cart.append({'product': self._save_product,
                                        'genere': genere})  # Armazena informações para atualização do estoque após a compra
                return  # Sai do loop após adicionar o item ao carrinho
            except ValueError:
                print("Valor inválido, digite um valor válido!")  # Exibe mensagem de erro se a entrada for inválida

            
    # Método para diminuir a quantidade de um produto no estoque (venda)
    def _decrease_stock(self, genere: str) -> None:
        """
        Diminui a quantidade de um produto.
        
        Parâmetros:
        - genere: O gênero do produto.
        """

        action = self._save_product(genere)
        products, choice = self._print_products(genere)
        products_details = self._print_products_details(genere)
        os.system("cls")
        self._view.display_header(f"\033[34mDetalhes do produto {products[choice]}\033[m")
        print(products_details[choice])
        while True:
            try:
                print(self._view.draw_line())
                decrease_quantity = int(input("\033[33mDigite a quantidade que deseja retirar: \033[m"))
                validate = action.decrease_quantity(products[choice], decrease_quantity)
                if validate:
                    print("\033[32mQuantidade retirada!\033[m")
                    products_details = self._print_products_details(genere)
                    print(f"Novo total: {products_details[choice]}")
                    sleep(2)
                    os.system("cls")
                    return
            except:
                    raise ValueError("Valor inválido, digite um valor válido!")
                
    # Método para criar um novo produto
    def _create_product(self, genere: str) -> None:
        """
        Adiciona um novo produto.
        
        Parâmetros:
        - genere: O gênero do produto.
        """

        action = self._save_product(genere)
        while True:
            try:
                product = input("\033[33mDigite o produto: \033[m")
                quantity = int(input("\033[33mDigite a quantidade: \033[m"))
                price = float(input("\033[33mDigite o preço: \033[m"))
                validate = action.add_product(product, quantity, price)
                if validate:
                    print("\033[32mProduto adicionado!\033[m")
                    products = self._print_products_details(genere)
                    print(f"\033[34mNovo produto: \033[m{products[-1]}")
                    return
            except:
                raise ValueError("Valor inválido, digite um valor válido!")

    # Método para alterar o preço de um produto
    def _change_product_price(self, genere: str) -> None:
        """
        Altera o preço de um produto.
        
        Parâmetros:
        - genere: O gênero do produto.
        """

        action = self._save_product(genere)
        products, choice = self._print_products(genere)
        products_details = self._print_products_details(genere)
        os.system("cls")
        self._view.display_header(f"\033[34mDetalhes do produto {products[choice]}\033[m")
        print(products_details[choice])
        while True:
            try:
                price = float(input("\033[33mDigite o novo preço do produto: \033[m"))
                validate = action.edit_price(products[choice], price)
                if validate:
                    print("\033[32mPreço alterado!\033[m")
                    products_details = self._print_products_details(genere)
                    self._view.display_header(f"\033[32mNovo preço: {products_details[choice]}\033[m")
                    sleep(2)
                    os.system("cls")
                    return
            except:
                raise ValueError("\033[31mValor inválido, digite um valor válido!\033[m")

    # Método para lidar com operações CRUD com base na escolha inicial
    def _handle_crud(self, genere: str) -> None:
        """
        Gerencia operações de CRUD com base na escolha inicial do usuário.
        
        Parâmetros:
        - genere: O gênero do produto.
        """
        if self._initial_choice == 1: 
            self._increase_product(genere)
        elif self._initial_choice == 2: 
            self._create_product(genere)
        elif self._initial_choice == 3: 
            self._change_product_price(genere)
        elif self._initial_choice == 4: 
            self._decrease_stock(genere)
        elif self._initial_choice == 5: 
            self._add_products_cart(genere)

    # Métodos para lidar com cada tipo de produto com base no gênero
    def _handle_unisex(self) -> None:
        """
        Lida com operações em produtos unissex.
        """
        self._handle_crud('unisex')

    def _handle_male(self) -> None:
        """
        Lida com operações em produtos masculinos.
        """
        self._handle_crud('masculino')  

    def _handle_female(self) -> None:
        """
        Lida com operações em produtos femininos.
        """
        self._handle_crud('feminino')  

    def _handle_child(self) -> None:
        """
        Lida com operações em produtos infantis.
        """ 
        self._handle_crud('infantil')  

    # Método para lidar com a escolha de gênero usando o dicionário
    def _handle_choice(self, genere : int) -> None:
        """
        Chama a função apropriada com base na escolha do usuário.
        
        Parâmetros:
        - genere: A escolha do gênero feita pelo usuário.
        """
        action = self._choice_actions.get(genere)
        action()  # Executa o método correspondente à escolha do gênero

    # Método para verificar produtos com quantidade zero
    def _check_zero_products(self) -> list:
        """
        Verifica quais produtos estão com quantidade zero.
        
        Retorna:
        - Uma lista de produtos com quantidade zero.
        """
        generes = ['unisex', 'masculino', 'feminino', 'infantil']
        validates = []

        # Verifica shampoo em falta
        shampoo_zero = self._shampoo(generes[1]).check_zero_quantity()
        if shampoo_zero:
            validates.append(f'\033[33mShampoo {generes[1]} em falta:\033[m')
            validates.append(shampoo_zero)

        shampoo_zero = self._shampoo(generes[2]).check_zero_quantity()
        if shampoo_zero:
            validates.append(f'\033[33mShampoo {generes[2]} em falta:\033[m')
            validates.append(shampoo_zero)

        # Verifica batom em falta
        lipstick_zero = self._lipstick(generes[0]).check_zero_quantity()
        if lipstick_zero:
            validates.append('\033[33mBatom em falta:\033[m')
            validates.append(lipstick_zero)

        # Verifica perfume em falta
        perfume_zero = self._perfume(generes[1]).check_zero_quantity()
        if perfume_zero:
            validates.append(f'\033[33mPerfume {generes[1]} em falta:\033[m')
            validates.append(perfume_zero)

        perfume_zero = self._perfume(generes[2]).check_zero_quantity()
        if perfume_zero:
            validates.append(f'\033[33mPerfume {generes[2]} em falta:\033[m')
            validates.append(perfume_zero)

        perfume_zero = self._perfume(generes[3]).check_zero_quantity()
        if perfume_zero:
            validates.append(f'\033[33mPerfume {generes[3]} em falta:\033[m')
            validates.append(perfume_zero)

        return validates
    
    def _handle_cart(self) -> None:
        """
        Gerencia a funcionalidade do carrinho de compras.

        Este método permite que o usuário adicione produtos ao carrinho repetidamente
        até que ele decida parar. Em seguida, ele solicita a confirmação do usuário para
        finalizar a compra e, caso confirmado, atualiza os estoques dos produtos.

        O método utiliza um loop para permitir ao usuário adicionar múltiplos produtos ao
        carrinho e outro loop para confirmar a compra e atualizar o estoque.

        No caso de finalizar a compra:
        - Mostra o total da compra.
        - Pede confirmação do usuário.
        - Atualiza a quantidade dos produtos no estoque.

        Lança:
        - Qualquer exceção ocorrida durante a adição ao carrinho ou atualização do estoque.
        """
        while True:
            try:
                os.system("cls")
                action = self._cart  # Obtém o objeto carrinho
                self._view.display_header('\033[34mCARRINHO DE COMPRAS\033[m')
                self._product_menu()  # Executa a progressão de menus para selecionar o produto
                action.display_cart()  # Exibe os itens atualmente no carrinho
                total = action.get_total()  # Calcula o total da compra
                print(f"\033[33mTotal da compra: {total}\033[m")
                continue_shopping = input("\033[34mDeseja adicionar mais produtos ao carrinho? (s/n): \033[m")
                if continue_shopping.lower() != 's':
                    break
            except Exception as e:
                print(f"\033[31mOcorreu um erro: {e}\033[m")  # Imprime a exceção, se houver
                print(self._view.draw_line())

        while True:
            payment = input("\033[33mDeseja finalizar a compra? (s/n): \033[m")
            if payment.lower() != 's':
                return  # Se o usuário não quiser finalizar a compra, retorna ao menu inicial
            else: 
                print('\033[32mCompra Efetuada com sucesso!\033[m')
                sleep(1)
            index = 0  # Variável de controle para iterar sobre os itens do carrinho
            cart_item_list = self._cart.get_list()  # Obtém a lista de produtos do carrinho
            for items in self._list_cart:  # Itera sobre os itens armazenados em list_cart
                action = items['product']  # Obtém o objeto produto (self._save_product)
                genere = items['genere']  # Obtém o gênero do produto
                product_type = cart_item_list[index]['product']  # Nome do produto no carrinho
                decrease_quantity = cart_item_list[index]['quantity']  # Quantidade do produto no carrinho
                action(genere).decrease_quantity(product_type, decrease_quantity)  # Atualiza a quantidade do produto no estoque
                index += 1  # Incrementa o índice para o próximo item do carrinho
            
            return  # Retorna ao menu inicial após finalizar a compra


    # Método inicial para exibir o menu principal e capturar a escolha do usuário
    def initial_menu(self) -> None:
        opcao = ('Adicionar produto já existente ao estoque', 'Adicionar um novo produto ao estoque', 'Alterar preço de um produto', 'Retirar um item do estoque', 'Vender um produto')
        """
        Exibe o menu inicial e gerencia a escolha do usuário.
        """

        while True:
            validates = self._check_zero_products()
            if validates:
                for zero_products in validates:
                    print(zero_products)
                    sleep(0.5)
            try:
                sleep(1)
                os.system("cls")
                self._view.display_header('\033[34mMENU PRINCIPAL\033[m')
                c = 1
                for item in opcao:
                    print(f'''\033[32m{c} - \033[34m{item}\033[m''')
                    c += 1
                print(self._view.draw_line())
                self._initial_choice = int(input("\033[33mDigite aqui sua opção: \033[m"))
                os.system("cls")
                if self._initial_choice not in [1, 2, 3, 4, 5]:
                    print("\033[31mOpção inválida! Tente novamente!\033[m")
                    sleep(1)
                    return
                if self._initial_choice == 5:
                    self._handle_cart()
                
                else:
                    self._product_menu()
                return
            
            except (InvalidChoice, ValueError):
                print("\033[31mOpção inválida! Tente novamente!\033[m]")
                sleep(1)
                return
