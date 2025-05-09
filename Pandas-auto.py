# IMPORTAÇÕES ----------------
import pandas as pd
from pathlib import Path # Biblio para manipular caminhos de arquivos e diretórios

# Informações variáveis para transformar em INPUT FUTURAMENTE ------------------
fw_name = 'ASS'
cliente_name = 'COPEL'
trimestre = '2025_T1-2' # Criar forma automática atrelada ao date time

# ----------------------------------------------------------
# ------- CONTROLE DE DIRETÓRIO ----------------------------
# ----------------------------------------------------------

# Organização do Diretório (até a pasta cliente que é fixa)
base_dir = Path(r'C:/Users/IuryAnnarumma/TI Safe/ICS-SOC - Documentos/Clientes') 

# Caminho até o trimestre
pasta_destino = base_dir / cliente_name / 'Arquitetura' / 'Regras de Pedra' / trimestre

# Cria as pastas (caso não exista)
pasta_destino.mkdir(parents=True, exist_ok=True)

# Arquivo pronto com o caminho de saída
arquivo_pronto = pasta_destino / f"RegrasPedrav2_{fw_name}_{trimestre}.xlsx"

# ------ CAMINHO DOS ARQUIVOS -----------------------------
# !!! - Fazer uma variável que recebe estritamente o nome do arquivo em xlsx e substituir no file_path para receber esse input 
caminho_firewall = fr'C:/Users/IuryAnnarumma/OneDrive - TI Safe/repositorio_iury/RegraPedra/files/Policy_Rules_{cliente_name}_{fw_name}_{trimestre}.xlsx'
caminho_aplicacao = r'C:/Users/IuryAnnarumma/OneDrive - TI Safe/repositorio_iury/RegraPedra/files/aplicacoes.csv'


# --- CRIANDO OS DATAFRAMES ---------------------------
df = pd.read_excel(caminho_firewall, sheet_name="Dados") # DataFrame do Firewall
df_aplicacao = pd.read_csv(caminho_aplicacao) # DataFrame das aplicações do Applipedia
# Pegando as colunas pertinentes do relatório
colunas = ['#', 'Name', 'Tags', 'Type', 'Source Zone', 'Source Address', 'Destination Zone', 'Destination Address', 'Application', 'Service', 'Action', 'Profile']

# Cria uma cópia do relatório e passa para a variável
df_firewall = df[colunas].copy()

# -----------------------------------------------------------
# Função -  Padronização de Dados
# -----------------------------------------------------------
# Função para padronizar dados de forma a facilitar queries e manipulações.
def padronizar_dados(data):
    return data.astype(str).str.strip().str.lower()

# -----------------------------------------------------------
# Verificação de Rule1
# -----------------------------------------------------------
checar_rule1 = df_firewall.copy() # Criar uma cópia para não afetar o DF padrão com a padronização do nome das regras.
checar_rule1['Name'] = padronizar_dados(checar_rule1['Name'])

have_rule1 = (checar_rule1['Name'] == 'rule1').any() # Atribuir a variável o booleando de checagem se existe a rule1
# ------------------------------------------------------------
# PONTUAÇÃO - CONFERIR REGRAS DE TOPO
# ------------------------------------------------------------
regras_topo = df_firewall.head(2).copy()
regras_topo['Tags'] = padronizar_dados(regras_topo['Tags'])
regras_topo['Action'] = padronizar_dados(regras_topo['Action'])
regras_topo['Profile'] = padronizar_dados(regras_topo['Profile'])

checagem_condicao = (
    regras_topo['Tags'].str.contains('drop') & (regras_topo['Action'] == 'drop') & (regras_topo['Profile'] == 'none')
)

qtd_topo = checagem_condicao.sum()

if qtd_topo == 2:
    ponto_topo = 1.0
elif qtd_topo == 1:
    ponto_topo = 0.5
else:
    ponto_topo = 0

# -----------------------------------------------------------
# Número de Regras
# -----------------------------------------------------------
df_regrasAllow = df_firewall.copy() # Cópia para um novo dataframe
df_regrasAllow['Action'] = padronizar_dados(df_regrasAllow['Action'])

# Modificar o DataFrame para ter somente as regras com action igual a allow
df_regrasAllow = df_regrasAllow[df_regrasAllow['Action'] == 'allow']
# Atribuir a quantidade de regras allow para a variável num_regras
num_regras = df_regrasAllow.shape[0]

# ------------------------------------------------------------
# Cálculo de Zonas Any & Criação da Coluna de contagem
# ------------------------------------------------------------
df_regrasAllow['Source Zone'] = padronizar_dados(df_regrasAllow['Source Zone'])
df_regrasAllow['Destination Zone'] = padronizar_dados(df_regrasAllow['Destination Zone'])

