import os
from config import app, db
from flask import Flask, render_template

# Importar os blueprints
from Produtos.produtos_routes import produtos_blueprint
from Clientes.clientes_routes import clientes_blueprint
from Pedidos.pedidos_routes import pedidos_blueprint
from Register_Seller.register_routes import register_routes
from Login_Seller.login_routes import login_routes

# Importar todos os modelos para garantir que sejam registrados no banco de dados
from Register_Seller.register_model import Seller
from Produtos.produtos_model import Produto
from Clientes.clientes_model import Cliente
from Pedidos.pedidos_model import Pedido

# Registrar os blueprints
app.register_blueprint(produtos_blueprint)
app.register_blueprint(clientes_blueprint)
app.register_blueprint(pedidos_blueprint)
app.register_blueprint(register_routes)
app.register_blueprint(login_routes)

# Criar todas as tabelas no banco de dados
with app.app_context():
    db.create_all()

# Rota para a página principal (home)
@app.route('/')
def home():
    return render_template('index.html')  # Substitua 'index.html' pelo nome do seu arquivo

@app.route('/manage')
def managesystem():
    return render_template('managesystem.html')

# Executar a aplicação
if __name__ == '__main__':
    app.run(host=app.config.get("HOST", "127.0.0.1"), port=app.config.get('PORT', 8000), debug=app.config.get('DEBUG', True))
