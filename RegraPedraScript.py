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
    Ponto_RII = round(Res_RII * Base_RII / NumTotalRegras_RII,1)

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
    Ponto_RIV = round(Res_RIV * Base_RIV / NumTotalRegras_RIV,1)

# Determinar o Status
    Status_RIV = "OK" if Ponto_RIV == 1 else "NOK"

    return Ponto_RIV, Status_RIV

# -------------------------------------------------------------------------------------------------------------------------------------------------
#[R5] - Quinta Etapa: REGRAS BASEADAS EM HOST
# -------------------------------------------------------------------------------------------------------------------------------------------------
def verificar_regras_hosts_RV():
    print("\n [Quinta Etapa] - Regras Baseadas em Host")
    print("Os campos de endereço, tanto origem quanto destino, devem ser definidos por IP.")
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
    Ponto_RV = round(Res_RV * Base_RV / NumTotalRegras_RII,1)

# Determinar o Status
    Status_RV = "OK" if Ponto_RV == 1 else "NOK"

    return Ponto_RV, Status_RV

# -------------------------------------------------------------------------------------------------------------------------------------------------
#[R6] - Sexta Etapa: VERIFICAÇÃO DE APLICAÇÕES NÍVEL 5
# -------------------------------------------------------------------------------------------------------------------------------------------------
def verificar_aplicacoes_nivel_RVI():
    print("\n [Sexta Etapa] - Verificação de Aplicações Nível 5")
    print("O Firewall não deve ter regras de criticidade nível 5 devido ao alto risco de comprometer o ambiente.")
    print("Nesta etapa, devemos verificar se há regras com aplicações de alto risco. \n")

# Lista para armazenar as aplicações de nível 5 de risco.
    AplicV = []

    Base_RVI = 1

# Perguntar ao usuário quantas regras possuem aplicação nivel 5 no Firewall.
    try:
        AplVRegras_RVI = int(input("Quantas regras com aplicação nível 5 existem no Firewall?").strip())
        if AplVRegras_RVI < 0:
            raise ValueError
    except ValueError:
        print("ERRO: Valor inválido! Valor não pode ser negativo ou decimal.")
        return None, None

# Cálculo do Resultado
    Res_RVI = NumTotalRegras_RII - AplVRegras_RVI

# Cálculo da Pontuação
    Ponto_RVI = round(Res_RVI * Base_RVI / NumTotalRegras_RII,1)

# Determinar o Status
    Status_RVI = "OK" if Ponto_RVI == 1 else "NOK"

    return Ponto_RVI, Status_RVI

# -------------------------------------------------------------------------------------------------------------------------------------------------
#[R7] & [R8] - Sétima Etapa: VERIFICAÇÃO DE VPNs
# -------------------------------------------------------------------------------------------------------------------------------------------------

# Esta etapa engloba duas regras de pedra em uma só. A regra 7 a respeito de VPN segmentada e a regra 8 a respeito de VPN com controle de acesso
def verificar_vpn_RVII():
    print("\n [Sétima e Oitava Etapa] - Verificação de VPN: Acesso por JumpServer/SRA & Split Tunnel Desabilitado.")
    print("OBS: Nesta análise, VPNs relacionadas ao acesso da TI Safe aos ativos devem ser ignoradas.")
    print("[Parte 7] Procure por regras do cliente referentes a VPN com configuração de JumpServer ou SRA para segmentação do acesso dos usuários entre as redes TI e TO.")
    print("[Parte 8] Procure por regras do cliente referentes a VPN que não permita o acesso do cliente diretamente a todo o ambiente (Split Tunnel)")
    print("Para saber se a regra atende aos critérios desta tarefa, basta analisar se as ZONAS são definidas e os endereços são definidos por IP ou pelo menos uma rede de range curto. ")
    print("Caminhos para fazer essa verificação são: Policies > Nat e Policies > Security. \n")

    Base_RVII = 0.5

# Pergunta referente a Parte 7: VPN para acesso via JumpServer ou SRA

    while True:
        VPN_JumpServer = input("O Firewall possui uma VPN para acesso a TO através de JumpServer ou SRA? (S/N)").strip().upper()
        if VPN_JumpServer in ['S', 'N']:
                break
        print("ERRO: Entrada inválida! Digite apenas 'S' para Sim ou 'N' para Não. ")

    Ponto_RVII = Base_RVII if VPN_JumpServer == 'S' else 0

