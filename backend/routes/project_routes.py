from flask import Blueprint, request, jsonify
from services.project_service import ProjectService

project_bp = Blueprint('project', __name__)


def _get_query_params():
    return {
        'start_date': request.args.get('startDate'),
        'end_date': request.args.get('endDate'),
        'store_ids': request.args.get('storeIds'),
        'sort_by': request.args.get('sortBy'),
        'sort_order': request.args.get('sortOrder', 'asc')
    }


@project_bp.route('/sales', methods=['GET'])
def get_sales():
    params = _get_query_params()
    data = ProjectService.get_sales(**params)
    return jsonify({'code': 200, 'message': 'success', 'data': data})


@project_bp.route('/margin', methods=['GET'])
def get_margin():
    params = _get_query_params()
    data = ProjectService.get_margin(**params)
    return jsonify({'code': 200, 'message': 'success', 'data': data})


@project_bp.route('/matrix', methods=['GET'])
def get_matrix():
    params = _get_query_params()
    data = ProjectService.get_matrix(
        start_date=params['start_date'],
        end_date=params['end_date'],
        store_ids=params['store_ids']
    )
    return jsonify({'code': 200, 'message': 'success', 'data': data})
