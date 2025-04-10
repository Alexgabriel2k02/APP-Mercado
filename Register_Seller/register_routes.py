from flask import Blueprint, request, render_template, redirect, url_for
from werkzeug.security import generate_password_hash
from Register_Seller.register_model import Seller, db

register_routes = Blueprint('register_routes', __name__, url_prefix='/register')

@register_routes.route('/', methods=['GET', 'POST'])
def registrar_vendedor():
    if request.method == 'GET':
        # Exibir o formulário de registro
        return render_template('register_seller.html')

    try:
        # Obter dados do formulário
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        cnpj = request.form.get('cnpj')
        phone = request.form.get('phone')

        # Validar campos obrigatórios
        if not name or not email or not password:
            return render_template('register_seller.html', error="Preencha todos os campos obrigatórios.")

        # Verificar se o vendedor já existe
        if Seller.query.filter_by(email=email).first():
            return render_template('register_seller.html', error="Email já registrado.")

        # Criar novo vendedor
        hashed_password = generate_password_hash(password)
        new_seller = Seller(name=name, email=email, password=hashed_password, cnpj=cnpj, phone=phone)
        db.session.add(new_seller)
        db.session.commit()

        # Redirecionar para a tela de login após registro bem-sucedido
        return redirect(url_for('login_routes.login'))
    except Exception as e:
        return render_template('register_seller.html', error=f"Ocorreu um erro: {str(e)}")