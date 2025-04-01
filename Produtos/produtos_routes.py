from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .produtos_model import (
    listar_produtos,
    produto_por_id,
    adicionar_produto,
    atualizar_produto,
    excluir_produto,
    ProdutoNaoEncontrado
)

# Criar o blueprint para produtos
produtos_blueprint = Blueprint('produtos', __name__, url_prefix='/produtos')

# Rota para listar todos os produtos
@produtos_blueprint.route('/', methods=['GET'])
def obter_produtos():
    produtos = listar_produtos()  # Obtém a lista de produtos do banco de dados
    return render_template('produtos.html', produtos=produtos)

# Rota para exibir detalhes de um produto específico
@produtos_blueprint.route('/<int:id_produto>/detalhes', methods=['GET'])
def exibir_detalhes_produto(id_produto):
    try:
        produto = produto_por_id(id_produto)  # Obtém o produto pelo ID
        return render_template('produto_id.html', produto=produto)
    except ProdutoNaoEncontrado:
        return jsonify({'erro': 'Produto não encontrado'}), 404

# Rota para exibir o formulário de criação de um novo produto
@produtos_blueprint.route('/novo', methods=['GET'])
def exibir_formulario_criar_produto():
    return render_template('criar_produto.html')

# Rota para adicionar um novo produto
@produtos_blueprint.route('/', methods=['POST'])
def criar_produto():
    dados = request.form
    try:
        novo_produto = {
            'nome': dados.get('nome', ""),
            'preco': float(dados.get('preco', 0)),
            'estoque': int(dados.get('estoque', 0))
        }
        adicionar_produto(novo_produto)
        return redirect(url_for('produtos.obter_produtos'))
    except ValueError as e:
        return render_template('criar_produto.html', error=str(e))

# Rota para exibir o formulário de atualização de um produto
@produtos_blueprint.route('/<int:id_produto>/editar', methods=['GET'])
def exibir_formulario_atualizar_produto(id_produto):
    try:
        produto = produto_por_id(id_produto)
        return render_template('produto_update.html', produto=produto)
    except ProdutoNaoEncontrado:
        return jsonify({'erro': 'Produto não encontrado'}), 404

# ✅ Rota corrigida para aceitar POST e evitar erro KeyError
@produtos_blueprint.route('/<int:id_produto>', methods=['POST', 'PUT'])
def atualizar_produto_por_id(id_produto):
    if request.method == "POST":
        dados = request.form
        print("Dados recebidos no formulário:", dados)  # ✅ Teste se os dados chegam
    else:
        dados = request.get_json()

    try:
        produto_atualizado = {
            'nome': dados.get('nome', ""),  # Evita erro se nome estiver faltando
            'preco': float(dados.get('preco', 0)),
            'estoque': int(dados.get('estoque', 0))
        }
        atualizar_produto(id_produto, produto_atualizado)

        return redirect(url_for('produtos.exibir_detalhes_produto', id_produto=id_produto))
    except ProdutoNaoEncontrado:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400

# Rota para excluir um produto

@produtos_blueprint.route('/<int:id_produto>/deletar', methods=['POST'])
def deletar_produto(id_produto):
    try:
        excluir_produto(id_produto)  # Exclui o produto
        return redirect(url_for('produtos.obter_produtos'))  # Volta para a lista de produtos
    except ProdutoNaoEncontrado:
        return jsonify({'erro': 'Produto não encontrado'}), 404