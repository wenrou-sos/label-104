from flask import Blueprint, request, jsonify
from services.member_service import MemberService

member_bp = Blueprint('member', __name__)


def _get_query_params():
    return {
        'store_ids': request.args.get('storeIds'),
        'sort_by': request.args.get('sortBy'),
        'sort_order': request.args.get('sortOrder', 'asc')
    }


@member_bp.route('/cycle', methods=['GET'])
def get_cycle():
    params = _get_query_params()
    data = MemberService.get_cycle(**params)
    return jsonify({'code': 200, 'message': 'success', 'data': data})


@member_bp.route('/recharge', methods=['GET'])
def get_recharge():
    params = _get_query_params()
    data = MemberService.get_recharge(**params)
    return jsonify({'code': 200, 'message': 'success', 'data': data})


@member_bp.route('/churn', methods=['GET'])
def get_churn():
    params = _get_query_params()
    sort_by = params.get('sort_by') or 'churn_rate'
    sort_order = params.get('sort_order') or 'desc'
    data = MemberService.get_churn(store_ids=params['store_ids'], sort_by=sort_by, sort_order=sort_order)
    return jsonify({'code': 200, 'message': 'success', 'data': data})
