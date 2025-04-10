from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Modelo de dados para a tabela Seller
class Seller(db.Model):
    __tablename__ = 'sellers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(18), unique=True, nullable=True)  # Armazena o CNPJ formatado
    phone = db.Column(db.String(15), nullable=True)

    def __init__(self, name, email, password, cnpj, phone):
        self.name = name
        self.email = email
        self.password = password
        self.cnpj = self.formatar_cnpj(cnpj)  # Formata o CNPJ antes de salvar
        self.phone = phone

    @staticmethod
    def formatar_cnpj(cnpj):
        """Remove caracteres não numéricos e formata o CNPJ."""
        cnpj = ''.join(filter(str.isdigit, cnpj))  # Remove caracteres não numéricos
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}" if len(cnpj) == 14 else cnpj

    # Método para retornar um dicionário com os dados do vendedor
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "cnpj": self.cnpj,
            "phone": self.phone,
        }

# Exceção para quando o vendedor não é encontrado
class SellerNotFound(Exception):
    pass

# Validações manuais
def validar_seller(seller_data):
    if not seller_data.get('name'):
        raise ValueError("O nome do vendedor é obrigatório.")
    if not seller_data.get('email'):
        raise ValueError("O email do vendedor é obrigatório.")
    if not seller_data.get('password'):
        raise ValueError("A senha do vendedor é obrigatória.")
    if seller_data.get('cnpj') and len(''.join(filter(str.isdigit, seller_data['cnpj']))) != 14:
        raise ValueError("O CNPJ deve ter 14 caracteres numéricos.")

# Funções para manipular os dados da tabela Seller
def seller_por_id(id_seller):
    seller = Seller.query.get(id_seller)
    if not seller:
        raise SellerNotFound
    return seller.to_dict()

# Função para listar todos os vendedores
def listar_sellers():
    sellers = Seller.query.all()
    return [seller.to_dict() for seller in sellers]

# Função para adicionar um novo vendedor
def adicionar_seller(seller_data):
    # Validação manual dos dados
    validar_seller(seller_data)

    # Criação do vendedor se os dados forem válidos
    novo_seller = Seller(
        name=seller_data['name'],
        email=seller_data['email'],
        password=seller_data['password'],
        cnpj=seller_data.get('cnpj'),
        phone=seller_data.get('phone'),
    )
    
    db.session.add(novo_seller)
    db.session.commit()

# Função para atualizar os dados de um vendedor
def atualizar_seller(id_seller, novos_dados):
    seller = Seller.query.get(id_seller)
    if not seller:
        raise SellerNotFound
    
    # Validação manual dos novos dados
    validar_seller(novos_dados)

    # Atualização dos dados do vendedor
    seller.name = novos_dados['name']
    seller.email = novos_dados.get('email', seller.email)
    seller.password = novos_dados.get('password', seller.password)
    seller.cnpj = Seller.formatar_cnpj(novos_dados.get('cnpj', seller.cnpj))
    seller.phone = novos_dados.get('phone', seller.phone)
    
    # Salva as alterações no banco de dados
    db.session.commit()

# Função para excluir um vendedor
def excluir_seller(id_seller):
    seller = Seller.query.get(id_seller)
    if not seller:
        raise SellerNotFound
    db.session.delete(seller)
    db.session.commit()