import unittest
from flask_testing import TestCase
from config import app, db
from Pedidos.pedidos_routes import pedidos_blueprint
from Clientes.clientes_model import Cliente
from Produtos.produtos_model import Produto
from Pedidos.pedidos_model import Pedido, pedido_produto

# Classe de teste para a rota de pedidos
class PedidoTestCase(TestCase):
   
    # Configuração da aplicação para os testes
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.register_blueprint(pedidos_blueprint)
        return app
    
    # Configuração do banco de dados para os testes
    def setUp(self):
        db.create_all()
    
        # Cria um cliente para associar ao pedido
        cliente = Cliente(nome="Cliente Teste", email="cliente@teste.com", idade=30)
        db.session.add(cliente)
        db.session.commit()
        
        # Cria um produto para associar ao pedido
        produto = Produto(nome="Produto Teste", preco=10.0, estoque=100)
        db.session.add(produto)
        db.session.commit()
        
        # Adiciona um pedido para testar
        pedido = Pedido(cliente_id=cliente.id, status="ativo")
        db.session.add(pedido)
        db.session.flush()  # Garante que o pedido tenha um ID antes de associar os produtos
        
        # Associa o produto ao pedido
        db.session.execute(
            pedido_produto.insert().values(
                pedido_id=pedido.id,
                produto_id=produto.id,
                quantidade=2
            )
        )
        db.session.commit()

    # Limpa o banco de dados após os testes
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Testa a rota de listagem de pedidos
    def test_get_pedidos(self):
        response = self.client.get('/api/pedidos')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Cliente Teste', response.data)  # Verifica se o nome do cliente está na resposta
        self.assertIn(b'Produto Teste', response.data)  # Verifica se o nome do produto está na resposta

    # Testa a rota de detalhes de um pedido
    def test_get_pedido_por_id(self):
        response = self.client.get('/api/pedidos/1')  # ID do pedido criado no setUp
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ativo', response.data)  # Verifica se o status do pedido está na resposta
        self.assertIn(b'Produto Teste', response.data)  # Verifica se o produto está associado ao pedido

    # Testa a criação de um novo pedido
    def test_create_pedido(self):
        novo_pedido = {
            "cliente_id": 1,  # ID do cliente criado no setUp
            "produtos": [
                {"id": 1, "quantidade": 3}  # ID do produto criado no setUp
            ],
            "status": "ativo"
        }
        response = self.client.post('/api/pedidos', json=novo_pedido)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'"status": "ativo"', response.data)  # Verifica se o status do pedido está correto

    # Testa a exclusão de um pedido
    def test_delete_pedido(self):
        response = self.client.post('/pedidos/1/deletar')  # ID do pedido criado no setUp
        self.assertEqual(response.status_code, 302)  # Redireciona após exclusão
        response = self.client.get('/api/pedidos/1')
        self.assertEqual(response.status_code, 404)  # Verifica se o pedido foi excluído

# Executa os testes
if __name__ == '__main__':
    unittest.main()