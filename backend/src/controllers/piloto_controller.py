from flask import Blueprint, jsonify, request
from src.services.piloto_service import PilotoService

piloto_bp = Blueprint('pilotos', __name__)
piloto_service = PilotoService()

@piloto_bp.route('/pilotos', methods=['GET'])
def get_pilotos():
    pilotos = piloto_service.get_all_pilotos()
    return jsonify([piloto.to_dict() for piloto in pilotos])

@piloto_bp.route('/pilotos/<int:numero>', methods=['GET'])
def get_piloto(numero):
    piloto = piloto_service.get_piloto_by_numero(numero)
    if piloto:
        return jsonify(piloto.to_dict())
    return jsonify({"error": "Piloto não encontrado"}), 404

@piloto_bp.route('/pilotos', methods=['POST'])
def add_piloto():
    data = request.get_json()
    piloto = piloto_service.add_piloto(data)
    if piloto:
        return jsonify(piloto.to_dict()), 201
    return jsonify({"error": "Piloto já existe"}), 400

@piloto_bp.route('/pilotos/<int:numero>', methods=['PUT'])
def update_piloto(numero):
    data = request.get_json()
    piloto = piloto_service.update_piloto(numero, data)
    if piloto:
        return jsonify(piloto.to_dict())
    return jsonify({"error": "Piloto não encontrado"}), 404

@piloto_bp.route('/pilotos/<int:numero>', methods=['DELETE'])
def delete_piloto(numero):
    if piloto_service.delete_piloto(numero):
        return jsonify({"message": "Piloto removido com sucesso"})
    return jsonify({"error": "Piloto não encontrado"}), 404

@piloto_bp.route('/pilotos/<int:numero>/pontos', methods=['POST'])
def atualizar_pontos(numero):
    data = request.get_json()
    pontos = data.get('pontos', 0)
    piloto = piloto_service.atualizar_pontos(numero, pontos)
    if piloto:
        return jsonify(piloto.to_dict())
    return jsonify({"error": "Piloto não encontrado"}), 404

@piloto_bp.route('/pilotos/<int:numero>/estatisticas', methods=['PUT'])
def atualizar_estatisticas(numero):
    data = request.get_json()
    piloto = piloto_service.atualizar_estatisticas(numero, data)
    if piloto:
        return jsonify(piloto.to_dict())
    return jsonify({"error": "Piloto não encontrado"}), 404 