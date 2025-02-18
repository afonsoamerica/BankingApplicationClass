# Estrutura das Classes

Comecei pensando em uma classe para o usuário que está acessando o banco e duas outras classes para os tipos de conta que ele pode criar: **Conta Corrente** e **Conta Poupança**.

## Classes Implementadas

- **Classe Usuario**
- **Classe ContaCorrente**
- **Classe ContaPoupanca**

---

## Classe Usuario

Representa um usuário do sistema bancário.

### Atributos:
- `nome`: Nome do usuário.
- `cpf`: CPF do usuário (usado como identificador único).
- `senha`: Senha do usuário para autenticação.
- `conta_corrente`: Referência para uma instância de **ContaCorrente** (pode ser **None** se não houver conta criada).
- `conta_poupanca`: Referência para uma instância de **ContaPoupanca** (pode ser **None** se não houver conta criada).

### Métodos:
- `criar_conta_corrente(saldo_inicial)`: Cria uma conta corrente para o usuário, caso ele ainda não possua uma.
- `criar_conta_poupanca(saldo_inicial)`: Cria uma conta poupança para o usuário, caso ele ainda não possua uma.
- `mostrar_saldo()`: Exibe os saldos das contas do usuário e o total do patrimônio.

---

## Classe ContaCorrente

Representa uma conta corrente.

### Atributos:
- `saldo`: Saldo atual da conta corrente.

---

## Classe ContaPoupanca

Representa uma conta poupança.

### Atributos:
- `saldo`: Saldo atual da conta poupança.

---

## Funcionalidades:

- **Criação e gerenciamento de contas**
- **Transferencias entre contas correntes de usuários diferentes**
- **transferências de valor entre conta poupança e conta corrente de um mesmo usuário**
- **Ver seu saldo**
- **Histórico de transações**

