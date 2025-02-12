class Usuario:
    def __init__(self, nome, cpf, senha):
        self.nome = nome
        self.cpf = cpf
        self.senha = senha
        self.conta_corrente = None
        self.conta_poupanca = None

    def criar_conta_corrente(self, saldo_inicial):
        if self.conta_corrente is None:
            self.conta_corrente = ContaCorrente(saldo_inicial)
            print(f"Conta Corrente criada com saldo de R$ {saldo_inicial:.2f}")
        else:
            print("Usuário já possui uma conta corrente.")

    def criar_conta_poupanca(self, saldo_inicial):
        if self.conta_poupanca is None:
            self.conta_poupanca = ContaPoupanca(saldo_inicial)
            print(f"Conta Poupança criada com saldo de R$ {saldo_inicial:.2f}")
        else:
            print("Usuário já possui uma conta poupança.")

    def mostrar_saldo(self):
        saldo_cc = self.conta_corrente.saldo if self.conta_corrente else 0
        saldo_cp = self.conta_poupanca.saldo if self.conta_poupanca else 0
        print(f"Saldo Conta Corrente: R$ {saldo_cc:.2f}")
        print(f"Saldo Conta Poupança: R$ {saldo_cp:.2f}")
        print(f"Total de Patrimônio: R$ {saldo_cp + saldo_cc:.2f}")

class ContaCorrente:
    def __init__(self, saldo=0):
        self.saldo = saldo

class ContaPoupanca:
    def __init__(self, saldo=0):
        self.saldo = saldo

usuarios = {}

def menu():
    while True:
        print("\n1. Criar Usuário")
        print("2. Criar Conta Corrente")
        print("3. Criar Conta Poupança")
        print("4. Ver Saldo")
        print("5. Sair")
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
                usuarios[cpf].criar_conta_corrente(saldo_inicial)
            else:
                print("Usuário não encontrado.")

        elif opcao == "3":
            cpf = input("Digite o CPF: ")
            if cpf in usuarios:
                saldo_inicial = float(input("Saldo inicial: "))
                usuarios[cpf].criar_conta_poupanca(saldo_inicial)
            else:
                print("Usuário não encontrado.")

        elif opcao == "4":
            cpf = input("Digite o CPF: ")
            if cpf in usuarios:
                usuarios[cpf].mostrar_saldo()
            else:
                print("Usuário não encontrado.")

        elif opcao == "5":
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

menu()
