import pandas as pd
from utils.csv_loader import CsvLoader


class ProjectService:
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
    def get_sales(start_date=None, end_date=None, store_ids=None, sort_by=None, sort_order='asc'):
        projects = CsvLoader.get_projects()
        project_sales = CsvLoader.get_project_sales()
        
        filtered = ProjectService._filter_data(project_sales, start_date, end_date, store_ids)
        
        if filtered.empty:
            return []
        
        agg_sales = filtered.groupby('project_id').agg({
            'sales_count': 'sum',
            'sales_amount': 'sum'
        }).reset_index()
        
        result = pd.merge(agg_sales, projects[['project_id', 'project_name', 'category', 'price', 'cost']], on='project_id', how='left')
        
        total_sales = result['sales_amount'].sum()
        result['sales_ratio'] = (result['sales_amount'] / total_sales).round(4) if total_sales > 0 else 0
        result['sales_amount'] = result['sales_amount'].round(2)
        
        result = ProjectService._sort_data(result, sort_by, sort_order)
        
        return result.to_dict('records')
    
    @staticmethod
    def get_margin(start_date=None, end_date=None, store_ids=None, sort_by=None, sort_order='asc'):
        projects = CsvLoader.get_projects()
        project_sales = CsvLoader.get_project_sales()
        
        filtered = ProjectService._filter_data(project_sales, start_date, end_date, store_ids)
        
        if filtered.empty:
            return []
        
        agg_sales = filtered.groupby('project_id').agg({
            'sales_count': 'sum',
            'sales_amount': 'sum'
        }).reset_index()
        
        result = pd.merge(agg_sales, projects[['project_id', 'project_name', 'category', 'price', 'cost']], on='project_id', how='left')
        
        result['total_cost'] = (result['sales_count'] * result['cost']).round(2)
        result['gross_profit'] = (result['sales_amount'] - result['total_cost']).round(2)
        result['gross_margin'] = (result['gross_profit'] / result['sales_amount']).round(4) if result['sales_amount'].sum() > 0 else 0
        
        result = result[[
            'project_id', 'project_name', 'category', 'price', 'cost',
            'sales_count', 'sales_amount', 'total_cost', 'gross_profit', 'gross_margin'
        ]]
        
        result = ProjectService._sort_data(result, sort_by, sort_order)
        
        return result.to_dict('records')
    
    @staticmethod
    def get_matrix(start_date=None, end_date=None, store_ids=None):
        projects = CsvLoader.get_projects()
        project_sales = CsvLoader.get_project_sales()
        
        filtered = ProjectService._filter_data(project_sales, start_date, end_date, store_ids)
        
        if filtered.empty:
            return {'projects': [], 'avg_sales': 0, 'avg_margin': 0}
        
        agg_sales = filtered.groupby('project_id').agg({
            'sales_count': 'sum',
            'sales_amount': 'sum'
        }).reset_index()
        
        result = pd.merge(agg_sales, projects[['project_id', 'project_name', 'category', 'price', 'cost']], on='project_id', how='left')
        
        result['total_cost'] = result['sales_count'] * result['cost']
        result['gross_profit'] = result['sales_amount'] - result['total_cost']
        result['gross_margin'] = result['gross_profit'] / result['sales_amount']
        
        avg_sales = result['sales_amount'].mean()
        avg_margin = result['gross_margin'].mean()
        
        def get_quadrant(row):
            high_sales = row['sales_amount'] >= avg_sales
            high_margin = row['gross_margin'] >= avg_margin
            if high_sales and high_margin:
                return 'q1'
            elif not high_sales and high_margin:
                return 'q2'
            elif not high_sales and not high_margin:
                return 'q3'
            else:
                return 'q4'
        
        result['quadrant'] = result.apply(get_quadrant, axis=1)
        result['sales_amount'] = result['sales_amount'].round(2)
        result['gross_margin'] = result['gross_margin'].round(4)
        
        project_list = result[[
            'project_id', 'project_name', 'category', 'sales_amount',
            'gross_margin', 'quadrant'
        ]].to_dict('records')
        
        return {
            'projects': project_list,
            'avg_sales': round(avg_sales, 2),
            'avg_margin': round(avg_margin, 4)
        }
