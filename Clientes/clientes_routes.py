from flask import Blueprint, request, jsonify
from .clientes_model import (
    listar_clientes,
    cliente_por_id,
    adicionar_cliente,
    atualizar_cliente,
    excluir_cliente,
    ClienteNaoEncontrado
)

# Criar o blueprint para clientes
clientes_blueprint = Blueprint('clientes', __name__)

# Rota para listar todos os clientes
@clientes_blueprint.route('/clientes', methods=['GET'])
def obter_clientes():
    clientes = listar_clientes()
    return jsonify(clientes), 200

# Rota para obter um cliente por ID
@clientes_blueprint.route('/clientes/<int:id_cliente>', methods=['GET'])
def obter_cliente_por_id(id_cliente):
    try:
        cliente = cliente_por_id(id_cliente)
        return jsonify(cliente), 200
    except ClienteNaoEncontrado:
        return jsonify({'erro': 'Cliente não encontrado'}), 404

# Rota para adicionar um novo cliente
@clientes_blueprint.route('/clientes', methods=['POST'])
def criar_cliente():
    dados = request.get_json()
    try:
        adicionar_cliente(dados)
        return jsonify({'mensagem': 'Cliente criado com sucesso'}), 201
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400

# Rota para atualizar um cliente existente
@clientes_blueprint.route('/clientes/<int:id_cliente>', methods=['PUT'])
def atualizar_cliente_por_id(id_cliente):
    dados = request.get_json()
    try:
        atualizar_cliente(id_cliente, dados)
        return jsonify({'mensagem': 'Cliente atualizado com sucesso'}), 200
    except ClienteNaoEncontrado:
        return jsonify({'erro': 'Cliente não encontrado'}), 404
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400

# Rota para excluir um cliente
@clientes_blueprint.route('/clientes/<int:id_cliente>', methods=['DELETE'])
def deletar_cliente(id_cliente):
    try:
        excluir_cliente(id_cliente)
        return jsonify({'mensagem': 'Cliente excluído com sucesso'}), 200
    except ClienteNaoEncontrado:
        return jsonify({'erro': 'Cliente não encontrado'}), 404