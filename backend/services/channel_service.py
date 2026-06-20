import pandas as pd
import numpy as np
from utils.csv_loader import CsvLoader


class ChannelService:
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
    def _safe_divide(numerator, denominator, decimals=4):
        result = np.where(denominator > 0, numerator / denominator, 0)
        return pd.Series(result).round(decimals).values
    
    @staticmethod
    def get_conversion(start_date=None, end_date=None, store_ids=None, sort_by=None, sort_order='desc'):
        channels = CsvLoader.get_channels()
        channel_data = CsvLoader.get_channel_data()
        
        filtered = ChannelService._filter_data(channel_data, start_date, end_date, store_ids)
        
        if filtered.empty:
            return []
        
        agg_data = filtered.groupby('channel_id').agg({
            'exposure_count': 'sum',
            'click_count': 'sum',
            'arrival_count': 'sum'
        }).reset_index()
        
        result = pd.merge(agg_data, channels[['channel_id', 'channel_name', 'channel_type']], on='channel_id', how='left')
        
        result['click_rate'] = ChannelService._safe_divide(result['click_count'], result['exposure_count'])
        result['arrival_rate'] = ChannelService._safe_divide(result['arrival_count'], result['click_count'])
        result['conversion_rate'] = ChannelService._safe_divide(result['arrival_count'], result['exposure_count'])
        
        result = ChannelService._sort_data(result, sort_by, sort_order)
        
        return result.to_dict('records')
    
    @staticmethod
    def get_aov(start_date=None, end_date=None, store_ids=None, sort_by='avg_price', sort_order='desc'):
        channels = CsvLoader.get_channels()
        channel_data = CsvLoader.get_channel_data()
        
        filtered = ChannelService._filter_data(channel_data, start_date, end_date, store_ids)
        
        if filtered.empty:
            return []
        
        agg_data = filtered.groupby('channel_id').agg({
            'arrival_count': 'sum',
            'avg_price': 'mean'
        }).reset_index()
        
        result = pd.merge(agg_data, channels[['channel_id', 'channel_name', 'channel_type']], on='channel_id', how='left')
        
        result['avg_price'] = result['avg_price'].round(2)
        result['total_revenue'] = (result['arrival_count'] * result['avg_price']).round(2)
        
        result = ChannelService._sort_data(result, sort_by, sort_order)
        
        return result.to_dict('records')
    
    @staticmethod
    def get_evaluation(start_date=None, end_date=None, store_ids=None, sort_by='score', sort_order='desc'):
        channels = CsvLoader.get_channels()
        channel_data = CsvLoader.get_channel_data()
        
        filtered = ChannelService._filter_data(channel_data, start_date, end_date, store_ids)
        
        if filtered.empty:
            return []
        
        agg_data = filtered.groupby('channel_id').agg({
            'exposure_count': 'sum',
            'click_count': 'sum',
            'arrival_count': 'sum',
            'avg_price': 'mean'
        }).reset_index()
        
        result = pd.merge(agg_data, channels[['channel_id', 'channel_name', 'channel_type']], on='channel_id', how='left')
        
        result['click_rate'] = ChannelService._safe_divide(result['click_count'], result['exposure_count'])
        result['conversion_rate'] = ChannelService._safe_divide(result['arrival_count'], result['exposure_count'])
        result['total_revenue'] = result['arrival_count'] * result['avg_price']
        
        max_revenue = result['total_revenue'].max() if not result.empty else 1
        max_conv = result['conversion_rate'].max() if not result.empty else 1
        max_aov = result['avg_price'].max() if not result.empty else 1
        
        result['revenue_score'] = np.where(max_revenue > 0, (result['total_revenue'] / max_revenue * 40), 0).round(2)
        result['conv_score'] = np.where(max_conv > 0, (result['conversion_rate'] / max_conv * 35), 0).round(2)
        result['aov_score'] = np.where(max_aov > 0, (result['avg_price'] / max_aov * 25), 0).round(2)
        result['score'] = (result['revenue_score'] + result['conv_score'] + result['aov_score']).round(2)
        
        def get_grade(score):
            if score >= 80:
                return 'A'
            elif score >= 60:
                return 'B'
            elif score >= 40:
                return 'C'
            else:
                return 'D'
        
        result['grade'] = result['score'].apply(get_grade)
        
        result['click_rate'] = result['click_rate'].round(4)
        result['conversion_rate'] = result['conversion_rate'].round(4)
        result['avg_price'] = result['avg_price'].round(2)
        result['total_revenue'] = result['total_revenue'].round(2)
        
        result = result[[
            'channel_id', 'channel_name', 'channel_type',
            'exposure_count', 'click_count', 'arrival_count',
            'click_rate', 'conversion_rate', 'avg_price', 'total_revenue',
            'revenue_score', 'conv_score', 'aov_score', 'score', 'grade'
        ]]
        
        result = ChannelService._sort_data(result, sort_by, sort_order)
        
        return result.to_dict('records')
