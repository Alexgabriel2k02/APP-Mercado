from config import db
from Clientes.clientes_model import Cliente  # Certifique-se de importar o modelo Cliente
from Produtos.produtos_model import Produto  # Certifique-se de importar o modelo Produto

# Tabela associativa para os produtos no pedido
pedido_produto = db.Table('pedido_produto',
    db.Column('pedido_id', db.Integer, db.ForeignKey('pedido.id'), primary_key=True),
    db.Column('produto_id', db.Integer, db.ForeignKey('produto.id'), primary_key=True),
    db.Column('quantidade', db.Integer, nullable=False)
)

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    data_criacao = db.Column(db.DateTime, default=db.func.now())
    status = db.Column(db.String(50), default='ativo')  # Status do pedido (ativo, concluído, cancelado)
    cliente = db.relationship('Cliente', backref='pedidos')
    produtos = db.relationship('Produto', secondary=pedido_produto, backref='pedidos')

    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'cliente_nome': self.cliente.nome if self.cliente else 'Cliente não encontrado',
            'data_criacao': self.data_criacao.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status,
            'produtos': [
                {
                    'id': produto.id,
                    'nome': produto.nome,
                    'preco': produto.preco,
                    'quantidade': produto_pivot.quantidade
                }
                for produto in self.produtos
                for produto_pivot in db.session.query(pedido_produto).filter_by(pedido_id=self.id, produto_id=produto.id)
            ]
        }

class PedidoNaoEncontrado(Exception):
    pass

def pedido_por_id(id_pedido):
    pedido = Pedido.query.get(id_pedido)
    if not pedido:
        raise PedidoNaoEncontrado
    return pedido.to_dict()

def listar_pedidos():
    pedidos = Pedido.query.all()
    return [pedido.to_dict() for pedido in pedidos]

def adicionar_pedido(pedido_data):
    if 'cliente_id' not in pedido_data or 'produtos' not in pedido_data:
        raise ValueError('Campos obrigatórios: cliente_id, produtos')
    
    # Criar o pedido
    novo_pedido = Pedido(
        cliente_id=pedido_data['cliente_id'],
        status=pedido_data.get('status', 'ativo')
    )
    db.session.add(novo_pedido)
    db.session.flush()  # Garante que o pedido tenha um ID antes de adicionar os produtos

    # Adicionar os produtos ao pedido
    for produto in pedido_data['produtos']:
        produto_id = produto['id']
        quantidade = produto['quantidade']
        db.session.execute(pedido_produto.insert().values(
            pedido_id=novo_pedido.id,
            produto_id=produto_id,
            quantidade=quantidade
        ))

    db.session.commit()

def atualizar_pedido(id_pedido, novos_dados):
    pedido = Pedido.query.get(id_pedido)
    if not pedido:
        raise PedidoNaoEncontrado
    
    if 'status' in novos_dados:
        pedido.status = novos_dados['status']
    db.session.commit()

def excluir_pedido(id_pedido):
    pedido = Pedido.query.get(id_pedido)
    if not pedido:
        raise PedidoNaoEncontrado
    db.session.delete(pedido)
    db.session.commit()