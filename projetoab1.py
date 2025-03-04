class Usuario:
    def __init__(self, nome, cpf, senha):
        self.nome = nome
        self.cpf = cpf
        self.senha = senha
        self.conta_corrente = None
        self.conta_poupanca = None
        self.divida = 0  # Dívida do empréstimo
        self.carteira = {}  # Carteira de moedas estrangeiras e criptomoedas

    def adicionar_moeda_na_carteira(self, nome_moeda, quantidade):
        """Adiciona uma moeda à carteira do usuário."""
        if nome_moeda in self.carteira:
            self.carteira[nome_moeda] += quantidade
        else:
            self.carteira[nome_moeda] = quantidade

    def ver_carteira(self):
        """Exibe a carteira de moedas do usuário com formatação personalizada."""
        if not self.carteira:
            print("Você não possui moedas na carteira.")
        else:
            print("\nSua carteira de moedas:")
            for moeda, quantidade in self.carteira.items():
                if moeda in ["Dólar", "Euro"]:  # Moedas estrangeiras
                    print(f"{moeda}: {quantidade:.2f}")
                else:  # Criptomoedas
                    print(f"{moeda}: {quantidade:.6f}")

    def solicitar_emprestimo(self, valor):
        """Solicita um empréstimo e adiciona o valor à conta corrente, gerando uma dívida com 10% de juros."""
        if not hasattr(self, 'conta_corrente'):
            print("Usuário não possui uma conta corrente para receber o empréstimo.")
            return

        self.conta_corrente.saldo += valor
        self.divida += valor * 1.10  # Dívida com juros de 10%
        print(f"Empréstimo de R$ {valor:.2f} concedido! Você agora deve R$ {self.divida:.2f}.")

    def pagar_emprestimo(self, valor):
        """Permite ao usuário pagar parte ou toda a sua dívida."""
        if self.divida == 0:
            print("Você não possui dívidas de empréstimo.")
            return
        if valor > self.conta_corrente.saldo:
            print("Saldo insuficiente para pagar essa quantia.")
            return

        self.conta_corrente.saldo -= valor
        self.divida -= valor

        if self.divida <= 0:
            self.divida = 0
            print("Parabéns! Você quitou completamente sua dívida.")
        else:
            print(f"Pagamento realizado. Saldo restante da dívida: R$ {self.divida:.2f}")

    def mostrar_saldo(self):
        saldo_cc = self.conta_corrente.saldo if hasattr(self, 'conta_corrente') else 0
        saldo_cp = self.conta_poupanca.saldo if hasattr(self, 'conta_poupanca') else 0
        print(f"Saldo Conta Corrente: R$ {saldo_cc:.2f}")
        print(f"Saldo Conta Poupança: R$ {saldo_cp:.2f}")
        print(f"Total de Patrimônio: R$ {saldo_cc + saldo_cp:.2f}")


class ContaCorrente(Usuario):
    def __init__(self, saldo=0, usuario=None):
        super().__init__(usuario.nome, usuario.cpf, usuario.senha)
        self.saldo = saldo
        self.historico = []  # Histórico de transações
        self.usuario = usuario  # Referência ao usuário

    def realizar_transacao(self, valor, tipo, destino_usuario=None):
        """Realiza a transação e registra no histórico."""
        if tipo == 'transferencia':
            if not hasattr(self.usuario, 'conta_corrente'):
                print("Usuário não possui uma conta corrente para realizar a transferência.")
                return
            if self.saldo < valor:
                print("Saldo insuficiente para a transferência.")
                return

            senha_digitada = input("Digite a sua senha para confirmar a transação: ")
            if senha_digitada != self.usuario.senha:
                print("Senha incorreta. Transação não realizada.")
                return

            if self.usuario.cpf == destino_usuario.cpf:
                print("Não é possível realizar transferência entre a mesma conta.")
                return

            self.saldo -= valor
            destino_usuario.conta_corrente.saldo += valor
            # Adiciona no histórico dos dois usuários
            self.historico.append(f"Transferência de R$ {valor:.2f} para {destino_usuario.nome} ({destino_usuario.cpf}).")
            destino_usuario.conta_corrente.historico.append(f"Recebido R$ {valor:.2f} de {self.usuario.nome} ({self.usuario.cpf}).")
            print(f"Transferência realizada com sucesso!")

        elif tipo == 'deposito_poupanca':
            if not hasattr(self.usuario, 'conta_poupanca'):
                print("Usuário não possui uma conta poupança. Crie uma conta poupança antes de realizar o depósito.")
                return
            if not hasattr(self.usuario, 'conta_corrente'):
                print("Usuário não possui uma conta corrente para realizar o depósito.")
                return

            self.saldo -= valor
            self.usuario.conta_poupanca.saldo += valor
            self.historico.append(f"Depósito de R$ {valor:.2f} na Conta Poupança.")
            print(f"Dinheiro deixado guardado na Poupança para futuras compras.")

        elif tipo == 'retirar_poupanca':
            if not hasattr(self.usuario, 'conta_poupanca'):
                print("Usuário não possui uma conta poupança para realizar a retirada.")
                return
            if valor > self.usuario.conta_poupanca.saldo:
                print("Saldo insuficiente na conta poupança para essa retirada.")
                return
            if not hasattr(self.usuario, 'conta_corrente'):
                print("Usuário não possui uma conta corrente para realizar a retirada.")
                return

            self.saldo += valor
            self.usuario.conta_poupanca.saldo -= valor
            self.historico.append(f"Retirada de R$ {valor:.2f} da Conta Poupança.")
            print(f"Dinheiro da sua Poupança agora pode ser usado na Conta Corrente para pagar contas, fazer compras e realizar transferências.")

        else:
            print("Tipo de transação inválido.")

    def mostrar_historico(self):
        """Exibe o histórico de transações da conta corrente."""
        if not self.historico:
            print("Nenhuma transação realizada.")
        else:
            print("Histórico de Transações:")
            for transacao in self.historico:
                print(transacao)


