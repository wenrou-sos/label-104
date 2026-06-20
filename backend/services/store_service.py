import pandas as pd
from utils.csv_loader import CsvLoader
from services.warning_service import WarningService


class StoreService:
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
    def _calculate_revenue_change(all_metrics, store_id, current_start, current_end):
        try:
            store_data = all_metrics[all_metrics['store_id'] == store_id].copy()
            if store_data.empty:
                return None, False

            store_data = store_data.sort_values('stat_month')
            months = sorted(store_data['stat_month'].unique().tolist())
            if len(months) < 2:
                return None, False

            current_months = [m for m in months if (not current_start or m >= current_start) and (not current_end or m <= current_end)]
            if not current_months:
                current_months = months[-1:]

            current_revenue = store_data[store_data['stat_month'].isin(current_months)]['revenue'].sum()

            current_month_idx = months.index(current_months[-1]) if current_months[-1] in months else len(months) - 1
            prev_month_idx = current_month_idx - len(current_months)
            if prev_month_idx < 0:
                return None, False

            prev_months = months[max(0, prev_month_idx - len(current_months) + 1):prev_month_idx + 1]
            if not prev_months:
                return None, False

            prev_revenue = store_data[store_data['stat_month'].isin(prev_months)]['revenue'].sum()

            if prev_revenue == 0:
                change_pct = 0.0 if current_revenue == 0 else float('inf') if current_revenue > 0 else float('-inf')
            else:
                change_pct = round(((current_revenue - prev_revenue) / abs(prev_revenue)) * 100, 2)

            threshold = WarningService.get_store_revenue_drop_threshold()
            is_warning = change_pct <= -threshold

            return change_pct, is_warning
        except Exception:
            return None, False
    
    @staticmethod
    def _sort_data(df, sort_by=None, sort_order='asc'):
        if sort_by and sort_by in df.columns:
            ascending = sort_order.lower() == 'asc'
            df = df.sort_values(by=sort_by, ascending=ascending)
        return df.reset_index(drop=True)
    
    @staticmethod
    def get_metrics(start_date=None, end_date=None, store_ids=None, sort_by=None, sort_order='asc'):
        stores = CsvLoader.get_stores()
        metrics = CsvLoader.get_store_metrics()
        all_metrics = metrics.copy()
        
        filtered = StoreService._filter_data(metrics, start_date, end_date, store_ids)
        
        if filtered.empty:
            return []
        
        agg_metrics = filtered.groupby('store_id').agg({
            'revenue': 'sum',
            'customer_price': 'mean',
            'visit_frequency': 'mean',
            'new_customers': 'sum',
            'repeat_rate': 'mean'
        }).reset_index()
        
        result = pd.merge(agg_metrics, stores[['store_id', 'store_name', 'city', 'area']], on='store_id', how='left')
        
        result['revenue'] = result['revenue'].round(2)
        result['customer_price'] = result['customer_price'].round(2)
        result['visit_frequency'] = result['visit_frequency'].round(2)
        result['repeat_rate'] = result['repeat_rate'].round(4)
        
        result = StoreService._sort_data(result, sort_by, sort_order)
        
        records = result.to_dict('records')
        for rec in records:
            change_pct, is_warning = StoreService._calculate_revenue_change(
                all_metrics, rec['store_id'], start_date, end_date
            )
            rec['revenueChange'] = float(change_pct) if change_pct is not None else None
            rec['revenueWarning'] = bool(is_warning) if is_warning is not None else False
        
        return records
    
    @staticmethod
    def get_ranking(start_date=None, end_date=None, store_ids=None, sort_by='revenue', sort_order='desc'):
        metrics = StoreService.get_metrics(start_date, end_date, store_ids, sort_by, sort_order)
        
        for i, item in enumerate(metrics):
            item['rank'] = i + 1
        
        return metrics
    
    @staticmethod
    def get_trend(start_date=None, end_date=None, store_ids=None):
        stores = CsvLoader.get_stores()
        metrics = CsvLoader.get_store_metrics()
        
        filtered = StoreService._filter_data(metrics, start_date, end_date, store_ids)
        
        if filtered.empty:
            return {'months': [], 'stores': []}
        
        months = sorted(filtered['stat_month'].unique().tolist())
        
        store_list = []
        for store_id in filtered['store_id'].unique():
            store_data = filtered[filtered['store_id'] == store_id].sort_values('stat_month')
            
            store_info = stores[stores['store_id'] == store_id].iloc[0]
            
            revenues = []
            customer_prices = []
            visit_frequencies = []
            new_customers_list = []
            
            for month in months:
                month_data = store_data[store_data['stat_month'] == month]
                if not month_data.empty:
                    revenues.append(round(month_data.iloc[0]['revenue'], 2))
                    customer_prices.append(round(month_data.iloc[0]['customer_price'], 2))
                    visit_frequencies.append(round(month_data.iloc[0]['visit_frequency'], 2))
                    new_customers_list.append(int(month_data.iloc[0]['new_customers']))
                else:
                    revenues.append(0)
                    customer_prices.append(0)
                    visit_frequencies.append(0)
                    new_customers_list.append(0)
            
            store_list.append({
                'store_id': store_id,
                'store_name': store_info['store_name'],
                'revenues': revenues,
                'customer_prices': customer_prices,
                'visit_frequencies': visit_frequencies,
                'new_customers': new_customers_list
            })
        
        return {
            'months': months,
            'stores': store_list
        }
