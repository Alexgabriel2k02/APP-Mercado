from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .pedidos_model import (
    PedidoNaoEncontrado,
    listar_pedidos,
    pedido_por_id,
    adicionar_pedido,
    atualizar_pedido,
    excluir_pedido
)

pedidos_blueprint = Blueprint('pedidos', __name__)

# Listar pedidos em JSON
@pedidos_blueprint.route('/api/pedidos', methods=['GET'])
def get_pedidos_json():
    return jsonify(listar_pedidos()), 200

# Listar pedidos em HTML
@pedidos_blueprint.route('/pedidos', methods=['GET'])
def get_pedidos_html():
    pedidos = listar_pedidos()
    return render_template("pedidos.html", pedidos=pedidos)

# Detalhes de um pedido em JSON
@pedidos_blueprint.route('/api/pedidos/<int:id_pedido>', methods=['GET'])
def get_pedido_json(id_pedido):
    try:
        pedido = pedido_por_id(id_pedido)
        return jsonify(pedido), 200
    except PedidoNaoEncontrado:
        return jsonify({'message': 'Pedido não encontrado'}), 404

# Detalhes de um pedido em HTML
@pedidos_blueprint.route('/pedidos/<int:id_pedido>', methods=['GET'])
def get_pedido_html(id_pedido):
    try:
        pedido = pedido_por_id(id_pedido)
        return render_template("pedido_id.html", pedido=pedido)
    except PedidoNaoEncontrado:
        return render_template("pedido_id.html", error="Pedido não encontrado"), 404

# Página para adicionar novo pedido
@pedidos_blueprint.route('/pedidos/adicionar', methods=['GET'])
def adicionar_pedido_page():
    return render_template("criar_pedidos.html")

# Criação de pedido em HTML
@pedidos_blueprint.route('/pedidos', methods=['POST'])
def create_pedido_html():
    try:
        cliente_id = int(request.form['cliente_id'])
        produtos = request.form.getlist('produtos')  # Lista de produtos e quantidades
        status = request.form['status']

        novo_pedido = {
            'cliente_id': cliente_id,
            'produtos': produtos,
            'status': status
        }

        adicionar_pedido(novo_pedido)
        return redirect(url_for('pedidos.get_pedidos_html'))
    except ValueError as e:
        return render_template("criar_pedidos.html", error=str(e))

# Criação de pedido em JSON
@pedidos_blueprint.route('/api/pedidos', methods=['POST'])
def create_pedido_json():
    data = request.json
    if 'cliente_id' not in data or 'produtos' not in data:
        return jsonify({'message': 'Campos obrigatórios: cliente_id, produtos'}), 400
    try:
        adicionar_pedido(data)
        return jsonify(data), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

# Rota para deletar um pedido
@pedidos_blueprint.route('/pedidos/<int:id_pedido>/deletar', methods=['POST'])
def delete_pedido(id_pedido):
    try:
        excluir_pedido(id_pedido)
        return redirect(url_for('pedidos.get_pedidos_html'))
    except PedidoNaoEncontrado:
        return render_template("pedidos.html", error="Pedido não encontrado"), 404

# Página para editar um pedido
@pedidos_blueprint.route('/pedidos/<int:id_pedido>/editar', methods=['GET'])
def editar_pedido_page(id_pedido):
    try:
        pedido = pedido_por_id(id_pedido)
        return render_template("pedido_update.html", pedido=pedido)
    except PedidoNaoEncontrado:
        return render_template("pedidos.html", error="Pedido não encontrado"), 404

# Atualizar pedido em HTML
@pedidos_blueprint.route('/pedidos/<int:id_pedido>', methods=['POST'])
def update_pedido_html(id_pedido):
    try:
        status = request.form['status']

        pedido_atualizado = {
            'status': status
        }

        atualizar_pedido(id_pedido, pedido_atualizado)
        return redirect(url_for('pedidos.get_pedido_html', id_pedido=id_pedido))
    except PedidoNaoEncontrado:
        return render_template("pedido_update.html", error="Pedido não encontrado", pedido_id=id_pedido), 404
    except ValueError as e:
        return render_template("pedido_update.html", error=str(e), pedido_id=id_pedido)

# Atualizar pedido em JSON
@pedidos_blueprint.route('/api/pedidos/<int:id_pedido>', methods=['PUT'])
def update_pedido_json(id_pedido):
    data = request.json
    if 'status' not in data:
        return jsonify({'message': 'Campo obrigatório: status'}), 400
    try:
        atualizar_pedido(id_pedido, data)
        return jsonify(data), 200
    except PedidoNaoEncontrado:
        return jsonify({'message': 'Pedido não encontrado'}), 404
    except ValueError as e:
        return jsonify({'message': str(e)}), 400