class ContaPoupanca(Usuario):
    def __init__(self, saldo=0, usuario=None):
        super().__init__(usuario.nome, usuario.cpf, usuario.senha)
        self.saldo = saldo

    def depositar(self, valor):
        """Deposita um valor na conta poupança e aplica um rendimento de 5%."""
        if valor <= 0:
            print("Valor de depósito inválido. O valor deve ser maior que zero.")
            return

        # Calcula o rendimento de 5% sobre o valor depositado
        rendimento = valor * 0.05
        self.saldo += valor + rendimento
        print(f"Depósito de R$ {valor:.2f} realizado. Rendimento de 5%: R$ {rendimento:.2f}.")
        print(f"Saldo atual da poupança: R$ {self.saldo:.2f}")
























































































class Moeda:
    def __init__(self, nome, taxa_conversao):
        self.nome = nome
        self.taxa_conversao = taxa_conversao  # Taxa de conversão para a moeda

    def comprar_moeda(self, valor_em_reais, conta_corrente):
        """Método genérico para comprar moeda (será sobrescrito pelas subclasses)."""
        raise NotImplementedError("Este método deve ser implementado pela subclasse.")


class DinheiroEstrangeiro(Moeda):
    def __init__(self, nome, taxa_conversao):
        super().__init__(nome, taxa_conversao)

    def comprar_moeda(self, valor_em_reais, conta_corrente, usuario):
        """Converte reais para a moeda estrangeira e debita o valor da conta corrente."""
        if valor_em_reais <= 0:
            return "Valor de compra inválido. O valor deve ser maior que zero."

        if conta_corrente.saldo < valor_em_reais:
            return "Saldo insuficiente na conta corrente para realizar a compra."

        # Debita o valor da conta corrente
        conta_corrente.saldo -= valor_em_reais

        # Calcula o valor convertido
        valor_convertido = valor_em_reais / self.taxa_conversao

        # Adiciona a moeda à carteira do usuário
        usuario.adicionar_moeda_na_carteira(self.nome, valor_convertido)

        return f"Você comprou {valor_convertido:.2f} {self.nome}. Saldo atual na conta corrente: R$ {conta_corrente.saldo:.2f}"


class Criptomoeda(Moeda):
    def __init__(self, nome, taxa_conversao):
        super().__init__(nome, taxa_conversao)
        self.senha_fake = self.gerar_senha_fake()  # Gera uma senha fake ao criar a instância

    def gerar_senha_fake(self):
        """Gera uma senha fake para acessar as criptomoedas."""
        import random
        import string
        senha = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        return senha

    def comprar_moeda(self, valor_em_reais, conta_corrente, usuario):
        """Converte reais para criptomoeda e debita o valor da conta corrente."""
        if valor_em_reais <= 0:
            return "Valor de compra inválido. O valor deve ser maior que zero."

        if conta_corrente.saldo < valor_em_reais:
            return "Saldo insuficiente na conta corrente para realizar a compra."

        # Debita o valor da conta corrente
        conta_corrente.saldo -= valor_em_reais

        # Calcula o valor convertido
        valor_convertido = valor_em_reais / self.taxa_conversao

        # Adiciona a moeda à carteira do usuário
        usuario.adicionar_moeda_na_carteira(self.nome, valor_convertido)

        return f"Você comprou {valor_convertido:.6f} {self.nome}. Senha fake: {self.senha_fake}. Saldo atual na conta corrente: R$ {conta_corrente.saldo:.2f}"
































































from abc import ABC, abstractmethod

