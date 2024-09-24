""" Modelo para predição de tempo de julgamento de processos judicais
O modelo será teinado com base nos dados disponíveis no Datajud, que é a base nacional de metadados processuais do poder judiciário brasileiro.
[Documentação do Datajud](https://datajud-wiki.cnj.jus.br/)
Os dados disponíveis são:
 - Tipo do Tribunal (Estadual, Federal, Trabalho, Eleitoal)
 - Estado
 - Grau do processo (G1, G2, TR, JE)
 - Unidade Judicial / Vara
 - Classe Processual
 - Assunto
 - Data Ajuizamento(Data de distribuição do processo)
 - Lista de movimentações

As classes, assuntos e movimentações seguem uma tabela nacional, com seus códigos e classificação previamente estabelecida.
Essa padronização é a TPU - [Tabelas Processuais Unificadas](https://www.cnj.jus.br/sgt/consulta_publica_classes.php)

Os dados da TPU foram organizados em arquivos csv
"""

# Imports
import pandas as pd
import requests
import json

# Leitura de csv's com dados da TPU
classes_tpu  = pd.read_csv('tpu-classes.csv', sep=',')
classes_tpu.rename(columns={'codnivel1': 'classe_nivel1', 
                            'codnivel2': 'classe_nivel2', 
                            'codnivel3': 'classe_nivel3', 
                            'codnivel4': 'classe_nivel4', 
                            'codnivel5': 'classe_nivel5', 
                            'codclasse': 'codclasse'}, inplace=True)

assuntos_tpu = pd.read_csv('tpu-assuntos.csv', sep=',')
assuntos_tpu.rename(columns={'codnivel1': 'assunto_nivel1', 
                             'codnivel2': 'assunto_nivel2', 
                             'codnivel3': 'assunto_nivel3', 
                             'codnivel4': 'assunto_nivel4', 
                             'codnivel5': 'assunto_nivel5', 
                             'codassunto': 'codassunto'}, inplace=True)

# Códigos de movimentos, que segunda a TPU são referentes a julgamentos
movs_julgamento = [193,196,198,200,202,208,210,212,214,218,219,220,221,228,230,235,236,237,238,239,240,241,242,244,385,442,443,444,445,446,447,448,449,450,451,452,453,454,455,456,
 457,458,459,460,461,462,463,464,465,466,471,472,473,853,871,884,900,901,972,973,1042,1043,1044,1045,1046,1047,1048,1049,1050,10953,10961,10964,10965,11373,11374,
 11375,11376,11377,11378,11379,11380,11381,11394,11396,11401,11402,11403,11404,11405,11406,11407,11408,11409,11411,11795,11796,11801,11876,11877,11878,11879,12028,
 12032,12033,12034,12041,12184,12187,12252,12253,12254,12256,12257,12258,12298,12319,12321,12322,12323,12324,12325,12326,12327,12328,12329,12330,12331,12433,12434,
 12435,12436,12437,12438,12439,12440,12441,12442,12443,12450,12451,12452,12453,12458,12459,12475,12615,12616,12617,12649,12650,12651,12652,12653,12654,12660,12661,
 12662,12663,12664,12665,12666,12667,12668,12669,12670,12671,12672,12673,12674,12675,12676,12677,12678,12679,12680,12681,12682,12683,12684,12685,12686,12687,12688,
 12689,12690,12691,12692,12693,12694,12695,12696,12697,12698,12699,12700,12701,12702,12703,12704,12705,12706,12707,12708,12709,12710,12711,12712,12713,12714,12715,
 12716,12717,12718,12719,12720,12721,12722,12723,12724,12735,12738,12792,14099,14210,14211,14213,14214,14215,14216,14217,14218,14219,14680,14777,14778,14848,14937,
 15022,15023,15024,15026,15027,15028,15029,15030,15165,15166,15211,15212,15213,15214,15245,15249,15250,15251,15252,15253,15254,15255,15256,15257,15258,15259,15260,
 15261,15262,15263,15264,15265,15266,15322,15408,1002013,1003301,1003302,1050009,1050080,1050083,1050147,4050028,4050079,4050080,4050083,22,246]

