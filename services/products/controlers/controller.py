import json
import os

class Controller:
    """
    Classe Controller para gerenciar a leitura e escrita de dados em um arquivo JSON.
    
    Esta classe fornece métodos para carregar dados de um arquivo JSON e salvar 
    dados de volta no arquivo. Se o arquivo JSON não existir, ele será criado.
    
    Atributos:
    - json_file (str): O nome do arquivo JSON usado para armazenar os dados.
    
    Métodos:
    - load_json(self): Carrega os dados do arquivo JSON.
    - save_json(self, data): Salva os dados no arquivo JSON.
    """
    def __init__(self) -> None:
        self._json_file = 'data.json'
    

    def load_json(self):
        """
        Carrega os dados do arquivo JSON.

        Se o arquivo JSON não existir, cria um novo arquivo vazio e retorna um dicionário vazio.

        Retorna:
        - dict: Os dados carregados do arquivo JSON.
        """
        # Verifica se o arquivo JSON existe
        if os.path.exists(self._json_file):
            # Abre o arquivo JSON e carrega os dados
            with open(self._json_file, 'r') as file:
                return json.load(file)
        else:
            # Se o arquivo não existir, cria um novo arquivo vazio
            print("JSON file not found. Creating a new file.")
            with open(self._json_file, 'w') as file:
                json.dump({}, file)
            return {}

    def save_json(self, data):
        """
        Salva os dados no arquivo JSON.

        Parâmetros:
        - data (dict): Os dados a serem salvos no arquivo JSON.
        """
        # Abre o arquivo JSON em modo de escrita e salva os dados
        with open(self._json_file, 'w') as file:
            json.dump(data, file, indent=4)
