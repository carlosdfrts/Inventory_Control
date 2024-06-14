from time import sleep
import os

class View:
    """
    Classe View para exibição de menus e cabeçalhos.

    Métodos:
    --------
    draw_line() -> str:
        Retorna uma linha de caracteres '-' com o tamanho especificado.
        
    display_header(text: str) -> None:
        Exibe um cabeçalho centrado com uma linha acima e abaixo.
        
    display_menu(options: list) -> str:
        Exibe um menu com opções numeradas e solicita uma entrada do usuário.
        
    read_input(prompt: str) -> int:
        Lê um valor inteiro do usuário, com tratamento de exceções.
    """

    def draw_line(self) -> str:
        """
        Retorna uma linha de caracteres '-' com o tamanho especificado.
        """
        line = '-' * 45
        return line

    def display_header(self, text: str) -> None:
        """
        Exibe um cabeçalho centrado com uma linha acima e abaixo.
        """
        print(self.draw_line())  # Exibe uma linha antes do cabeçalho
        print(text.center(45))  # Centraliza o texto do cabeçalho com um comprimento de 45
        print(self.draw_line())  # Exibe uma linha depois do cabeçalho

    def display_menu(self, options: list) -> str:
        """
        Exibe um menu com opções numeradas e solicita uma entrada do usuário.
        """
        self.display_header('\033[34mMENU PRINCIPAL\033[m')  # Exibe o cabeçalho com texto azul
        for index, option in enumerate(options, start=1):
            print(f'\033[33m{index} - \033[34m{option}\033[m')  # Exibe cada item da lista com formatação de cores
        print(self.draw_line())  # Exibe uma linha depois do menu
        user_choice = self.read_input('\033[32mSua opção: \033[m')  # Solicita ao usuário para escolher uma opção
        sleep(1)
        os.system("cls")  # Limpa a tela
        return user_choice

    def read_input(prompt: str) -> int:
        """
        Lê um valor inteiro do usuário, com tratamento de exceções.
        """
        while True:
            try:
                user_input = int(input(prompt))  # Tenta converter a entrada do usuário para um inteiro
            except (ValueError, TypeError):
                print('\033[31mERRO! Por favor, digite uma opção válida.\033[m')  # Mensagem de erro para entrada inválida
                continue
            except KeyboardInterrupt:
                print('\033[31mERRO! O usuário não informou opções.\033[m')  # Mensagem de erro para interrupção pelo usuário
                break
            else:
                return user_input  # Retorna o valor inteiro se a conversão for bem-sucedida
