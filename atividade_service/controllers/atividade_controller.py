from flask import Blueprint, jsonify, request
from models import atividade_model
from clients.pessoa_service_client import PessoaServiceClient

atividade_bp = Blueprint('atividade_bp', __name__)

@atividade_bp.route('/', methods=['GET'])
def listar_atividades():
    atividades = atividade_model.listar_atividades()
    return jsonify(atividades)

@atividade_bp.route('/<int:id_atividade>', methods=['GET'])
def obter_atividade(id_atividade):
    try:
        atividade = atividade_model.obter_atividade(id_atividade)
        return jsonify(atividade)
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404

@atividade_bp.route('/<int:id_atividade>/professor/<int:id_professor>', methods=['GET'])
def obter_atividade_para_professor(id_atividade, id_professor):
    try:
        atividade = atividade_model.obter_atividade(id_atividade)
        if not PessoaServiceClient.verificar_leciona(id_professor, atividade['id_disciplina']):
            atividade = atividade.copy()
            atividade.pop('respostas', None)
        return jsonify(atividade)
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404

@atividade_bp.route('/atividades', methods=['POST'])
def criar_atividade_endpoint():
    try:
        dados = request.get_json()
        id_disciplina = dados.get('id_disciplina')
        enunciado = dados.get('enunciado')
        respostas = dados.get('respostas', [])

        if not id_disciplina or not enunciado:
            return jsonify({'erro': 'Campos id_disciplina e enunciado são obrigatórios'}), 400

        nova_atividade = atividade_model.criar_atividade(id_disciplina, enunciado, respostas)
        return jsonify(nova_atividade), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@atividade_bp.route('/<int:id_atividade>/', methods=['PUT'])
def atualizar_atividade_endpoint(id_atividade):
    try:
        dados = request.get_json()
        id_disciplina = dados.get('id_disciplina')
        enunciado = dados.get('enunciado')
        respostas = dados.get('respostas', [])

        if not id_disciplina or not enunciado:
            return jsonify({'erro': 'Campos id_disciplina e enunciado são obrigatórios'}), 400

        atividade_atualizada = atividade_model.atualizar_atividade(id_atividade, id_disciplina, enunciado, respostas)
        if atividade_atualizada:
            return jsonify(atividade_atualizada), 200
        else:
            return jsonify({'erro': 'Atividade não encontrada'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@atividade_bp.route('/<int:id_atividade>/', methods=['DELETE'])
def excluir_atividade_endpoint(id_atividade):
    try:
        sucesso = atividade_model.excluir_atividade(id_atividade)
        if sucesso:
            return jsonify({'mensagem': 'Atividade excluída com sucesso'}), 200
        else:
            return jsonify({'erro': 'Atividade não encontrada'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500