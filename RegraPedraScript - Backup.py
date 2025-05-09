## Script REGRA DE PEDRA

# -------------------------------------------------------------------------------------------------------------------------------------------------
#[R1] - Primeira etapa: REGRA DE BLOQUEIO NO TOPO
# -------------------------------------------------------------------------------------------------------------------------------------------------
def verificar_regra_bloqueio_RI():
    print("\n [Primeira Etapa] - Regras de Bloqueio no Topo")

# Valores de Referência

    Ref_RI = 2 # valor referência
    Base_RI = 1 # Valor por padrão 1, mas pode mudar em futuras atualizações.

# Input do Usuário 
    try:
        RegraOK_RI = int(input("Quantas regras de bloqueio no Topo possui o Firewall? (Digite 0, 1 ou 2): ").strip())
        if RegraOK_RI not in [0,1,2]:
            raise ValueError # Garante que o número esteja dentro do intervalo permitido
    except ValueError:
        print("O valor é inválido! Por favor, digite 0, 1 ou 2.")
        return None, None

# Cálculo dos pontos
    Ponto_RI = (RegraOK_RI * Base_RI) / Ref_RI

# Verificação do Status da primeira Regra de Pedra[R1]
    Status_RI = "OK" if Ponto_RI == 1 else "NOK"

    return Ponto_RI, Status_RI

# -------------------------------------------------------------------------------------------------------------------------------------------------
#[R2] - Segunda Etapa: REGRA DE BLOQUEIO ENTRE ZONAS
# -------------------------------------------------------------------------------------------------------------------------------------------------
def verificar_regra_bloqueio_RII():
    print("\n [Segunda Etapa] - Regras de Bloqueio entre Zonas")

# Valores de Referência
    Base_RII = 1 # Valor por padrão 1, mas pode mudar em futuras atualizações.
    Ponto_RII = 0 # Inicializado com 0
    global NumTotalRegras_RII

# Observação antes do Input
    print("OBSERVAÇÃO: Mesmo que a regra tenha 2 'any', ela ainda conta só uma vez para o cálculo. Portanto, atenção na hora de preencher em seguida. ")
    print("As regras de topo de bloqueio e as ao final default [só aparecem no acesso pelo firewall essas últimas] são ignoradas nessa contagem.")

# Input do usuário para TOTAL de regras
    try:
        NumTotalRegras_RII = int(input("Quantas regras o Firewall possui?").strip()) # a variável armazena o valor inserido - 1
        if NumTotalRegras_RII < 1:
            raise ValueError # Garante que o número não seja menor que 1.
    except ValueError:
            print("Valor Incorreto: Verifique o valor inserido e insira novamente. O Número inserido não pode ser menor que 1.")
            return None, None
    
# Input do usuário para regras ANY
    try:
        RegraAny_RII = int(input("Quantas regras com zonas 'ANY' o Firewall possui?").strip())
    except ValueError:
        print("ERRO: Digite um número válido. ")
        return None, None


# Situação a respeito do Rule 1
    while True:
        RuleOneInput = input("O Firewall possui Rule 1? Digite S ou N: ").strip().upper()
        if RuleOneInput in ["S", "N"]:
            break
        print("Erro: Por favor, digite apenas 'S' para 'sim' ou 'N' para 'não'. ")



# Definição do RuleOne_RII

    # A variável RuleOne_RII recebe ou o número de regras do firewall -1 (se tiver Rule1) 
    # ou recebe o número de regras do firewall dividido por 2 (se não tiver Rule1)
    RuleOne_RII = NumTotalRegras_RII if RuleOneInput == "S" else NumTotalRegras_RII / 2

# Cálculo dos pontos
    Res_RII = RuleOne_RII - RegraAny_RII
    Ponto_RII = Res_RII * Base_RII / NumTotalRegras_RII

# Verificação do Status
    Status_RII = "OK" if Ponto_RII == Base_RII else "NOK"

    return Ponto_RII, Status_RII


# -------------------------------------------------------------------------------------------------------------------------------------------------
#[R3] - Terceira Etapa: FIREWALL COM COMUNICAÇÃO EXTERNA (INTERNET)
# -------------------------------------------------------------------------------------------------------------------------------------------------
def verificar_comunicacao_externa_RIII():
    print("\n[Terceira Regra] - Acesso à Internet Bloqueada por padrão.")

# Informativo ao Usuário
    print("O Firewall deve ter a comunicação com a internet bloqueada.")
    print("Caso o ambiente não seja aberto para a internet, então está correto. Caso contrário, está errado.")
    print("O Caminho para consultar essa informação é: Network > Interfaces > Ethernet. ")

# Valor de Referência
    Ref_RIII = 1.0

# Perguntar sobre Bloqueio de Internet
    while True:
        BlockExtInput = input("O Firewall possui bloqueio para a internet? (Digite S ou N): ").strip().upper()
        if BlockExtInput in ["S", "N"]:
            break
        print("ERRO: Valor inválido! Digite 'S' ou 'N'. ")

# Atribuição a variável BlockExt_RIII
    # Se o acesso a internet for bloqueado no Firewall, então ele recebe o valor 1 que é da referência. Caso Contrário, recebe 0
    BlockExt_RIII = Ref_RIII if BlockExtInput == "S" else 0

# Cálculo dos Pontos
    Ponto_RIII = BlockExt_RIII

