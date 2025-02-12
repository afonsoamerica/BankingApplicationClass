# Lista global para armazenar os clientes cadastrados
clientes = []

# Dicionário global para armazenar o histórico de transações de cada cliente (por CPF)
historico_transacoes = {}

# Função para formatar o CPF no padrão XXX.XXX.XXX-XX




# Dicionário global para armazenar as contas poupança (associadas ao CPF)
# Dicionário para armazenar as contas poupança
poupancas = {}  # Inicializa um dicionário para armazenar contas poupança.




#######################################################################################
##########################################################################
#######################################################





def formatar_cpf(cpf):
    """
    Formata o CPF no padrão XXX.XXX.XXX-XX.

    Parâmetros:
        cpf (str): CPF apenas com números.

    Retorna:
        str: CPF formatado.
    """
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

# Função para adicionar um cliente
def adicionar_cliente():
    """
    Adiciona um cliente solicitando os dados pelo terminal.
    """
    print("\nAdicionando um novo cliente...")
    nome = input("Digite o nome do cliente: ")

    # Valida a entrada do CPF apenas com números
    while True:
        cpf = input("Digite o CPF do cliente (apenas números): ")
        if len(cpf) == 11 and cpf.isdigit():
            cpf = formatar_cpf(cpf)
            break
        else:
            print("CPF inválido. Certifique-se de digitar 11 números.")

    # Verifica se o CPF já está cadastrado
    for cliente in clientes:
        if cliente["cpf"] == cpf:
            print("CPF já cadastrado. Use outro CPF.")
            return

    # Solicita a criação de uma senha
    while True:
        senha = input("Crie uma senha para sua conta: ")
        if len(senha) >= 4:
            break
        else:
            print("A senha deve ter pelo menos 4 caracteres.")

    # Gera um ID único baseado no tamanho da lista
    id_cliente = len(clientes) + 1

    # Cria um dicionário para representar o cliente
    cliente = {
        "id": id_cliente,
        "nome": nome,
        "cpf": cpf,
        "senha": senha,
        "saldo": 0.0  # Saldo inicial da conta
    }

    # Adiciona o cliente à lista global
    clientes.append(cliente)

    # Cria um histórico de transações vazio para o cliente
    historico_transacoes[cpf] = []

    print(f"Cliente {nome} adicionado com sucesso!\n")

# Função para adicionar dinheiro à conta
def adicionar_dinheiro():
    """
    Permite adicionar dinheiro à conta de um cliente mediante verificação de CPF e senha.
    """
    print("\nAdicionando dinheiro à conta...")

    # Verifica o CPF
    while True:
        cpf = input("Digite o CPF do cliente (apenas números): ")
        if len(cpf) == 11 and cpf.isdigit():
            cpf = formatar_cpf(cpf)
            break
        else:
            print("CPF inválido. Certifique-se de digitar 11 números.")

    # Verifica se o cliente existe
    cliente = next((cliente for cliente in clientes if cliente["cpf"] == cpf), None)
    if not cliente:
        print("Cliente não encontrado. Verifique o CPF.")
        return

    # Solicita a senha
    senha = input("Digite a senha: ")
    if senha != cliente["senha"]:
        print("Senha incorreta. Operação cancelada.")
        return

    # Solicita o valor a ser depositado
    valor = float(input("Digite o valor a ser adicionado à conta: R$ "))
    if valor <= 0:
        print("Valor inválido. Insira um valor positivo.")
        return

    # Atualiza o saldo do cliente
    cliente["saldo"] += valor

    # Atualiza o histórico de transações
    historico_transacoes[cpf].append(f"Depósito de R${valor:.2f} realizado com sucesso.")

    print(f"Depósito de R${valor:.2f} registrado com sucesso!")
    print("Boleto enviado ao e-mail para depósito bancário.\n")

# Função para transferência de fundos
# Função para transferência de fundos
def transferencia_fundos():
    """
    Realiza uma transferência de fundos entre clientes.
    """
    print("\nIniciando transferência de fundos...")

    # Solicita o CPF de origem
    while True:
        cpf_origem = input("Digite o CPF do cliente de origem (apenas números): ")
        if len(cpf_origem) == 11 and cpf_origem.isdigit():
            cpf_origem = formatar_cpf(cpf_origem)
            break
        else:
            print("CPF inválido. Certifique-se de digitar 11 números.")

    # Solicita o CPF de destino
    while True:
        cpf_destino = input("Digite o CPF do cliente de destino (apenas números): ")
        if len(cpf_destino) == 11 and cpf_destino.isdigit():
            cpf_destino = formatar_cpf(cpf_destino)
            break
        else:
            print("CPF inválido. Certifique-se de digitar 11 números.")
    
    # Solicita o valor da transferência
    valor = float(input("Digite o valor a ser transferido: R$ "))
    if valor <= 0:
        print("Valor inválido. Insira um valor positivo.")
        return

    # Localiza os clientes na lista
    cliente_origem = next((cliente for cliente in clientes if cliente["cpf"] == cpf_origem), None)
    cliente_destino = next((cliente for cliente in clientes if cliente["cpf"] == cpf_destino), None)

    # Verifica se os clientes existem
    if not cliente_origem:
        print("Cliente de origem não encontrado. Verifique o CPF.")
        return
    if not cliente_destino:
        print("Cliente de destino não encontrado. Verifique o CPF.")
        return

    # Verifica a senha do cliente de origem
    senha = input("Digite a senha: ")
    if senha != cliente_origem["senha"]:
        print("Senha incorreta. Operação cancelada.")
        return

    # Realiza a transferência
    cliente_origem["saldo"] -= valor
    cliente_destino["saldo"] += valor

    # Atualiza o histórico de transações
    historico_transacoes[cpf_origem].append(f"Transferência enviada: R${valor:.2f} para {cliente_destino['nome']}.")
    historico_transacoes[cpf_destino].append(f"Transferência recebida: R${valor:.2f} de {cliente_origem['nome']}.")

    print(f"Transferência de R${valor:.2f} realizada com sucesso!")
    print(f"Novo saldo de {cliente_origem['nome']}: R${cliente_origem['saldo']:.2f}")
    print(f"Novo saldo de {cliente_destino['nome']}: R${cliente_destino['saldo']:.2f}\n")