# Criação da coluna "zona_any"
df_regrasAllow['zona_any'] = (
    (df_regrasAllow['Source Zone'] == 'any') |
    (df_regrasAllow['Destination Zone'] == 'any')
).astype(int)

# Quantidade de regras que possuem pelo menos uma zona "any"
regras_zonaAny = df_regrasAllow['zona_any'].sum()

# ------------------------------------------------------------
# PONTUAÇÃO - ZONAS ANY
# ------------------------------------------------------------
if have_rule1: # Equação a ser realizada mediante a ter ou não rule1 no Firewall
    ponto_zona = (num_regras - regras_zonaAny) / num_regras

else:
    ponto_zona = ((num_regras / 2) - regras_zonaAny) / num_regras


# -----------------------------------------------------------------------------------------------
# TRANSFORMAR COLUNA APLICACÃO ARQUIVO
# -----------------------------------------------------------------------------------------------
# Todas as aplicações da Palo Alto para uma lista
known_app = df_aplicacao['Name'].tolist()

# Função para separar as aplicações com vírgulas
def separar_aplicacoes(app_string):
    if pd.isna(app_string): # Caso tenha NaN preencher com vazio
        return ""
    
    app_string = str(app_string) # Garantir que é string
    found_app = [] # Lista para armazenar as aplicações do firewall 
    remain = app_string 

    while remain:
        match = False
        for app in known_app: # Varredura para comparar os elementos com os apps listados
            if remain.startswith(app):
                found_app.append(app)
                remain = remain[len(app):] # Remove da dataframe a aplicação já adicionada ao found_app
                match = True
                break

        if not match:   # Se a aplicação do DataFrame não der match com a lista de aplicações da Palo Alto, pula um caractere e faz a verificação novamente.
            remain = remain[1:] 

    return ', '.join(found_app) if found_app else app_string

df_firewall['Application'] = df_firewall['Application'].apply(separar_aplicacoes) 

# ---------------------------------------------------------------
# APLICAÇÕES RISCO 5 
# ---------------------------------------------------------------

# Lista de Referência com as aplicações Nível 5
lista_risco5 = df_aplicacao.loc[df_aplicacao["Risk"] == 5, "Name"].tolist()

# Criar coluna para salientar regras com risco 5 nela

df_firewall['tem_app5'] = df_firewall['Application'].str.contains("|".join(lista_risco5), case=False, na=False).astype(int)

# Criar uma lista com o nome de todas as regras que possuem regras nível 5 e informando quais são as aplicações

# ---------------------------------------------------------------
# CHECAGEM DE REGRAS ANY e REDES
# ---------------------------------------------------------------

df_firewall['regra_any'] = (
    (
        padronizar_dados(df_firewall['Source Address']).eq('any') | 
        padronizar_dados(df_firewall['Destination Address']).eq('any')
    ) &
    (padronizar_dados(df_firewall['Action']) == 'allow')
).astype(int)

   #!!!!!! Complementar o código para que se pegue só any de regras "allow"

# ----------- Testando busca por aplicações nível 5 de risco -------------------
# criar uma lista que contenha as aplicações a serem buscadas no arquivo
#lista_teste = ['ftp', 'vnc', 'telnet']

# Separar as aplicações por vírgula

# ---------------------------------------------------------------
# PONTUAÇAO FINAL
# ---------------------------------------------------------------
pontuacoes_regras = {
    'Regras de Topo': ponto_topo,
    'Regras Zona Any': ponto_zona
}

pontuacao_final = sum(pontuacoes_regras.values())

# Criação do DataFrame do Relatório

df_relatorio = pd.DataFrame([
    {'Critério': chave, 'Pontuação': valor}
    for chave, valor in pontuacoes_regras.items()
])

# Adiciona linha da pontuação total

df_relatorio = pd.concat([
    df_relatorio, 
    pd.DataFrame([{
        'Critério': 'Total', 'Pontuação': pontuacao_final
    }])
], ignore_index=True)

# ----------------------------------------------
# Criando Abas e separando informações nelas
# ----------------------------------------------
with pd.ExcelWriter(arquivo_pronto, engine='openpyxl') as writer:
    df_firewall.to_excel(writer, sheet_name='Regras', index=False)
    df_relatorio.to_excel(writer, sheet_name='Relatório', index=False)


# FAZER FUTURAMENTE: Criação automática de sub pastas que entendam qual cliente e localidade se trata, assim como o trimestre.
# Baixar o arquivo em xlsx sem index gerado automaticamente

# # RETIRAR O COMENTARIO DEPOIS ----->  

print(f"Arquivo salvo em: {arquivo_pronto}")

