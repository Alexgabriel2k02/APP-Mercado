from config import db

# Modelo de dados para a tabela Produto
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False)

    # Método para retornar um dicionário com os dados do produto
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'preco': self.preco,
            'estoque': self.estoque
        }

# Exceção para quando o produto não é encontrado
class ProdutoNaoEncontrado(Exception):
    pass

# Validações manuais
def validar_produto(produto_data):
    if not produto_data.get('nome'):
        raise ValueError("O nome do produto é obrigatório.")
    if not isinstance(produto_data.get('preco'), (int, float)) or produto_data['preco'] <= 0:
        raise ValueError("O preço deve ser um número positivo.")
    if not isinstance(produto_data.get('estoque'), int) or produto_data['estoque'] < 0:
        raise ValueError("O estoque deve ser um número inteiro não negativo.")

# Funções para manipular os dados da tabela Produto
def produto_por_id(id_produto):
    produto = Produto.query.get(id_produto)
    if not produto:
        raise ProdutoNaoEncontrado
    return produto.to_dict()

# Função para listar todos os produtos
def listar_produtos():
    produtos = Produto.query.all()
    return [produto.to_dict() for produto in produtos]

# Função para adicionar um novo produto
def adicionar_produto(produto_data):
    # Validação manual dos dados
    validar_produto(produto_data)

    # Criação do produto se os dados forem válidos
    novo_produto = Produto(
        nome=produto_data['nome'],
        preco=produto_data['preco'],
        estoque=produto_data['estoque']
    )
    
    db.session.add(novo_produto)
    db.session.commit()

# Função para atualizar os dados de um produto
def atualizar_produto(id_produto, novos_dados):
    produto = Produto.query.get(id_produto)
    if not produto:
        raise ProdutoNaoEncontrado
    
    # Validação manual dos novos dados
    validar_produto(novos_dados)

    # Atualização dos dados do produto
    produto.nome = novos_dados['nome']
    produto.preco = novos_dados.get('preco', produto.preco)
    produto.estoque = novos_dados.get('estoque', produto.estoque)
    
    # Salva as alterações no banco de dados
    db.session.commit()

# Função para excluir um produto
def excluir_produto(id_produto):
    produto = Produto.query.get(id_produto)
    if not produto:
        raise ProdutoNaoEncontrado
    db.session.delete(produto)
    db.session.commit()