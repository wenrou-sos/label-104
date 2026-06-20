from flask import Blueprint, request, jsonify
from services.member_service import MemberService

member_bp = Blueprint('member', __name__)


def _get_query_params():
    return {
        'store_ids': request.args.get('storeIds'),
        'start_date': request.args.get('startDate'),
        'end_date': request.args.get('endDate'),
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
    days = request.args.get('days', type=int, default=None)
    limit = request.args.get('limit', type=int, default=200)
    data = MemberService.get_churn(**params, days=days, limit=limit)
    return jsonify({'code': 200, 'message': 'success', 'data': data})
