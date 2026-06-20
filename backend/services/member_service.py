import pandas as pd
import numpy as np
import hashlib
from datetime import datetime
from utils.csv_loader import CsvLoader
from services.warning_service import WarningService


class MemberService:
    _SURNAMES = [
        '王', '李', '张', '刘', '陈', '杨', '赵', '黄', '周', '吴',
        '徐', '孙', '胡', '朱', '高', '林', '何', '郭', '马', '罗',
        '梁', '宋', '郑', '谢', '韩', '唐', '冯', '于', '董', '萧',
        '程', '曹', '袁', '邓', '许', '傅', '沈', '曾', '彭', '吕'
    ]
    _GIVEN_CHARS = [
        '丽', '娜', '敏', '静', '秀英', '霞', '平', '刚', '桂英',
        '玉兰', '华', '雪', '慧', '琳', '颖', '芳', '洁', '红',
        '梅', '云', '婷', '艳', '娟', '莉', '玲', '倩', '秋',
        '欣', '怡', '佳', '乐', '晨', '悦', '妍', '蕾', '薇',
        '思', '语', '蓉', '菲', '瑶', '梦', '悦', '曦', '萱'
    ]

    @staticmethod
    def _generate_member_name(member_id: str) -> str:
        h = int(hashlib.md5(member_id.encode('utf-8')).hexdigest(), 16)
        surname = MemberService._SURNAMES[h % len(MemberService._SURNAMES)]
        given = MemberService._GIVEN_CHARS[(h >> 8) % len(MemberService._GIVEN_CHARS)]
        return surname + given

    @staticmethod
    def _filter_by_store(df, store_ids=None):
        filtered = df.copy()
        if store_ids and 'store_id' in filtered.columns:
            if isinstance(store_ids, str):
                store_ids = [s.strip() for s in store_ids.split(',') if s.strip()]
            if store_ids:
                filtered = filtered[filtered['store_id'].isin(store_ids)]
        return filtered

    @staticmethod
    def _filter_by_date(df, date_col, start_date=None, end_date=None):
        if not start_date and not end_date:
            return df
        filtered = df.copy()
        if date_col not in filtered.columns:
            return filtered
        col_dt = pd.to_datetime(filtered[date_col], errors='coerce')
        if start_date:
            try:
                sd = pd.to_datetime(start_date)
                filtered = filtered[col_dt >= sd]
                col_dt = pd.to_datetime(filtered[date_col], errors='coerce')
            except Exception:
                pass
        if end_date:
            try:
                ed = pd.to_datetime(end_date)
                filtered = filtered[col_dt <= ed]
            except Exception:
                pass
        return filtered

    @staticmethod
    def _filter_data(df, store_ids=None, date_col='register_date', start_date=None, end_date=None):
        filtered = MemberService._filter_by_store(df, store_ids)
        filtered = MemberService._filter_by_date(filtered, date_col, start_date, end_date)
        return filtered

    @staticmethod
    def get_cycle(store_ids=None, start_date=None, end_date=None):
        stores = CsvLoader.get_stores()
        members = CsvLoader.get_members()

        filtered = MemberService._filter_data(members, store_ids, 'register_date', start_date, end_date)

        new_members = int(len(filtered))

        if filtered.empty:
            return {
                'avg_recharge_cycle': 0,
                'recharge_rate': 0,
                'total_members': 0,
                'active_members': 0,
                'new_members': 0,
                'distribution': [],
                'stores': [],
            }

        total_members = int(len(filtered))
        avg_cycle = float(round(filtered['recharge_cycle_days'].mean(), 1)) if total_members > 0 else 0
        recharged_count = int(filtered['recharged_in_90d'].sum())
        recharge_rate = round(recharged_count / total_members, 4) if total_members > 0 else 0

        churn_threshold = WarningService.get_member_churn_days_threshold()
        today = datetime.now()
        filtered = filtered.copy()
        filtered['last_visit_date_dt'] = pd.to_datetime(filtered['last_visit_date'])
        filtered['days_since_visit'] = (today - filtered['last_visit_date_dt']).dt.days
        active_members = int((filtered['days_since_visit'] < churn_threshold).sum())

        cycle_bins = [0, 30, 60, 90, 120, 150, 180, float('inf')]
        cycle_labels = ['0-30天', '31-60天', '61-90天', '91-120天', '121-150天', '151-180天', '180天以上']
        filtered['cycle_group'] = pd.cut(filtered['recharge_cycle_days'], bins=cycle_bins, labels=cycle_labels, right=True)
        distribution = filtered['cycle_group'].value_counts().reindex(cycle_labels, fill_value=0)
        dist_list = []
        for label in cycle_labels:
            count = int(distribution[label])
            ratio = round(count / total_members, 4) if total_members > 0 else 0
            dist_list.append({'label': label, 'count': count, 'ratio': ratio})

        store_cycles = filtered.groupby('store_id').agg({
            'recharge_cycle_days': 'mean',
            'member_id': 'count',
        }).reset_index()
        store_cycles.columns = ['store_id', 'avg_cycle_days', 'member_count']
        store_cycles = pd.merge(store_cycles, stores[['store_id', 'store_name']], on='store_id', how='left')
        store_cycles['avg_cycle_days'] = store_cycles['avg_cycle_days'].round(1)

        return {
            'avg_recharge_cycle': avg_cycle,
            'recharge_rate': recharge_rate,
            'total_members': total_members,
            'active_members': active_members,
            'new_members': new_members,
            'distribution': dist_list,
            'stores': store_cycles.to_dict('records'),
        }

    @staticmethod
    def get_recharge(store_ids=None, start_date=None, end_date=None):
        stores = CsvLoader.get_stores()
        members = CsvLoader.get_members()

        filtered = MemberService._filter_data(members, store_ids, 'register_date', start_date, end_date)

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
            'avg_recharge': avg_recharge,
        }

        store_recharge = filtered.groupby('store_id').agg({
            'member_id': 'count',
            'recharged_in_90d': 'sum',
            'total_recharge': 'sum',
        }).reset_index()
        store_recharge.columns = ['store_id', 'member_count', 'recharged_count', 'total_recharge']
        store_recharge = pd.merge(store_recharge, stores[['store_id', 'store_name']], on='store_id', how='left')
        store_recharge['recharge_rate'] = (store_recharge['recharged_count'] / store_recharge['member_count']).round(4)
        store_recharge['avg_recharge'] = (store_recharge['total_recharge'] / store_recharge['member_count']).round(2)
        store_recharge['total_recharge'] = store_recharge['total_recharge'].round(2)
        store_recharge['recharged_count'] = store_recharge['recharged_count'].astype(int)

        return {'overall': overall, 'stores': store_recharge.to_dict('records')}

    @staticmethod
    def get_churn(store_ids=None, start_date=None, end_date=None, days=None, limit=200):
        stores = CsvLoader.get_stores()
        members = CsvLoader.get_members()

        filtered = MemberService._filter_data(members, store_ids, 'register_date', start_date, end_date)

        if filtered.empty:
            return {'total': 0, 'list': []}

        if days is None:
            days = WarningService.get_member_churn_days_threshold()

        churn_levels = WarningService.get_member_churn_levels()

        today = datetime.now()
        filtered = filtered.copy()
        filtered['last_visit_date_dt'] = pd.to_datetime(filtered['last_visit_date'])
        filtered['days_since_visit'] = (today - filtered['last_visit_date_dt']).dt.days

        churned = filtered[filtered['days_since_visit'] >= days].copy()

        def get_churn_level(d):
            if d >= churn_levels['high']:
                return 'high'
            elif d >= churn_levels['medium']:
                return 'medium'
            else:
                return 'low'

        churned['level'] = churned['days_since_visit'].apply(get_churn_level)
        churned = pd.merge(churned, stores[['store_id', 'store_name']], on='store_id', how='left')

        churned['member_name'] = churned['member_id'].apply(MemberService._generate_member_name)

        churned = churned.sort_values(by='days_since_visit', ascending=False)
        total = int(len(churned))

        if limit and limit > 0:
            churned = churned.head(limit)

        result = []
        for _, row in churned.iterrows():
            result.append({
                'member_id': str(row['member_id']),
                'member_name': str(row['member_name']),
                'store_name': str(row['store_name']),
                'last_visit_date': row['last_visit_date_dt'].strftime('%Y-%m-%d') if pd.notna(row['last_visit_date_dt']) else '',
                'days_since_last_visit': int(row['days_since_visit']),
                'total_recharge': round(float(row['total_recharge']), 2),
                'total_visits': int(row['total_visits']),
                'level': str(row['level']),
            })

        return {'total': total, 'list': result}