#######################################
######################### P O U P A N C A##########################################
















def criar_conta_poupanca():
    """
    Função para criar uma conta poupança.
    Verifica se o CPF já existe no dicionário de contas poupança.
    Se não existir, adiciona a conta ao dicionário.
    """
    global poupancas  # Garante que estamos manipulando a variável global.
    cpf = input("Digite o CPF (somente números): ")
    
    # Verifica se o CPF já possui uma conta poupança.
    if cpf in poupancas:
        print("Uma conta poupança já existe para este CPF.")
        return

    # Solicita os dados para criar a conta poupança.
    nome = input("Digite o nome do titular: ")
    saldo_inicial = float(input("Adicione um saldo inicial: "))

    # Adiciona a conta poupança ao dicionário.
    poupancas[cpf] = {
        "nome": nome,
        "saldo": saldo_inicial
    }
    print("Conta poupança criada com sucesso!")

def exibir_conta_poupanca():
    """
    Função para exibir os detalhes de uma conta poupança.
    O usuário insere o CPF, e os dados da conta são exibidos, se existirem.
    """
    global poupancas
    cpf = input("Digite o CPF (somente números): ")

    # Verifica se o CPF está no dicionário de contas poupança.
    if cpf in poupancas:
        conta = poupancas[cpf]
        print("=== Dados da Conta Poupança ===")
        print(f"Titular: {conta['nome']}")
        print(f"Saldo: R$ {conta['saldo']:.2f}")
    else:
        print("Conta poupança não encontrada para este CPF.")

def depositar_poupanca():
    """
    Função para realizar depósito em uma conta poupança.
    O usuário insere o CPF e o valor do depósito.
    """
    global poupancas
    cpf = input("Digite o CPF (somente números): ")

    # Verifica se o CPF está no dicionário de contas poupança.
    if cpf in poupancas:
        valor = float(input("Digite o valor do depósito: "))
        if valor <= 0:
            print("Valor inválido. Insira um valor positivo.")
        return


# Verifica se o cliente existe
    cliente = next((cliente for cliente in clientes if cliente["cpf"] == cpf), None)
    if not cliente:
        print("Cliente não encontrado. Verifique o CPF.")
        return



    # Atualiza o saldo do cliente
    cliente["saldo"] += valor

    # Atualiza o histórico de transações
    historico_transacoes[cpf].append(f"Depósito de R${valor:.2f} realizado com sucesso.")

    print(f"Depósito de R${valor:.2f} registrado com sucesso!")
    print("Boleto enviado ao e-mail para depósito bancário.\n")

def sacar_poupanca():
    """
    Função para realizar saque em uma conta poupança.
    O usuário insere o CPF e o valor do saque.
    """
    global poupancas
    cpf = input("Digite o CPF (somente números): ")

    # Verifica se o CPF está no dicionário de contas poupança.
    if cpf in poupancas:
        valor = float(input("Digite o valor do saque: "))
        if 0 < valor <= poupancas[cpf]['saldo']:
            poupancas[cpf]['saldo'] -= valor
            print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
        else:
            print("Saldo insuficiente ou valor inválido.")
    else:
        print("Conta poupança não encontrada para este CPF.")





