# Pergunta referente a Parte 8: VPN com controle de acesso ao ambiente (Split Tunnel Desabilitado)
    while True:
        VPN_SplitTunnel = input("O Firewall possui uma VPN que restringe o acesso dos usuário a apenas ambientes permitidos (Split Tunnel Desabilitado) (S/N)").strip().upper()
        if VPN_SplitTunnel in ['S', 'N']:
            break
        print("ERRO: Entrada inválida! Digite 'S' para Sim ou 'N' para Não. ")

    Ponto_RVIII = Base_RVII if VPN_SplitTunnel == 'S' else 0

# Determinar o Status
    Status_RVII = "OK" if Ponto_RVII == 0.5 else "NOK"
    Status_RVIII = "OK" if Ponto_RVIII == 0.5 else "NOK"

    return Ponto_RVII, Status_RVII, Ponto_RVIII, Status_RVIII

# -------------------------------------------------------------------------------------------------------------------------------------------------
#[9] - Nona Etapa: VERIFICAÇÃO DO SECURITY GROUP PROFILE
# -------------------------------------------------------------------------------------------------------------------------------------------------
def verificar_security_profile_RIX():
    print("\n [Nona Etapa] - Verificação de Security Group Profile")
    print("Nessa etapa, precisamos identificar se o profile está em conformidade com os requisitos da Palo Alto")
    print("Requisitos: As incidências de nível MEDIUM, HIGH e CRITICAL devem ser dropados por definição.")
    print("Primeiramente, identifique o Security Group do Firewall. Siga o caminho: Objects > Security Profile Groups")
    print("Verifique também os seguintes perfis de segurança:")
    print("1 - ANTIVIRUS: Objects > Security Profiles > Antivirus")
    print("2 - Anti-Spyware: Objects > Security Profiles > Anti-Spyware")
    print("3 - VULNERABILITY PROTECTION: Objects > Security Profiles > Vulnerability Protection")
    print("4 - FILE BLOCKING: Objects > Security Profiles > File Blocking")
    print("Caso alguma configuração esteja fora do padrão, consulte o gerente responsável. \n")

    Base_RIX = 1
    NumRegra_RIX = NumTotalRegras_RII
# Verificação do Security Group Profile

    while True:
        Check_RIX = input("Todas as regras (exceto Drop e Default) possuem Security Group Profile (com o perfil correto)? (S/N)").strip().upper()
        if Check_RIX in ['S', 'N']:
            break
        print("Entrada inválida: Digite apenas 'S' para sim e 'N' para não. ")

# Caso todas as regras tenham grupo e com o grupo correto:
    if Check_RIX == 'S':

        Res_RIX = NumRegra_RIX
 
    else: # Caso haja pelo menos uma regra sem profile group:
        while True:
            try:
                SecProf_RIX = int(input("Quantas regras não possuem Security Group Profile?"))
                if SecProf_RIX >= 0:
                    break
                else:
                    print("O Número não pode ser negativo.")
            except ValueError:
                print("ERRO: Digite um número inteiro. ")
        Res_RIX = NumRegra_RIX - SecProf_RIX

# Cálculo dos pontos
    Ponto_RIX = round(Res_RIX * Base_RIX / NumTotalRegras_RII,1)

# Cálculo Status
    Status_RIX = "OK" if Ponto_RIX == 1 else "NOK"

    return Ponto_RIX, Status_RIX

# -------------------------------------------------------------------------------------------------------------------------------------------------
#[10] - Décima Etapa: VERIFICAÇÃO DO LOG FORWARD
# -------------------------------------------------------------------------------------------------------------------------------------------------
def verificar_log_forward_RX():
    print("\n [Décima Etapa] - Verificação de Log Forward")
    print("Conferir se as regras possuem Log Forward (END).")
    print("OBS: Ignorar regras do tipo DROP/DENY. \n")

    Base_RX = 1

# Obter a quantidade de regras sem log forward ou então configurado errado.

    try:
        LogRegra_RX = int(input("Quantas regras não possuem log Forward ou estão configuradas errada?"))
        if LogRegra_RX < 0:
            raise ValueError
    except ValueError:
        print("ERRO: Valor inválido! Digite um número diferente de número negativo ou decimal.")

        return None, None

# Cálculo das regras totais - Regras configuradas errado.
    Res_RX = NumTotalRegras_RII - LogRegra_RX

# Cálculo dos Pontos
    Ponto_RX = round(Res_RX * Base_RX / NumTotalRegras_RII,1)

# Cálculo Status
    Status_RX = "OK" if Ponto_RX == 1 else "NOK"

    return Ponto_RX, Status_RX

