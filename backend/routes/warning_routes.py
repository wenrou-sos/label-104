from flask import Blueprint, request, jsonify
from services.warning_service import WarningService

warning_bp = Blueprint('warning', __name__)


@warning_bp.route('/config', methods=['GET'])
def get_config():
    config = WarningService.get_config()
    return jsonify({'code': 200, 'message': 'success', 'data': config})


@warning_bp.route('/config', methods=['POST'])
def save_config():
    data = request.get_json(silent=True) or {}
    config = WarningService.save_config(data)
    return jsonify({'code': 200, 'message': 'success', 'data': config})