def transferir_poupanca_para_corrente():
    """
    Transfere um valor de uma conta poupança para a conta corrente associada ao mesmo CPF.
    """
    global poupancas  # Manipula a variável global de poupanças.
    
    cpf = input("Digite o CPF do titular (somente números): ")
    cpf_formatado = formatar_cpf(cpf)  # Formata o CPF para garantir o padrão correto.
    
    # Verifica se o CPF tem uma conta poupança associada.
    if cpf not in poupancas:
        print("Não há conta poupança associada a este CPF.")
        return

    # Verifica se o CPF tem uma conta corrente associada.
    cliente_corrente = next((cliente for cliente in clientes if cliente["cpf"] == cpf_formatado), None)
    if not cliente_corrente:
        print("Não há conta corrente associada a este CPF.")
        return

    # Solicita o valor da transferência.
    valor = float(input("Digite o valor a ser transferido para a conta corrente: R$ "))
    if valor <= 0:
        print("O valor deve ser maior que zero.")
        return

    # Verifica se há saldo suficiente na conta poupança.
    if poupancas[cpf]["saldo"] < valor:
        print("Saldo insuficiente na conta poupança.")
        return

    # Realiza a transferência.
    poupancas[cpf]["saldo"] -= valor
    cliente_corrente["saldo"] += valor

    print(f"Transferência de R${valor:.2f} da poupança para a conta corrente realizada com sucesso!")
    print(f"Novo saldo da poupança: R${poupancas[cpf]['saldo']:.2f}")
    print(f"Novo saldo da conta corrente: R${cliente_corrente['saldo']:.2f}")

def transferir_corrente_para_poupanca():
    """
    Transfere um valor de uma conta corrente para a conta poupança associada ao mesmo CPF.
    """
    global poupancas  # Manipula a variável global de poupanças.

    cpf = input("Digite o CPF do titular (somente números): ")
    cpf_formatado = formatar_cpf(cpf)  # Formata o CPF para garantir o padrão correto.

    # Verifica se o CPF tem uma conta corrente associada.
    cliente_corrente = next((cliente for cliente in clientes if cliente["cpf"] == cpf_formatado), None)
    if not cliente_corrente:
        print("Não há conta corrente associada a este CPF.")
        return

    # Verifica se o CPF tem uma conta poupança associada.
    if cpf not in poupancas:
        print("Não há conta poupança associada a este CPF.")
        return

    # Solicita o valor da transferência.
    valor = float(input("Digite o valor a ser transferido para a conta poupança: R$ "))
    if valor <= 0:
        print("O valor deve ser maior que zero.")
        return

    # Verifica se há saldo suficiente na conta corrente.
    if cliente_corrente["saldo"] < valor:
        print("Saldo insuficiente na conta corrente.")
        return

    # Realiza a transferência.
    cliente_corrente["saldo"] -= valor
    poupancas[cpf]["saldo"] += valor

    print(f"Transferência de R${valor:.2f} da conta corrente para a poupança realizada com sucesso!")
    print(f"Novo saldo da conta corrente: R${cliente_corrente['saldo']:.2f}")
    print(f"Novo saldo da poupança: R${poupancas[cpf]['saldo']:.2f}")





























##########################################################################################################


   
# Função para exibir o histórico de transações de um cliente
def exibir_historico():
    """
    Exibe o histórico de transações de um cliente mediante verificação de CPF.
    """
    print("\nExibindo histórico de transações...")

    # CPF do cliente
    while True:
        cpf = input("Digite o CPF do cliente (apenas números): ")
        if len(cpf) == 11 and cpf.isdigit():
            cpf = formatar_cpf(cpf)
            break
        else:
            print("CPF inválido. Certifique-se de digitar 11 números.")

    # Verifica se o cliente existe
    if cpf not in historico_transacoes:
        print("Cliente não encontrado.")
        return

    # Exibe o histórico de transações
    print(f"Histórico de transações para o CPF {cpf}:")
    for transacao in historico_transacoes[cpf]:
        print(f"- {transacao}")
    print()

# Função principal para gerenciar o fluxo interativo
def menu_interativo():
    """
    Apresenta um menu interativo para gerenciar clientes e transações.
    """
    while True:
        print("Menu:")
        print("1. Criar conta corrente")
        print("2. Realizar transferência com a conta corrente")
        print("3. Exibir histórico de transações")
        print("4. Adicionar dinheiro à conta")
        print("5. Criar conta poupança")
        print("6. Adicionar dinheiro à poupança")
        print("7. Retirar dinheiro da poupança")
        print("8. Transferir da poupança para a conta corrente")
        print("9. Transferir da conta corrente para a poupança")
        print("10. exibirpoupanca")
        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            adicionar_cliente()
        elif opcao == 2:
            transferencia_fundos()
        elif opcao == 3:
            exibir_historico()
        elif opcao == 4:
            adicionar_dinheiro()
        elif opcao == 5:
            ##cpf = input("Digite o CPF do cliente: ")
            criar_conta_poupanca()
        elif opcao == 6:
           ## cpf = input("Digite o CPF do cliente: ")
            ##valor = float(input("Digite o valor a adicionar à poupança: "))
            ##def depositar_poupanca()
            depositar_poupanca()
        elif opcao == 7:
            cpf = input("Digite o CPF do cliente: ")
            valor = float(input("Digite o valor a retirar da poupança: "))
            sacar_poupanca()

        elif opcao == 8:
            transferir_poupanca_para_corrente()

        elif opcao == 9:
            transferir_corrente_para_poupanca()




        elif opcao == 10:
            exibir_conta_poupanca()
            
        elif opcao == 11:
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida! Tente novamente.")


# Executa o programa interativo
if __name__ == "__main__":
    menu_interativo()
