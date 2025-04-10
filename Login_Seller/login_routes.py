from flask import Blueprint, request, render_template, redirect, url_for
from werkzeug.security import check_password_hash
from Register_Seller.register_model import Seller

login_routes = Blueprint('login_routes', __name__, url_prefix='/login')

@login_routes.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')  # Exibe o formulário de login

    try:
        # Obter dados do formulário
        email = request.form.get('email')
        password = request.form.get('password')

        # Verificar se o vendedor existe
        seller = Seller.query.filter_by(email=email).first()
        if not seller or not check_password_hash(seller.password, password):
            return render_template('login.html', error="Credenciais inválidas.")

        # Redirecionar para a tela de gerenciamento após login bem-sucedido
        return redirect(url_for('managesystem'))
    except Exception as e:
        return render_template('login.html', error=f"Ocorreu um erro: {str(e)}")