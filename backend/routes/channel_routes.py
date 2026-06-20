from flask import Blueprint, request, jsonify
from services.channel_service import ChannelService

channel_bp = Blueprint('channel', __name__)


def _get_query_params():
    return {
        'start_date': request.args.get('startDate'),
        'end_date': request.args.get('endDate'),
        'store_ids': request.args.get('storeIds'),
        'sort_by': request.args.get('sortBy'),
        'sort_order': request.args.get('sortOrder', 'asc')
    }


@channel_bp.route('/conversion', methods=['GET'])
def get_conversion():
    params = _get_query_params()
    sort_order = params.pop('sort_order') or 'desc'
    data = ChannelService.get_conversion(**params, sort_order=sort_order)
    return jsonify({'code': 200, 'message': 'success', 'data': data})


@channel_bp.route('/aov', methods=['GET'])
def get_aov():
    params = _get_query_params()
    sort_by = params.pop('sort_by') or 'avg_price'
    sort_order = params.pop('sort_order') or 'desc'
    data = ChannelService.get_aov(**params, sort_by=sort_by, sort_order=sort_order)
    return jsonify({'code': 200, 'message': 'success', 'data': data})


@channel_bp.route('/evaluation', methods=['GET'])
def get_evaluation():
    params = _get_query_params()
    sort_by = params.pop('sort_by') or 'score'
    sort_order = params.pop('sort_order') or 'desc'
    data = ChannelService.get_evaluation(**params, sort_by=sort_by, sort_order=sort_order)
    return jsonify({'code': 200, 'message': 'success', 'data': data})
