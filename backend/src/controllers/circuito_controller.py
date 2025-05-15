from flask import Blueprint, jsonify, request
from src.services.circuito_service import CircuitoService

circuito_bp = Blueprint('circuitos', __name__)
circuito_service = CircuitoService()

@circuito_bp.route('/circuitos', methods=['GET'])
def get_circuitos():
    circuitos = circuito_service.get_all_circuitos()
    return jsonify([circuito.to_dict() for circuito in circuitos])

@circuito_bp.route('/circuitos/<string:nome>', methods=['GET'])
def get_circuito(nome):
    circuito = circuito_service.get_circuito_by_nome(nome)
    if circuito:
        return jsonify(circuito.to_dict())
    return jsonify({"error": "Circuito não encontrado"}), 404

@circuito_bp.route('/circuitos', methods=['POST'])
def add_circuito():
    data = request.get_json()
    circuito = circuito_service.add_circuito(data)
    if circuito:
        return jsonify(circuito.to_dict()), 201
    return jsonify({"error": "Circuito já existe"}), 400

@circuito_bp.route('/circuitos/<string:nome>', methods=['PUT'])
def update_circuito(nome):
    data = request.get_json()
    circuito = circuito_service.update_circuito(nome, data)
    if circuito:
        return jsonify(circuito.to_dict())
    return jsonify({"error": "Circuito não encontrado"}), 404

@circuito_bp.route('/circuitos/<string:nome>', methods=['DELETE'])
def delete_circuito(nome):
    if circuito_service.delete_circuito(nome):
        return jsonify({"message": "Circuito removido com sucesso"})
    return jsonify({"error": "Circuito não encontrado"}), 404 