class SuporteCliente(ABC):
    def __init__(self, nome_cliente, problema):
        self.nome_cliente = nome_cliente
        self.problema = problema
        self.consulta_aberta = False

    @abstractmethod
    def abrir_consulta(self):
        """Abre uma consulta de suporte."""
        pass

    @abstractmethod
    def resolver_problema(self):
        """Tenta resolver o problema do cliente."""
        pass

    @abstractmethod
    def fechar_consulta(self):
        """Fecha a consulta de suporte."""
        pass

# Suporte por E-mail
class SuporteEmail(SuporteCliente):
    def abrir_consulta(self):
        self.consulta_aberta = True
        self.email = input("Digite seu e-mail: ")
        print(f"Consulta por e-mail aberta para {self.nome_cliente}.")
        print(f"E-mail de contato: {self.email}")

    def resolver_problema(self):
        if self.consulta_aberta:
            print(f"Resolvendo problema por e-mail: {self.problema}")
            print(f"Enviando solução para o e-mail: {self.email}...")
        else:
            print("Erro: Consulta não está aberta.")

    def fechar_consulta(self):
        if self.consulta_aberta:
            self.consulta_aberta = False
            print(f"Consulta por e-mail fechada para {self.nome_cliente}.")
        else:
            print("Erro: Consulta já está fechada.")


# Suporte por Chat
class SuporteChat(SuporteCliente):
    def abrir_consulta(self):
        self.consulta_aberta = True
        print(f"Consulta por chat aberta para {self.nome_cliente}.")

    def resolver_problema(self):
        if self.consulta_aberta:
            print(f"Resolvendo problema por chat: {self.problema}")
            print("Enviando solução por chat...")
        else:
            print("Erro: Consulta não está aberta.")

    def fechar_consulta(self):
        if self.consulta_aberta:
            self.consulta_aberta = False
            print(f"Consulta por chat fechada para {self.nome_cliente}.")
        else:
            print("Erro: Consulta já está fechada.")


# Suporte por Telefone

class SuporteTelefone(SuporteCliente):
    def abrir_consulta(self):
        self.consulta_aberta = True
        self.telefone = input("Digite seu número de telefone: ")
        print(f"Consulta por telefone aberta para {self.nome_cliente}.")
        print(f"Telefone de contato: {self.telefone}")

    def resolver_problema(self):
        if self.consulta_aberta:
            print(f"Resolvendo problema por telefone: {self.problema}")
            print(f"Ligando para o número: {self.telefone}...")
        else:
            print("Erro: Consulta não está aberta.")

    def fechar_consulta(self):
        if self.consulta_aberta:
            self.consulta_aberta = False
            print(f"Consulta por telefone fechada para {self.nome_cliente}.")
        else:
            print("Erro: Consulta já está fechada.")

















