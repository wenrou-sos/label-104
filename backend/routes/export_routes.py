import io
import pandas as pd
from flask import Blueprint, request, jsonify, make_response
from services.store_service import StoreService
from services.project_service import ProjectService
from services.employee_service import EmployeeService
from services.member_service import MemberService
from services.channel_service import ChannelService

export_bp = Blueprint('export', __name__)


def _get_query_params():
    return {
        'start_date': request.args.get('startDate'),
        'end_date': request.args.get('endDate'),
        'store_ids': request.args.get('storeIds')
    }


def _create_csv_response(data, filename):
    if not data:
        df = pd.DataFrame()
    else:
        df = pd.DataFrame(data)
    
    output = io.StringIO()
    df.to_csv(output, index=False, encoding='utf-8-sig')
    output.seek(0)
    
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


@export_bp.route('/stores/metrics', methods=['GET'])
def export_store_metrics():
    params = _get_query_params()
    data = StoreService.get_metrics(**params)
    return _create_csv_response(data, 'store_metrics.csv')


@export_bp.route('/stores/ranking', methods=['GET'])
def export_store_ranking():
    params = _get_query_params()
    data = StoreService.get_ranking(**params)
    return _create_csv_response(data, 'store_ranking.csv')


@export_bp.route('/projects/sales', methods=['GET'])
def export_project_sales():
    params = _get_query_params()
    data = ProjectService.get_sales(**params)
    return _create_csv_response(data, 'project_sales.csv')


@export_bp.route('/projects/margin', methods=['GET'])
def export_project_margin():
    params = _get_query_params()
    data = ProjectService.get_margin(**params)
    return _create_csv_response(data, 'project_margin.csv')


@export_bp.route('/employees/ranking', methods=['GET'])
def export_employee_ranking():
    params = _get_query_params()
    data = EmployeeService.get_ranking(**params)
    return _create_csv_response(data, 'employee_ranking.csv')


@export_bp.route('/employees/orders', methods=['GET'])
def export_employee_orders():
    params = _get_query_params()
    data = EmployeeService.get_orders(**params)
    return _create_csv_response(data, 'employee_orders.csv')


@export_bp.route('/members/cycle', methods=['GET'])
def export_member_cycle():
    params = _get_query_params()
    result = MemberService.get_cycle(store_ids=params['store_ids'])
    data = result.get('distribution', [])
    return _create_csv_response(data, 'member_cycle.csv')


@export_bp.route('/members/recharge', methods=['GET'])
def export_member_recharge():
    params = _get_query_params()
    result = MemberService.get_recharge(store_ids=params['store_ids'])
    data = result.get('stores', [])
    return _create_csv_response(data, 'member_recharge.csv')


@export_bp.route('/members/churn', methods=['GET'])
def export_member_churn():
    params = _get_query_params()
    result = MemberService.get_churn(store_ids=params['store_ids'])
    data = result.get('stores', [])
    return _create_csv_response(data, 'member_churn.csv')


@export_bp.route('/channels/conversion', methods=['GET'])
def export_channel_conversion():
    params = _get_query_params()
    data = ChannelService.get_conversion(**params)
    return _create_csv_response(data, 'channel_conversion.csv')


@export_bp.route('/channels/aov', methods=['GET'])
def export_channel_aov():
    params = _get_query_params()
    data = ChannelService.get_aov(**params)
    return _create_csv_response(data, 'channel_aov.csv')


@export_bp.route('/channels/evaluation', methods=['GET'])
def export_channel_evaluation():
    params = _get_query_params()
    data = ChannelService.get_evaluation(**params)
    return _create_csv_response(data, 'channel_evaluation.csv')