# Verificação do Status
    Status_RIII = "OK" if Ponto_RIII == 1 else "NOK"

    return Ponto_RIII, Status_RIII

# -------------------------------------------------------------------------------------------------------------------------------------------------
#[R4] - Quarta Etapa: Regras Baseadas em Aplicações
# -------------------------------------------------------------------------------------------------------------------------------------------------
def verificador_regras_aplicacao_RIV():
    print("\n[Quarta Etapa] - Regras Baseadas em aplicações")
    print("Nessa etapa, devemos identificar quais regras possuem definição por aplicação.")
    print("Regras definidas apenas por serviço devem ser computadas como incorretas nessa tarefa.")
    print("Exemplo: Correto: RDP // Incorreto: TCP-3389\n")

    Base_RIV = 1


# Pegando o valor total de regras da Parte 2
    global NumTotalRegras_RII, NumTotalRegras_RIV
    NumTotalRegras_RIV = NumTotalRegras_RII

# Perguntar ao Usuário quantas regras não possuem aplicação definida

    try:
        AplRegras_RIV = int(input("Quantas regras com aplicação não definida existem no Firewall?").strip())
        if AplRegras_RIV < 0:
            raise ValueError
    except ValueError:
        print("ERRO: Digite um número válido. ")
        return None, None

# Cálculo do Resultado
    Res_RIV = NumTotalRegras_RIV - AplRegras_RIV

# Cálculo da Pontuação
    Ponto_RIV = Res_RIV * Base_RIV / NumTotalRegras_RIV

# Determinar o Status
    Status_RIV = "OK" if Ponto_RIV == 1 else "NOK"

    return Ponto_RIV, Status_RIV

# -------------------------------------------------------------------------------------------------------------------------------------------------
#[R5] - Quinta Etapa: REGRAS BASEADAS EM HOST
# -------------------------------------------------------------------------------------------------------------------------------------------------
def verificar_regras_hosts():
    print("\n Os campos de endereço, tanto origem quanto destino, devem ser definidos por IP.")
    print("Endereços com 'any' ou redes devem ser evitados.")
    print("\n Nesta etapa, contaremos a quantidade de regras que possuem 'any' ou redes.")
    print("OBS: Se uma regra possuir 2 'any' ou 2 redes, contamos apenas uma única vez.")
    print("OBS2: Se uma mesma regra tiver 'any' e rede, a contagem será apenas para a pergunta referente 'any'.")

    Base_RV = 1
    
# Perguntar ao usuário quantas regras o endereço de REDE definido
    try:
        RegrasRede_RV = int(input("Quantas regras com endereço de REDE definida existem no Firewall").strip())
        if RegrasRede_RV < 0:
            raise ValueError
    except ValueError:
            print("ERRO: Valor inválido! O valor não pode ser negativo nem decimal. Tente novamente.")
            return None, None
            
# Aplicando a regra de contagem para redes pegando o valor inserido e dividindo por 2.
    RegrasRede_RV /= 2

# Perguntar ao usuário quantas regras o Firewall possui com ANY.
    try:
        RegrasAny_RV = int(input("Quantas regras 'any' existem no Firewall.").strip())
        if RegrasAny_RV < 0:
            raise ValueError
    except ValueError:
            print("ERRO: Valor inválido! O valor não pode ser negativo nem decimal. Tente novamente.")
            return None, None

# Aplicando a regra de contagem de ANYs pegando o valor inserindo e somando com o valor calculado de redes.
    RegrasAny_RV += RegrasRede_RV

# Cálculo do Resultado
    Res_RV = NumTotalRegras_RII - RegrasAny_RV

# Cálculo da pontuação
    Ponto_RV = Res_RV * Base_RV / NumTotalRegras_RII

# Determinar o Status
    Status_RV = "OK" if Ponto_RV == 1 else "NOK"

    return Ponto_RV, Status_RV

# Executa a verificação Para saber se alguma variável armazenou dados incorretos ou vazios e armazena os resultados

Ponto_RI, Status_RI = verificar_regra_bloqueio_RI()
Ponto_RII, Status_RII = verificar_regra_bloqueio_RII()
Ponto_RIII, Status_RIII = verificar_comunicacao_externa_RIII()
Ponto_RIV, Status_RIV = verificador_regras_aplicacao_RIV()
Ponto_RV, Status_RV = verificar_regras_hosts()

if None not in [Ponto_RI, Ponto_RII, Ponto_RIII, Ponto_RIV, Ponto_RV, Status_RI, Status_RII, Status_RIII, Status_RIV, Status_RV]:

# Relatório Final (SER DISPOSTO SÓ AO FINAL DE TODo O CODIGO)

# Pontuação das Regras de Pedra
    print("\n Pontuação: ")
    print("--------------------------")
    print(f"R1 = {Ponto_RI}")
    print(f"R2 = {Ponto_RII}")
    print(f"R3 = {Ponto_RIII}")
    print(f"R4 = {Ponto_RIV}")
    print(f"R5 = {Ponto_RV}")


# Status das Regras de Pedra
    print("\n Status: ")
    print("--------------------------")
    print(f"R1 = {Status_RI}")
    print(f"R2 = {Status_RII}")
    print(f"R3 = {Status_RIII}")
    print(f"R4 = {Status_RIV}")
    print(f"R5 = {Status_RV}")


print("\n✅ Verificação concluída!")

