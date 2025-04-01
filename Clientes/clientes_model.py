from config import db

# Modelo de dados para a tabela Cliente
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=True)  # Idade pode ser opcional
    email = db.Column(db.String(100), nullable=False, unique=True)  # Email único para cada cliente
    observacoes = db.Column(db.Text, nullable=True)  # Observações opcionais

    # Método para inicializar o cliente
    def __init__(self, nome, email, idade=None, observacoes=None):
        # Validações manuais
        if not nome or len(nome) > 100:
            raise ValueError("O nome deve ser preenchido e ter no máximo 100 caracteres.")
        if idade is not None and (not isinstance(idade, int) or idade <= 0):
            raise ValueError("A idade deve ser um número inteiro positivo.")
        if not email or len(email) > 100:
            raise ValueError("O email deve ser preenchido e ter no máximo 100 caracteres.")
        
        # Cria o cliente
        self.nome = nome
        self.idade = idade
        self.email = email
        self.observacoes = observacoes

    # Método para retornar um dicionário com os dados do cliente
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'email': self.email,
            'observacoes': self.observacoes
        }

# Exceção para quando o cliente não é encontrado
class ClienteNaoEncontrado(Exception):
    pass

# Funções para manipular os dados da tabela Cliente
def cliente_por_id(id_cliente):
    cliente = Cliente.query.get(id_cliente)
    if not cliente:
        raise ClienteNaoEncontrado("Cliente não encontrado.")
    return cliente.to_dict()

# Função para listar todos os clientes
def listar_clientes():
    clientes = Cliente.query.all()
    return [cliente.to_dict() for cliente in clientes]

# Função para adicionar um novo cliente
def adicionar_cliente(cliente_data):
    # Validações de dados antes de adicionar
    nome = cliente_data.get('nome')
    email = cliente_data.get('email')
    idade = cliente_data.get('idade')

    # Validações manuais
    if not nome or len(nome) > 100:
        raise ValueError("O nome deve ser preenchido e ter no máximo 100 caracteres.")
    if not email or len(email) > 100:
        raise ValueError("O email deve ser preenchido e ter no máximo 100 caracteres.")
    if idade is not None and (not isinstance(idade, int) or idade <= 0):
        raise ValueError("A idade deve ser um número inteiro positivo.")
    
    # Cria o cliente
    novo_cliente = Cliente(
        nome=nome,
        email=email,
        idade=idade,
        observacoes=cliente_data.get('observacoes')  # Observações é opcional
    )
    
    # Adiciona o cliente ao banco de dados
    db.session.add(novo_cliente)
    db.session.commit()

# Função para atualizar os dados de um cliente
def atualizar_cliente(id_cliente, novos_dados):
    cliente = Cliente.query.get(id_cliente)
    if not cliente:
        raise ClienteNaoEncontrado("Cliente não encontrado.")
    
    # Validações ao atualizar
    nome = novos_dados.get('nome')
    email = novos_dados.get('email')
    idade = novos_dados.get('idade')

    if nome and len(nome) > 100:
        raise ValueError("O nome deve ter no máximo 100 caracteres.")
    if email and len(email) > 100:
        raise ValueError("O email deve ter no máximo 100 caracteres.")
    if idade is not None and (not isinstance(idade, int) or idade <= 0):
        raise ValueError("A idade deve ser um número inteiro positivo.")
   
    # Atualiza os dados do cliente
    cliente.nome = nome if nome else cliente.nome
    cliente.email = email if email else cliente.email
    cliente.idade = idade if idade else cliente.idade
    cliente.observacoes = novos_dados.get('observacoes', cliente.observacoes)  # Observações é opcional
    db.session.commit()

# Função para excluir um cliente
def excluir_cliente(id_cliente):
    cliente = Cliente.query.get(id_cliente)
    if not cliente:
        raise ClienteNaoEncontrado("Cliente não encontrado.")
    db.session.delete(cliente)
    db.session.commit()