import requests
import pandas as pd
import sys
import datetime
import numpy as np
from google.cloud import bigquery
from google.oauth2 import service_account
from pandas_gbq import to_gbq

# =================================================================================================
# Função para consumir os dados da API, atribuir cada uma a seu nome dentro do json e 
# inserir todas dentro de um dicionário para serem tratadas individualmente  
# =================================================================================================
def get_data():
    print('\nIniciando chamada da API...')

    response = requests.get('https://swapi.dev/api')
    tabelas = {}
    try:
        for tabela in response.json():
            # Variaveis para paginação 
            # Isso foi feito pois a API só retorna 10 linhas por página
            page = 1
            all_data = []

            while True:
                # Traz as 10 linhas da primeira página 
                result = requests.get(f'https://swapi.dev/api/{tabela}/?page={page}')
                page_data = pd.DataFrame(result.json()['results'])

                for col in page_data.columns:
                    # print(f'Coluna: {i}')
                    for row_idx, row in enumerate(page_data[col]):
                        if isinstance(row, str) and row.startswith('https://'):
                            campo = requests.get(row)
                            if tabela != 'films':
                                new_value = campo.json()['name']
                            else:
                                new_value = campo.json()['title']

                            page_data.at[row_idx, col] = new_value
                            # print(f'{l}')
                        else:
                            continue

                # Append dos dados na variável com todos os dados 
                all_data.append(page_data)

                # Verifica se existem mais páginas 
                if result.json()['next'] is None:
                    break

                page += 1

            # Cria uma tabela com todas as páginas carregadas 
            tabela_dados = pd.concat(all_data, ignore_index=True)

            tabelas[tabela] = tabela_dados
            print(f'> Tabela "{tabela}" com {tabela_dados.shape[0]} linhas carregada com sucesso!')
        
    except requests.exceptions.HTTPError as e:
        print(f'Erro na requisição: {e}')
    except ValueError as e:
        print(f'Erro de conversão de valor: {e}')
    # except Exception as e:
    #     print(f'Erro inesperado: {e}')

    return tabelas


# =================================================================================================
# Função que faz o tratamento dos dados, incluindo remoção de várias colunas não muito úteis, 
# colunas que vem apenas com um link, etc.
# =================================================================================================
def tratar_dados(data):
    print('\nIniciando tratamento das tabelas...')
    # Define um array com todas as tabelas a remover
    remove_columns = ['url', 'edited', 'created'] 
                    # ['films', 'pilots', 'homeworld', 
                    #   'people', 'vehicles', 'species', 'planets', 'starships', 'characters', 
                    #   'residents']
    
    # Cria um dicionário para armazenar as tabelas após serem tratadas 
    tabelas_tratadas = {}

    # Início do loop para iterar com as colunas das tabelas
    try:
        for tabela_nome, tabela in data.items():
            # Removendo colunas
            try:
                tabela = pd.DataFrame(tabela)
                # Inicio do loop para remover as colunas definidas caso existam 
                for coluna in remove_columns:
                    if coluna in tabela.columns:
                        tabela.drop(coluna, axis=1, inplace=True)
                    else:
                        continue
            except KeyError as e: 
                print(f'> Erro ao remover colunas predefinidas: {e}') 

            # Removendo colunas com listas 
            try:
                for coluna in tabela.columns:
                    if isinstance(tabela[coluna].iloc[0], list):
                        # print(coluna)
                        tabela = tabela.drop(coluna, axis=1)
                    else:
                        continue
            except Exception as e:
                print(f'> Erro ao remover colunas com listas: {e}')
                        
            print(f'> Tabela "{tabela_nome}" tratada com sucesso!')
            tabelas_tratadas[tabela_nome] = tabela

    except Exception as e:
        print(f'> Erro no tratamento: {e}')
    
    return tabelas_tratadas

# =================================================================================================
# Função para carregar os dados para o BigQuery
# =================================================================================================
def load_data_togbq(nome_tabela, dados):

    try:
        credentials = service_account.Credentials.from_service_account_file('files\etl-starwars-swapi-4f53955e764c.json')
        client = bigquery.Client(credentials=credentials)
        project_id = 'etl-starwars-swapi'
        dataset_id = 'etl-starwars-swapi.dataset_starwars'

        dados = pd.DataFrame(dados)

        destination_table = f'{dataset_id}.{nome_tabela}'

        to_gbq(dados, destination_table, project_id = project_id, if_exists = 'replace')

        print(f'> Upload da tabela "{nome_tabela}" para o BigQuery realizado com sucesso!')

    except pd.errors.ParserError as e:
        print(f'> Erro ao analisar dados para a tabela "{nome_tabela}": {e}')

    except Exception as e:
        print(f'> Erro inesperado ao carregar a tabela "{nome_tabela}": {e}')
        # Registrar erro em um log
        with open('etl_errors.log', 'a') as logfile:
            logfile.write(f'[{datetime.datetime.now()}] Erro na tabela {nome_tabela}: {e}\n')
        

# =================================================================================================
# Chamada da função main
# =================================================================================================
if __name__ == '__main__':

    print('=' * 50)
    print('\nIniciando função main...\n')

    try:
        print('=' * 50)
        data = get_data()

        print('=' * 50)
        dados = tratar_dados(data)

        print('=' * 50)
        print('\nIniciando carregamento das tabelas para o BigQuery...')
        for nome_tabela, tabela in dados.items():
            load_data_togbq(nome_tabela, tabela)
        
        print('=' * 50)
        print('\nFunção finalizada com sucesso! Finalizando...')
        sys.exit(0)

    except Exception as e:
        function = sys._getframe().f_code.co_name
        print(f'Erro na função {function}: {e}')