# -------------------------------------------------------------------------------------------------------------------------------------------------
#[11] - Décima Primeira Etapa: VERIFICAÇÃO DO DNS-PROXY
# -------------------------------------------------------------------------------------------------------------------------------------------------
def verificar_dnsproxy_RXI():
    print("[Décima Primeira Etapa - Verificação Do DNS-PROXY]")
    print("Nesta etapa, devemos verificar se o Firewall possui DNS-Proxy configurado. Para isso, basta seguir o caminho Network > DNS-Proxy")

    Base_RXI = 1

    while True:
        Check_RXI = input("O Firewall analisado possui DNS-Proxy configurado? (S/N)").strip().upper()
        if Check_RXI in ['S', 'N']:
            break
        print("Entrada inválida: Digite apenas 'S' para sim e 'N' para não. ")

# Cálculo de Pontuação
    Ponto_RXI = Base_RXI if Check_RXI == 'S' else 0

# Cálculo de Status
    Status_RXI = "OK" if Check_RXI == 'S' else "NOK"

    return Ponto_RXI, Status_RXI


    


# Executa a verificação Para saber se alguma variável armazenou dados incorretos ou vazios e armazena os resultados

Ponto_RI, Status_RI = verificar_regra_bloqueio_RI()
Ponto_RII, Status_RII = verificar_regra_bloqueio_RII()
Ponto_RIII, Status_RIII = verificar_comunicacao_externa_RIII()
Ponto_RIV, Status_RIV = verificador_regras_aplicacao_RIV()
Ponto_RV, Status_RV = verificar_regras_hosts_RV()
Ponto_RVI, Status_RVI = verificar_aplicacoes_nivel_RVI()
Ponto_RVII, Status_RVII, Ponto_RVIII, Status_RVIII = verificar_vpn_RVII()
Ponto_RIX, Status_RIX = verificar_security_profile_RIX()
Ponto_RX, Status_RX = verificar_log_forward_RX()
Ponto_RXI, Status_RXI = verificar_dnsproxy_RXI()

if None not in [Ponto_RI, Ponto_RII, Ponto_RIII, Ponto_RIV, Ponto_RV, Ponto_RVI, Ponto_RVII, Ponto_RVIII , Ponto_RIX, Ponto_RX, Ponto_RXI, Status_RI, Status_RII, Status_RIII, Status_RIV, Status_RV, Status_RVI, Status_RVII, Status_RVIII, Status_RIX, Status_RX, Status_RXI]:
    
# Somatório dos pontos
    Soma_RegraPedra = Ponto_RI + Ponto_RII + Ponto_RIII + Ponto_RIV + Ponto_RV + Ponto_RVI + Ponto_RVII + Ponto_RVIII + Ponto_RIX + Ponto_RX + Ponto_RXI

# Relatório Final (SER DISPOSTO SÓ AO FINAL DE TODo O CODIGO)

# Pontuação das Regras de Pedra

    largura = 15
    print(f"\n {' ' * 7} PONTUAÇÃO: {' ' * 9}STATUS: ")
    print("-" * 45)
    print(f"{' ' * 10}R1 = {str(Ponto_RI).ljust(largura)} {Status_RI}")
    print(f"{' ' * 10}R2 = {str(Ponto_RII).ljust(largura)} {Status_RII}")
    print(f"{' ' * 10}R3 = {str(Ponto_RIII).ljust(largura)} {Status_RIII}")
    print(f"{' ' * 10}R4 = {str(Ponto_RIV).ljust(largura)} {Status_RIV}")
    print(f"{' ' * 10}R5 = {str(Ponto_RV).ljust(largura)} {Status_RV}")
    print(f"{' ' * 10}R6 = {str(Ponto_RVI).ljust(largura)} {Status_RVI}")
    print(f"{' ' * 10}R7 = {str(Ponto_RVII).ljust(largura)} {Status_RVII}")
    print(f"{' ' * 10}R8 = {str(Ponto_RVIII).ljust(largura)} {Status_RVIII}")
    print(f"{' ' * 10}R9 = {str(Ponto_RIX).ljust(largura)} {Status_RIX}")
    print(f"{' ' * 10}R10 = {str(Ponto_RX).ljust(largura - 1)} {Status_RX}")
    print(f"{' ' * 10}R11 = {str(Ponto_RXI).ljust(largura - 12)} {Status_RXI}")
    
# Nota final da Regra de Pedra
    print(f"\n A PONTUAÇÃO FINAL DO FIREWALL É: \n\n {' ' * 15}{Soma_RegraPedra}")

print("\n✅ Verificação concluída!")
