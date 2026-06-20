from flask import Blueprint, request, jsonify
from services.channel_cost_service import ChannelCostService

channel_cost_bp = Blueprint('channel_cost', __name__)


@channel_cost_bp.route('', methods=['GET'])
def get_channel_costs():
    channel_id = request.args.get('channelId')
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    if channel_id:
        costs = ChannelCostService.get_channel_costs(channel_id)
        return jsonify({'code': 200, 'message': 'success', 'data': costs})
    elif start_date or end_date:
        costs = ChannelCostService.get_costs_by_period(start_date, end_date)
        return jsonify({'code': 200, 'message': 'success', 'data': costs})
    else:
        all_costs = ChannelCostService.get_all_costs()
        return jsonify({'code': 200, 'message': 'success', 'data': all_costs})


@channel_cost_bp.route('', methods=['POST'])
def set_channel_cost():
    data = request.get_json(force=True, silent=True) or {}
    channel_id = data.get('channelId') or data.get('channel_id')
    stat_month = data.get('statMonth') or data.get('stat_month')
    cost = data.get('cost') or data.get('channelCost')

    if not channel_id or not stat_month:
        return jsonify({'code': 400, 'message': 'channelId and statMonth are required'}), 400

    if cost is None:
        return jsonify({'code': 400, 'message': 'cost is required'}), 400

    try:
        cost_val = float(cost)
    except (ValueError, TypeError):
        return jsonify({'code': 400, 'message': 'cost must be a number'}), 400

    result = ChannelCostService.set_channel_cost(channel_id, stat_month, cost_val)
    return jsonify({'code': 200, 'message': 'success', 'data': result})


@channel_cost_bp.route('/batch', methods=['POST'])
def batch_set_costs():
    data = request.get_json(force=True, silent=True) or {}
    costs_data = data.get('costs') or data.get('data') or []

    if not costs_data or not isinstance(costs_data, list):
        return jsonify({'code': 400, 'message': 'costs array is required'}), 400

    result = ChannelCostService.batch_set_costs(costs_data)
    return jsonify({'code': 200, 'message': 'success', 'data': result})
