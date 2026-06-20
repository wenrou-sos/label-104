import pandas as pd
import numpy as np
from datetime import datetime
from utils.csv_loader import CsvLoader


class MemberService:
    @staticmethod
    def _filter_data(df, store_ids=None):
        filtered = df.copy()
        
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
    def get_cycle(store_ids=None, sort_by=None, sort_order='asc'):
        stores = CsvLoader.get_stores()
        members = CsvLoader.get_members()
        
        filtered = MemberService._filter_data(members, store_ids)
        
        if filtered.empty:
            return {'distribution': [], 'stores': []}
        
        cycle_bins = [0, 30, 60, 90, 120, 150, 180, float('inf')]
        cycle_labels = ['0-30天', '31-60天', '61-90天', '91-120天', '121-150天', '151-180天', '180天以上']
        
        filtered['cycle_group'] = pd.cut(filtered['recharge_cycle_days'], bins=cycle_bins, labels=cycle_labels, right=True)
        
        distribution = filtered['cycle_group'].value_counts().reindex(cycle_labels, fill_value=0)
        total = len(filtered)
        dist_list = []
        for label in cycle_labels:
            count = int(distribution[label])
            ratio = round(count / total, 4) if total > 0 else 0
            dist_list.append({
                'label': label,
                'count': count,
                'ratio': ratio
            })
        
        store_cycles = filtered.groupby('store_id').agg({
            'recharge_cycle_days': 'mean',
            'member_id': 'count'
        }).reset_index()
        store_cycles.columns = ['store_id', 'avg_cycle_days', 'member_count']
        store_cycles = pd.merge(store_cycles, stores[['store_id', 'store_name']], on='store_id', how='left')
        store_cycles['avg_cycle_days'] = store_cycles['avg_cycle_days'].round(1)
        
        store_cycles = MemberService._sort_data(store_cycles, sort_by, sort_order)
        
        return {
            'distribution': dist_list,
            'stores': store_cycles.to_dict('records')
        }
    
    @staticmethod
    def get_recharge(store_ids=None, sort_by=None, sort_order='asc'):
        stores = CsvLoader.get_stores()
        members = CsvLoader.get_members()
        
        filtered = MemberService._filter_data(members, store_ids)
        
        if filtered.empty:
            return {'overall': {}, 'stores': []}
        
        total_members = len(filtered)
        recharged_count = int(filtered['recharged_in_90d'].sum())
        recharge_rate = round(recharged_count / total_members, 4) if total_members > 0 else 0
        
        total_recharge = float(filtered['total_recharge'].sum())
        avg_recharge = round(total_recharge / total_members, 2) if total_members > 0 else 0
        
        overall = {
            'total_members': total_members,
            'recharged_count': recharged_count,
            'recharge_rate': recharge_rate,
            'total_recharge': round(total_recharge, 2),
            'avg_recharge': avg_recharge
        }
        
        store_recharge = filtered.groupby('store_id').agg({
            'member_id': 'count',
            'recharged_in_90d': 'sum',
            'total_recharge': 'sum'
        }).reset_index()
        store_recharge.columns = ['store_id', 'member_count', 'recharged_count', 'total_recharge']
        store_recharge = pd.merge(store_recharge, stores[['store_id', 'store_name']], on='store_id', how='left')
        store_recharge['recharge_rate'] = (store_recharge['recharged_count'] / store_recharge['member_count']).round(4)
        store_recharge['avg_recharge'] = (store_recharge['total_recharge'] / store_recharge['member_count']).round(2)
        store_recharge['total_recharge'] = store_recharge['total_recharge'].round(2)
        store_recharge['recharged_count'] = store_recharge['recharged_count'].astype(int)
        
        store_recharge = MemberService._sort_data(store_recharge, sort_by, sort_order)
        
        return {
            'overall': overall,
            'stores': store_recharge.to_dict('records')
        }
    
    @staticmethod
    def get_churn(store_ids=None, sort_by=None, sort_order='desc'):
        stores = CsvLoader.get_stores()
        members = CsvLoader.get_members()
        
        filtered = MemberService._filter_data(members, store_ids)
        
        if filtered.empty:
            return {'levels': [], 'stores': []}
        
        today = datetime.now()
        filtered['last_visit_date'] = pd.to_datetime(filtered['last_visit_date'])
        filtered['days_since_visit'] = (today - filtered['last_visit_date']).dt.days
        
        def get_churn_level(days):
            if days <= 30:
                return 'active'
            elif days <= 60:
                return 'warning'
            elif days <= 90:
                return 'risk'
            else:
                return 'churned'
        
        filtered['churn_level'] = filtered['days_since_visit'].apply(get_churn_level)
        
        level_order = ['active', 'warning', 'risk', 'churned']
        level_names = {'active': '活跃', 'warning': '预警', 'risk': '风险', 'churned': '流失'}
        
        level_counts = filtered['churn_level'].value_counts().reindex(level_order, fill_value=0)
        total = len(filtered)
        levels_list = []
        for level in level_order:
            count = int(level_counts[level])
            ratio = round(count / total, 4) if total > 0 else 0
            levels_list.append({
                'level': level,
                'name': level_names[level],
                'count': count,
                'ratio': ratio
            })
        
        store_churn = filtered.groupby('store_id').apply(lambda x: pd.Series({
            'total_members': len(x),
            'active_count': (x['churn_level'] == 'active').sum(),
            'warning_count': (x['churn_level'] == 'warning').sum(),
            'risk_count': (x['churn_level'] == 'risk').sum(),
            'churned_count': (x['churn_level'] == 'churned').sum(),
            'churn_rate': (x['churn_level'] == 'churned').sum() / len(x) if len(x) > 0 else 0
        })).reset_index()
        
        store_churn = pd.merge(store_churn, stores[['store_id', 'store_name']], on='store_id', how='left')
        store_churn['churn_rate'] = store_churn['churn_rate'].round(4)
        
        for col in ['active_count', 'warning_count', 'risk_count', 'churned_count']:
            store_churn[col] = store_churn[col].astype(int)
        
        store_churn = MemberService._sort_data(store_churn, sort_by, sort_order)
        
        return {
            'levels': levels_list,
            'stores': store_churn.to_dict('records')
        }
