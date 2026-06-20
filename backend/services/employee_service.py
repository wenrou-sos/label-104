import pandas as pd
from utils.csv_loader import CsvLoader


class EmployeeService:
    @staticmethod
    def _filter_data(df, start_date=None, end_date=None, store_ids=None):
        filtered = df.copy()
        
        if start_date and 'stat_month' in filtered.columns:
            filtered = filtered[filtered['stat_month'] >= start_date]
        if end_date and 'stat_month' in filtered.columns:
            filtered = filtered[filtered['stat_month'] <= end_date]
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
    def get_ranking(start_date=None, end_date=None, store_ids=None, sort_by='card_amount', sort_order='desc'):
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
    def get_orders(start_date=None, end_date=None, store_ids=None, sort_by='order_count', sort_order='desc'):
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
