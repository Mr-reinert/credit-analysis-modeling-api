#---------------------------- IMPORTAÇÕES ------------------------------------------------------
from fuzzywuzzy import process
import pandas as pd    
from sklearn.preprocessing import StandardScaler,LabelEncoder  
import joblib      
import yaml
import psycopg2
import const
#----------------------------------------------------------------------------------------------
def fech_data_from_db(sql_query):   # função que faz uma consulta sql do arquivo de constante
    try:
        with open('config.yaml','r') as file:
            config = yaml.safe_load(file)

        con = psycopg2.connect(
            dbname=config['database_config']['dbname'],
            user=config['database_config']['user'],
            password=config['database_config']['password'],
            host=config['database_config']['host']
        )

        cursor = con.cursor()
        cursor.execute(sql_query)

        df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()
    return df

#Substituição de nulos
def substitui_nulos(df):
    for i in df.columns:
        if df[i].dtype == 'object':
            moda= df[i].mode()[0]
            df[i].fillna(moda, inplace=True)
        else:
            mediana= df[i].median()
            df[i].fillna(mediana, inplace=True)

profissoes_validas = ['Advogado', 'Arquiteto', 'Cientista de Dados', 
                      'Contador', 'Dentista', 'Empresário', 
                      'Engenheiro', 'Médico', 'Programador']

def corrigir_erros_digitacao(df, coluna, lista_valida):
    for i, valor in enumerate(df[coluna]):
        # Verifica se o valor é válido e não nulo
        valor_str = str(valor) if pd.notnull(valor) else ''
        
        if valor_str not in lista_valida and valor_str:  # Verifica se o valor não está na lista válida
            correcao = process.extractOne(valor_str, lista_valida)[0]  # Sugere a correção mais próxima
            df.at[i, coluna] = correcao  # Atualiza o valor corrigido no DataFrame

def tratar_outliers(df, coluna, minimo, maximo):
    """
    Substitui os outliers de uma coluna por sua mediana.
    
    Parâmetros:
    - df: DataFrame contendo os dados.
    - coluna: Nome da coluna a ser tratada.
    - minimo: Valor mínimo aceitável.
    - maximo: Valor máximo aceitável.
    
    Retorna:
    - O DataFrame com os outliers da coluna tratados.
    """
    # Calcula a mediana apenas dos valores dentro do intervalo aceitável
    mediana = df[(df[coluna] > minimo) & (df[coluna] < maximo)][coluna].median()
    # Substitui os outliers pela mediana
    df[coluna] = df[coluna].apply(lambda x: mediana if x < minimo or x > maximo else x)
    return df

def save_scalers(df, nome_colunas):
    for nome_coluna in nome_colunas:
        scaler = StandardScaler()
        df[nome_coluna] = scaler.fit_transform(df[[nome_coluna]])
        joblib.dump(scaler, f"./objects/scaler{nome_coluna}.joblib")

    return df


def save_encoders(df, nome_colunas):
    for nome_coluna in nome_colunas:
        label_encoder = LabelEncoder()
        df[nome_coluna] = label_encoder.fit_transform(df[nome_coluna])
        joblib.dump(label_encoder, f"./objects/labelencoder{nome_coluna}.joblib")

    return df