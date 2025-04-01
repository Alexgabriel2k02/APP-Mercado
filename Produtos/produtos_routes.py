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
produtos_blueprint = Blueprint('produtos', __name__)

# Rota para listar todos os produtos em HTML
@produtos_blueprint.route('/produtos', methods=['GET'])
def obter_produtos():
    produtos = listar_produtos()  # Obtém a lista de produtos do banco de dados
    return render_template('produtos.html', produtos=produtos)

# Rota para obter um produto por ID em JSON
@produtos_blueprint.route('/produtos/<int:id_produto>', methods=['GET'])
def obter_produto_por_id(id_produto):
    try:
        produto = produto_por_id(id_produto)
        return jsonify(produto), 200
    except ProdutoNaoEncontrado:
        return jsonify({'erro': 'Produto não encontrado'}), 404

# Rota para exibir o formulário de criação de um novo produto
@produtos_blueprint.route('/produtos/novo', methods=['GET'])
def exibir_formulario_criar_produto():
    return render_template('criar_produto.html')

# Rota para adicionar um novo produto ao banco de dados
@produtos_blueprint.route('/produtos', methods=['POST'])
def criar_produto():
    dados = request.form  # Obtém os dados do formulário
    try:
        novo_produto = {
            'nome': dados['nome'],
            'preco': float(dados['preco']),
            'estoque': int(dados['estoque'])
        }
        adicionar_produto(novo_produto)  # Função do modelo para salvar no banco
        return redirect(url_for('produtos.obter_produtos'))  # Redireciona para a lista de produtos
    except ValueError as e:
        return render_template('criar_produto.html', error=str(e))

# Rota para atualizar um produto existente
@produtos_blueprint.route('/produtos/<int:id_produto>', methods=['PUT'])
def atualizar_produto_por_id(id_produto):
    dados = request.get_json()
    try:
        atualizar_produto(id_produto, dados)
        return jsonify({'mensagem': 'Produto atualizado com sucesso'}), 200
    except ProdutoNaoEncontrado:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400

# Rota para excluir um produto
@produtos_blueprint.route('/produtos/<int:id_produto>', methods=['DELETE'])
def deletar_produto(id_produto):
    try:
        excluir_produto(id_produto)
        return jsonify({'mensagem': 'Produto excluído com sucesso'}), 200
    except ProdutoNaoEncontrado:
        return jsonify({'erro': 'Produto não encontrado'}), 404