import pandas as pd
from utils.csv_loader import CsvLoader


class EmployeeService:
    @staticmethod
    def _filter_data(df, start_date=None, end_date=None, store_ids=None):
        filtered = df.copy()
        
        if start_date and 'stat_month' in filtered.columns:
            start_month = start_date[:7] if len(start_date) > 7 else start_date
            filtered = filtered[filtered['stat_month'] >= start_month]
        if end_date and 'stat_month' in filtered.columns:
            end_month = end_date[:7] if len(end_date) > 7 else end_date
            filtered = filtered[filtered['stat_month'] <= end_month]
        if store_ids and 'store_id' in filtered.columns:
            if isinstance(store_ids, str):
                store_ids = [s.strip() for s in store_ids.split(',') if s.strip()]
            if store_ids:
                filtered = filtered[filtered['store_id'].isin(store_ids)]
        
        return filtered
    
    @staticmethod
    def _sort_data(df, sort_by=None, sort_order='asc'):
        if sort_by and sort_by in df.columns:
            ascending = sort_order.lower() == 'asc'
            df = df.sort_values(by=sort_by, ascending=ascending)
        return df.reset_index(drop=True)
    
    @staticmethod
    def _filter_by_service_type(df, service_type=None):
        if not service_type or service_type == 'all':
            return df
        type_map = {
            'beauty': ['皮肤管理', '抗衰紧致'],
            'nail': ['美甲美睫'],
            'spa': ['脱毛'],
            'hair': ['纹绣'],
            '皮肤管理': ['皮肤管理'],
            '抗衰紧致': ['抗衰紧致'],
            '脱毛': ['脱毛'],
            '纹绣': ['纹绣'],
            '美甲美睫': ['美甲美睫'],
        }
        allowed_types = type_map.get(service_type, [service_type])
        if 'service_type' in df.columns and allowed_types:
            return df[df['service_type'].isin(allowed_types)]
        return df

    @staticmethod
    def get_ranking(start_date=None, end_date=None, store_ids=None, sort_by='card_amount', sort_order='desc', service_type=None):
        employees = CsvLoader.get_employees()
        stores = CsvLoader.get_stores()
        performance = CsvLoader.get_employee_performance()
        
        filtered = EmployeeService._filter_data(performance, start_date, end_date, store_ids)
        
        if filtered.empty:
            return []
        
        agg_perf = filtered.groupby(['emp_id', 'store_id']).agg({
            'card_amount': 'sum',
            'order_count': 'sum',
            'avg_price': 'mean'
        }).reset_index()
        
        result = pd.merge(agg_perf, employees[['emp_id', 'emp_name', 'position', 'service_type']], on='emp_id', how='left')
        result = pd.merge(result, stores[['store_id', 'store_name']], on='store_id', how='left')
        
        result = EmployeeService._filter_by_service_type(result, service_type)
        
        if result.empty:
            return []
        
        result['card_amount'] = result['card_amount'].round(2)
        result['avg_price'] = result['avg_price'].round(2)
        
        result = result[[
            'emp_id', 'emp_name', 'position', 'service_type',
            'store_id', 'store_name', 'card_amount', 'order_count', 'avg_price'
        ]]
        
        result = EmployeeService._sort_data(result, sort_by, sort_order)
        
        result_list = result.to_dict('records')
        for i, item in enumerate(result_list):
            item['rank'] = i + 1
        
        return result_list
    
    @staticmethod
    def get_orders(start_date=None, end_date=None, store_ids=None, sort_by='order_count', sort_order='desc', service_type=None):
        employees = CsvLoader.get_employees()
        stores = CsvLoader.get_stores()
        performance = CsvLoader.get_employee_performance()
        
        filtered = EmployeeService._filter_data(performance, start_date, end_date, store_ids)
        
        if filtered.empty:
            return []
        
        agg_perf = filtered.groupby(['emp_id', 'store_id']).agg({
            'card_amount': 'sum',
            'order_count': 'sum',
            'avg_price': 'mean'
        }).reset_index()
        
        result = pd.merge(agg_perf, employees[['emp_id', 'emp_name', 'position', 'service_type']], on='emp_id', how='left')
        result = pd.merge(result, stores[['store_id', 'store_name']], on='store_id', how='left')
        
        result = EmployeeService._filter_by_service_type(result, service_type)
        
        if result.empty:
            return []
        
        result['card_amount'] = result['card_amount'].round(2)
        result['avg_price'] = result['avg_price'].round(2)
        
        total_orders = result['order_count'].sum()
        result['order_ratio'] = (result['order_count'] / total_orders).round(4) if total_orders > 0 else 0
        
        result = result[[
            'emp_id', 'emp_name', 'position', 'service_type',
            'store_id', 'store_name', 'order_count', 'order_ratio',
            'card_amount', 'avg_price'
        ]]
        
        result = EmployeeService._sort_data(result, sort_by, sort_order)
        
        return result.to_dict('records')
    
    @staticmethod
    def get_employee_trend(emp_id, months=6):
        performance = CsvLoader.get_employee_performance()
        employees = CsvLoader.get_employees()
        stores = CsvLoader.get_stores()
        
        if not emp_id:
            return {'employee': None, 'trend': []}
        
        emp_data = performance[performance['emp_id'] == emp_id].copy()
        if emp_data.empty:
            return {'employee': None, 'trend': []}
        
        emp_data = emp_data.sort_values('stat_month', ascending=False)
        months_list = sorted(emp_data['stat_month'].unique().tolist(), reverse=True)[:months]
        months_list = sorted(months_list)
        
        emp_data = emp_data[emp_data['stat_month'].isin(months_list)]
        
        trend_data = emp_data.groupby('stat_month').agg({
            'card_amount': 'sum',
            'order_count': 'sum',
            'avg_price': 'mean'
        }).reset_index()
        
        trend_data['card_amount'] = trend_data['card_amount'].round(2)
        trend_data['avg_price'] = trend_data['avg_price'].round(2)
        
        emp_info = employees[employees['emp_id'] == emp_id].iloc[0].to_dict() if len(employees[employees['emp_id'] == emp_id]) > 0 else {}
        store_info = {}
        if 'store_id' in emp_info and emp_info['store_id']:
            store_row = stores[stores['store_id'] == emp_info['store_id']]
            if len(store_row) > 0:
                store_info = store_row.iloc[0].to_dict()
        
        employee_full = {
            'empId': emp_info.get('emp_id'),
            'empName': emp_info.get('emp_name'),
            'position': emp_info.get('position'),
            'serviceType': emp_info.get('service_type'),
            'storeId': emp_info.get('store_id'),
            'storeName': store_info.get('store_name'),
        }
        
        trend_list = trend_data.to_dict('records')
        trend_result = []
        for item in trend_list:
            trend_result.append({
                'statMonth': item['stat_month'],
                'cardAmount': float(item['card_amount']),
                'orderCount': int(item['order_count']),
                'avgPrice': float(item['avg_price']),
            })
        
        return {'employee': employee_full, 'trend': trend_result}
