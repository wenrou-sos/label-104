from flask import Blueprint, request, jsonify
from services.store_service import StoreService

store_bp = Blueprint('store', __name__)


def _get_query_params():
    return {
        'start_date': request.args.get('startDate'),
        'end_date': request.args.get('endDate'),
        'store_ids': request.args.get('storeIds'),
        'sort_by': request.args.get('sortBy'),
        'sort_order': request.args.get('sortOrder', 'asc')
    }


@store_bp.route('/metrics', methods=['GET'])
def get_metrics():
    params = _get_query_params()
    data = StoreService.get_metrics(**params)
    return jsonify({'code': 200, 'message': 'success', 'data': data})


@store_bp.route('/ranking', methods=['GET'])
def get_ranking():
    params = _get_query_params()
    sort_by = params.pop('sort_by') or 'revenue'
    sort_order = params.pop('sort_order') or 'desc'
    data = StoreService.get_ranking(**params, sort_by=sort_by, sort_order=sort_order)
    return jsonify({'code': 200, 'message': 'success', 'data': data})


@store_bp.route('/trend', methods=['GET'])
def get_trend():
    params = _get_query_params()
    data = StoreService.get_trend(
        start_date=params['start_date'],
        end_date=params['end_date'],
        store_ids=params['store_ids']
    )
    return jsonify({'code': 200, 'message': 'success', 'data': data})
