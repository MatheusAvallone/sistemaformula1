from flask import Blueprint, jsonify, request
from src.services.lenda_service import LendaService

lenda_bp = Blueprint('lendas', __name__)
lenda_service = LendaService()

@lenda_bp.route('/lendas', methods=['GET'])
def get_lendas():
    lendas = lenda_service.get_all_lendas()
    return jsonify([lenda.to_dict() for lenda in lendas])

@lenda_bp.route('/lendas/<string:nome>', methods=['GET'])
def get_lenda(nome):
    lenda = lenda_service.get_lenda_by_nome(nome)
    if lenda:
        return jsonify(lenda.to_dict())
    return jsonify({"error": "Lenda não encontrada"}), 404

@lenda_bp.route('/lendas', methods=['POST'])
def add_lenda():
    data = request.get_json()
    lenda = lenda_service.add_lenda(data)
    if lenda:
        return jsonify(lenda.to_dict()), 201
    return jsonify({"error": "Lenda já existe"}), 400

@lenda_bp.route('/lendas/<string:nome>', methods=['PUT'])
def update_lenda(nome):
    data = request.get_json()
    lenda = lenda_service.update_lenda(nome, data)
    if lenda:
        return jsonify(lenda.to_dict())
    return jsonify({"error": "Lenda não encontrada"}), 404

@lenda_bp.route('/lendas/<string:nome>', methods=['DELETE'])
def delete_lenda(nome):
    if lenda_service.delete_lenda(nome):
        return jsonify({"message": "Lenda removida com sucesso"})
    return jsonify({"error": "Lenda não encontrada"}), 404 