movs_arquivamento = [22,246]
mov_evolucao_classe = 14739

# Variáveis para utilização da API do Datajud
headers = {
  'Authorization': 'ApiKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
  'Content-Type': 'application/json'
}
tribunal = 'tjrr'


# Método para pegar apenas o primeiro assunto, pois o processo pode conter um assunto principal e N secundários
def extrair_assunto(assuntos):
  return assuntos[0]['codigo']


# Método para extrair a data de julgamento
def extrair_julgamento(movimentos):
  for movimento in movimentos:
    if movimento['codigo'] in movs_julgamento:
      return movimento['dataHora']
  return None


def load_data_from_datajud_api(tribunal, classe):
    url = f"https://api-publica.datajud.cnj.jus.br/api_publica_{tribunal}/_search"

    payload = json.dumps({
        "size":10000,
        "query": {
            "bool": {
                "must": [
                    {"match": {"classe.codigo": classe}}
                ]
            }
        }
    })

    response = requests.request("POST", url, headers=headers, data=payload)
    resposta = json.loads(response.text)
    # Os dados estão dentro de hits
    lista = resposta['hits']['hits']
    
    # Criando o DataFrame com os dados
    df = pd.DataFrame.from_records(lista)
    df = df['_source'].apply(pd.Series)

    # Muitos dados estão em json dentro da coluna do DataFrame, por isso são extraídos para novas colunas
    df[['codigo_classe','nome_classe']] = df['classe'].apply(pd.Series)
    df[['codigo_formato','nome_formato']] = df['formato'].apply(pd.Series)
    df[['orgao_codigoMunicipioIBGE','orgao_codigo','orgao_nome']] = df['orgaoJulgador'].apply(pd.Series)

    # Aplica os métodos para extrair os assuntos e data de julgamento
    df['data_julgamento'] = df['movimentos'].apply(extrair_julgamento)
    df['codigo_assunto'] = df['assuntos'].apply(extrair_assunto)

    # Conversão dos campos de data
    df['data_ajuizamento'] = pd.to_datetime(df['dataAjuizamento']).dt.strftime('%Y-%m-%d')
    df['data_julgamento'] = pd.to_datetime(df['data_julgamento']).dt.strftime('%Y-%m-%d')
    df['data_julgamento'] = pd.to_datetime(df['data_julgamento'])
    df['data_ajuizamento'] = pd.to_datetime(df['data_ajuizamento'])
    

    # Removendo colunas desnecessárias
    colunas_desnecessarias = ['@timestamp','id','sistema','dataHoraUltimaAtualizacao','dataAjuizamento',
                              'classe','nome_classe','formato','nome_formato',
                              'orgaoJulgador','orgao_codigoMunicipioIBGE','movimentos',
                              'nivelSigilo', 'assuntos'] 
    df.drop(columns=colunas_desnecessarias,inplace=True)

    # Removendo os processos que não tem julgamento
    df.dropna(subset=['data_julgamento'],inplace=True)

    # Criando coluna com o tempo de julgamento
    df['tempo_julgamento'] = (df['data_julgamento'] - df['data_ajuizamento']).dt.days


    # Fazendo join dos DataFrame de classes e assuntos da TPU
    df = pd.merge(df, assuntos_tpu, how='left', left_on='codigo_assunto', right_on='codassunto')
    df = pd.merge(df, classes_tpu, how='left',  left_on='codigo_classe', right_on='codclasse')

    df['numero_processo'] = df['numeroProcesso'].astype(str)
    df.drop(columns=['descclasse','descassunto','codclasse', 'codassunto','numeroProcesso'],inplace=True)

    return df


load_data_from_datajud_api(tribunal, 1116).to_csv('data.csv', index=False, doublequote=True)


# 'orgao_nome' guardar pra pegar os respectivos códigos




# df_final = pd.merge(df_final, classes, how='left', left_on='nome_classe', right_on='descclasse')

# df_final.drop(columns=['movimentos','descclasse','descassunto','nome_classe', 'dcr_assunto'])
