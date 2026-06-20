from flask import Blueprint, request, jsonify
from services.employee_service import EmployeeService

employee_bp = Blueprint('employee', __name__)


def _get_query_params():
    return {
        'start_date': request.args.get('startDate'),
        'end_date': request.args.get('endDate'),
        'store_ids': request.args.get('storeIds'),
        'sort_by': request.args.get('sortBy'),
        'sort_order': request.args.get('sortOrder', 'asc')
    }


@employee_bp.route('/ranking', methods=['GET'])
def get_ranking():
    params = _get_query_params()
    sort_by = params.pop('sort_by') or 'card_amount'
    sort_order = params.pop('sort_order') or 'desc'
    data = EmployeeService.get_ranking(**params, sort_by=sort_by, sort_order=sort_order)
    return jsonify({'code': 200, 'message': 'success', 'data': data})


@employee_bp.route('/orders', methods=['GET'])
def get_orders():
    params = _get_query_params()
    sort_by = params.pop('sort_by') or 'order_count'
    sort_order = params.pop('sort_order') or 'desc'
    data = EmployeeService.get_orders(**params, sort_by=sort_by, sort_order=sort_order)
    return jsonify({'code': 200, 'message': 'success', 'data': data})
