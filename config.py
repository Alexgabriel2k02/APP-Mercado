import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configurações da aplicação
app = Flask(__name__)
app.config['HOST'] = '0.0.0.0'
app.config['PORT'] = 8000
app.config['DEBUG'] = True

# Configuração do banco de dados SQLite na pasta "database"
os.makedirs("database", exist_ok=True)  # Garante que a pasta "database" exista
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.abspath('database/market.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar o SQLAlchemy
db = SQLAlchemy(app)

# Criar todas as tabelas no banco de dados
with app.app_context():
    db.create_all()
