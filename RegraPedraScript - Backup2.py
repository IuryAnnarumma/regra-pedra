## Script REGRA DE PEDRA

# ----------------------------------
#[R1] - Primeira etapa: REGRA DE BLOQUEIO NO TOPO
# ------------------------------------
def verificar_regra_bloqueio_RI():
    print("\n [Primeira Etapa] - Regras de Bloqueio no Topo")

# Valores de Referência

    Ref_RI = 2 # valor referência
    Base_RI = 1 # Valor por padrão 1, mas pode mudar em futuras atualizações.

# Input do Usuário 
    try:
        NumRegraOK_RI = int(input("Quantas regras de bloqueio no Topo possui o Firewall? (Digite 0, 1 ou 2): ").strip())
        if NumRegraOK_RI not in [0,1,2]:
            raise ValueError # Garante que o número esteja dentro do intervalo permitido
    except ValueError:
        print("O valor é inválido! Por favor, digite 0, 1 ou 2.")
        return None, None

# Cálculo dos pontos
    Ponto_RI = (NumRegraOK_RI * Base_RI) / Ref_RI

# Verificação do Status da primeira Regra de Pedra[R1]
    Status_RI = "OK" if Ponto_RI == 1 else "NOK"

    return Ponto_RI, Status_RI

# ------------------------------------
#[R2] - Segunda Etapa: REGRA DE BLOQUEIO ENTRE ZONAS
# ------------------------------------
def verificar_regra_bloqueio_RII():
    print("\n [Segunda Etapa] - Regras de Bloqueio entre Zonas")

# Valores de Referência
    Base_RII = 1 # Valor por padrão 1, mas pode mudar em futuras atualizações.
    Ponto_RII = 0 # Inicializado com 0

# Observação antes do Input
    print("OBSERVAÇÃO: Mesmo que a regra tenha 2 'any', ela ainda conta só uma vez para o cálculo. Portanto, atenção na hora de preencher em seguida. ")

# Input do usuário para TOTAL de regras
    try:
        NumTotalRegras_RII = int(input("Quantas regras o Firewall possui?").strip()) - 1 # a variável armazena o valor inserido - 1
        if NumTotalRegras_RII < 1:
            raise ValueError # Garante que o número não seja menor que 1.
    except ValueError:
            print("Valor Incorreto: Verifique o valor inserido e insira novamente. O Número inserido não pode ser menor que 2.")
            return None, None
    
# Input do usuário para regras ANY
    try:
        NumRegraAny_RII = int(input("Quantas regras com zonas 'ANY' o Firewall possui?").strip())
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
    Res_RII = RuleOne_RII - NumRegraAny_RII
    Ponto_RII = Res_RII * Base_RII / NumTotalRegras_RII

# Verificação do Status
    Status_RII = "OK" if Ponto_RII == Base_RII else "NOK"

    return Ponto_RII, Status_RII

# ------------------------------------
#[R3] - Terceira Etapa: FIREWALL COM COMUNICAÇÃO EXTERNA (INTERNET)
# ------------------------------------
def verificar_comunicacao_externa_RIII():
    print("\n[Terceira Regra] - Acesso à Internet Bloqueada por padrão.")

# Informativo ao Usuário
    print("O Firewall deve ter a comunicação com a internet bloqueada.")
    print("Caso o ambiente não seja aberto para a internet, então está correto. Caso contrário, está errado.")

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


# Executa a verificação Para saber se alguma variável armazenou dados incorretos ou vazios e armazena os resultados

Ponto_RI, Status_RI = verificar_regra_bloqueio_RI()
Ponto_RII, Status_RII = verificar_regra_bloqueio_RII()
Ponto_RIII, Status_RIII = verificar_comunicacao_externa_RIII()


if None not in [Ponto_RI, Ponto_RII, Ponto_RIII, Status_RI, Status_RII, Status_RIII]:

# Relatório Final (SER DISPOSTO SÓ AO FINAL DE TODo O CODIGO)

# Pontuação das Regras de Pedra
    print("\n Pontuação: ")
    print("--------------------------")
    print(f"RI = {Ponto_RI}")
    print(f"R2 = {Ponto_RII}")
    print(f"R3 = {Ponto_RIII}")


# Status das Regras de Pedra
    print("\n Status: ")
    print("--------------------------")
    print(f"RI = {Status_RI}")
    print(f"R2 = {Status_RII}")
    print(f"R3 = {Status_RIII}")


print("\n✅ Verificação concluída!")

