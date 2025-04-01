import os
from config import app, db
from flask import render_template
from Produtos.produtos_routes import produtos_blueprint
from Clientes.clientes_routes import clientes_blueprint
from Pedidos.pedidos_routes import pedidos_blueprint

# Registrar os blueprints
app.register_blueprint(produtos_blueprint)
app.register_blueprint(clientes_blueprint)
app.register_blueprint(pedidos_blueprint)

# Criar todas as tabelas no banco de dados
with app.app_context():
    db.create_all()

# Rota para a página principal (home)
@app.route('/')
def home():
    return render_template('index.html')  # Substitua 'index.html' pelo nome do seu arquivo

# Executar a aplicação
if __name__ == '__main__':
    app.run(host=app.config.get("HOST", "127.0.0.1"), port=app.config.get('PORT', 8000), debug=app.config.get('DEBUG', True))
