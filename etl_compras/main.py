from google.cloud import bigquery
from google.oauth2 import service_account
from pandas_gbq import to_gbq
import pandas as pd
import openpyxl

# ===================================================================================
# DEFININDO VARIÁVEIS 
# ===================================================================================
file_path = 'Arquivos/Base Compras.xlsx'

# Variáveis do GCP e do BigQuery
project_id = "projeto-dash-compras"
credentials_file = "projeto-dash-compras-c65d00286455.json"
dataset_id = "dataset_compras"
table_id = ['comprador', 'compras', 'fornecedor', 'materia_prima']

# ===================================================================================
# DEFININDO FUNÇÃO PARA LER A PLANILHA
# NOTA: wb / workbook (workbooks permitem ler e iterar com todas as abas de uma planilha)
# ===================================================================================
def get_data(file):
    data = {}
    print('Abrindo arquivo...')
    try:
        with open(file, "rb") as f:
            wb = openpyxl.load_workbook(f)

            # Loop para ler todas as abas da planilha
            for sheet_name in wb.sheetnames:
                data[sheet_name] = pd.DataFrame(pd.read_excel(f, sheet_name=sheet_name))

            # Renomeando as abas da planilha
            data['comprador'] = data.pop('dComprador')
            data['fornecedor'] = data.pop('dFornecedor')
            data['compras'] = data.pop('fCompras')
            data['materia_prima'] = data.pop('dMateriaPrima')

            print('Arquivo aberto e carregado com sucesso!')
    except FileNotFoundError as e: 
        print(f'Erro ao abrir o arquivo: {e.filename}')

    return data

# ===================================================================================
# DEFININDO FUNÇÃO PARA TRATAR OS DADOS 
# ===================================================================================
def tratar_dados(data):
    print('Tratando dados e colunas...')

    data['compras'] = data['compras'].rename(columns={'Desconto (%)': 'Desconto Percentual'})

    try:
        for tabela in data.keys():
            for coluna in data[tabela].columns: 
                print(f'renomeando a coluna {data[tabela][coluna]}')
                data[tabela].rename(columns={coluna: coluna.replace(' ', '_')}, inplace=True)
                
        print('Dados tratados com sucesso!')

    except KeyError as e:
        print(f'Erro no acesso à coluna: {e}')
    except ValueError as e:
        print(f'Erro de conversão de tipo: {e}')
    except Exception as e:
        print(f'Erro no tratamento: {e}')


# ===================================================================================
# DEFININDO FUNÇÃO PARA SUBIR OS DADOS PARA O BIGQUERY
# ===================================================================================
def load_data(data, project, credentials):
    
    # Criação da conexão com BigQuery
    credentials = service_account.Credentials.from_service_account_file(credentials_file)

    # Subindo os dados de cada aba da planilha para a tabela correspondente no bigquery
    if data is not None:
        try:
            for nome_aba, df in data.items():
                # Une o nome do dataset ao nome da aba (mesmo nome da tabela no bigquery)
                table_id = f"{dataset_id}.{nome_aba}" 
                # Subindo os dados para o bigquery          
                try:
                    to_gbq(df, destination_table = table_id, project_id = project_id, credentials = credentials, if_exists = 'replace')
                    print(f"Tabela '{nome_aba}' carregada com sucesso!")

                except Exception as e:
                    print(f"Erro ao carregar a tabela '{nome_aba}': {e}")
            print('Todas as tabelas carregadas com sucesso!')

        except Exception as e: 
            print(f'Erro ao carregar tabelas: {e}')
    else:
        print('Tabela vazia')

def main():
    dados = get_data(file_path)
    tratar_dados(dados)
    load_data(dados, project_id, credentials_file)

if __name__ == '__main__':
    main()