def menu_suporte():
    while True:
        print("\n--- Suporte ao Cliente ---")
        print("1. Suporte por E-mail")
        print("2. Suporte por Chat")
        print("3. Suporte por Telefone")
        print("4. Voltar ao menu principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "4":
            break

        nome_cliente = input("Digite seu nome: ")
        problema = input("Descreva seu problema: ")

        if opcao == "1":
            suporte = SuporteEmail(nome_cliente, problema)
        elif opcao == "2":
            suporte = SuporteChat(nome_cliente, problema)
        elif opcao == "3":
            suporte = SuporteTelefone(nome_cliente, problema)
        else:
            print("Opção inválida.")
            continue

        suporte.abrir_consulta()
        suporte.resolver_problema()
        suporte.fechar_consulta()







































































usuarios = {}

def menu():







    # Criando instâncias das moedas
    dolar = DinheiroEstrangeiro("Dólar", 5.0)  # 1 dólar = 5 reais
    euro = DinheiroEstrangeiro("Euro", 6.0)    # 1 euro = 6 reais
    bitcoin = Criptomoeda("Bitcoin", 200000.0)  # 1 Bitcoin = 200.000 reais
    ethereum = Criptomoeda("Ethereum", 15000.0)  # 1 Ethereum = 15.000 reais















    while True:
        print("\n--- Menu Principal ---")
        print("1. Criar Usuário")
        print("2. Criar Conta Corrente")
        print("3. Criar Conta Poupança")
        print("4. Ver Saldo")
        print("5. Realizar Transferência")
        print("6. Ver Histórico de Transações")
        print("7. Depositar na Poupança ou Retirar para a Conta Corrente")
        print("8. Solicitar Empréstimo")
        print("9. Pagar Empréstimo")
        print("10. Comprar Moeda Estrangeira ou Criptomoeda")
        print("11. Ver Carteira de Moedas")
        print("12. Suporte ao Cliente")
        print("13. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            senha = input("Senha: ")
            if cpf not in usuarios:
                usuarios[cpf] = Usuario(nome, cpf, senha)
                print("Usuário criado com sucesso!")
            else:
                print("Já existe um usuário com esse CPF.")

        elif opcao == "2":
            cpf = input("Digite o CPF: ")
            if cpf in usuarios:
                saldo_inicial = float(input("Saldo inicial: "))
                usuarios[cpf].conta_corrente = ContaCorrente(saldo_inicial, usuarios[cpf])
                print(f"Conta Corrente criada com saldo de R$ {saldo_inicial:.2f}")
            else:
                print("Usuário não encontrado.")

        elif opcao == "3":
            cpf = input("Digite o CPF: ")
            if cpf in usuarios:
                saldo_inicial = float(input("Saldo inicial: "))
                usuarios[cpf].conta_poupanca = ContaPoupanca(saldo_inicial, usuarios[cpf])
                print(f"Conta Poupança criada com saldo de R$ {saldo_inicial:.2f}")
            else:
                print("Usuário não encontrado.")

        elif opcao == "4":
            cpf = input("Digite o CPF: ")
            if cpf in usuarios:
                usuarios[cpf].mostrar_saldo()
            else:
                print("Usuário não encontrado.")

        elif opcao == "5":
            cpf_origem = input("Digite o CPF do usuário de origem: ")
            if cpf_origem in usuarios:
                cpf_destino = input("Digite o CPF do usuário de destino: ")
                if cpf_destino in usuarios and cpf_origem != cpf_destino:
                    valor = float(input("Digite o valor da transferência: "))
                    usuarios[cpf_origem].conta_corrente.realizar_transacao(valor, 'transferencia', usuarios[cpf_destino])
                else:
                    print("Usuário de destino inválido ou é o mesmo que o de origem.")
            else:
                print("Usuário de origem não encontrado.")

        elif opcao == "6":
            cpf = input("Digite o CPF para ver o histórico: ")
            if cpf in usuarios:
                usuarios[cpf].conta_corrente.mostrar_historico()
            else:
                print("Usuário não encontrado.")

        elif opcao == "7":
            cpf = input("Digite o CPF do usuário: ")
            if cpf in usuarios:
                print("1. Depositar dinheiro na Poupança")
                print("2. Retirar dinheiro da Poupança para a Conta Corrente")
                escolha = input("Escolha uma opção: ")
                valor = float(input("Digite o valor: "))

                if escolha == "1":
                    usuarios[cpf].conta_poupanca.depositar(valor)  # Usa o novo método depositar
                elif escolha == "2":
                    usuarios[cpf].conta_corrente.realizar_transacao(valor, 'retirar_poupanca')
                else:
                    print("Opção inválida.")
            else:
                print("Usuário não encontrado.")

        elif opcao == "8":
            cpf = input("Digite o CPF do usuário: ")
            if cpf in usuarios:
                valor = float(input("Digite o valor do empréstimo: "))
                usuarios[cpf].solicitar_emprestimo(valor)
            else:
                print("Usuário não encontrado.")

        elif opcao == "9":
            cpf = input("Digite o CPF do usuário: ")
            if cpf in usuarios:
                valor = float(input("Digite o valor que deseja pagar: "))
                usuarios[cpf].pagar_emprestimo(valor)
            else:
                print("Usuário não encontrado.")





        
        elif opcao == "10":
            cpf = input("Digite o CPF do usuário: ")
            if cpf in usuarios:
                usuario = usuarios[cpf]
                if not hasattr(usuario, 'conta_corrente'):
                    print("Usuário não possui uma conta corrente.")
                    continue

                print("Escolha a moeda:")
                print("1. Dólar")
                print("2. Euro")
                print("3. Bitcoin")
                print("4. Ethereum")
                escolha = input("Escolha uma opção: ")
                valor = float(input("Digite o valor em reais: "))

                if escolha == "1":
                    print(dolar.comprar_moeda(valor, usuario.conta_corrente, usuario))
                elif escolha == "2":
                    print(euro.comprar_moeda(valor, usuario.conta_corrente, usuario))
                elif escolha == "3":
                    print(bitcoin.comprar_moeda(valor, usuario.conta_corrente, usuario))
                elif escolha == "4":
                    print(ethereum.comprar_moeda(valor, usuario.conta_corrente, usuario))
                else:
                    print("Opção inválida.")
            else:
                print("Usuário não encontrado.")

        elif opcao == "11":
            cpf = input("Digite o CPF do usuário: ")
            if cpf in usuarios:
                usuarios[cpf].ver_carteira()
            else:
                print("Usuário não encontrado.")

        elif opcao == "12":
            menu_suporte()


        elif opcao == "13":
            print("Saindo...")
            break
        else:
            print("Opção inválida ou ainda não implementada.")
menu()
