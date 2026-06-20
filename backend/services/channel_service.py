import pandas as pd
import numpy as np
from utils.csv_loader import CsvLoader
from services.channel_cost_service import ChannelCostService


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
    def get_evaluation(start_date=None, end_date=None, store_ids=None, sort_by='roi', sort_order='desc'):
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
        
        costs_map = ChannelCostService.get_costs_by_period(start_date, end_date)
        result['total_cost'] = result['channel_id'].map(lambda cid: costs_map.get(cid, 0.0))
        
        result['roi'] = np.where(
            result['total_cost'] > 0,
            ((result['total_revenue'] - result['total_cost']) / result['total_cost'] * 100).round(2),
            None
        )
        
        result['profit'] = (result['total_revenue'] - result['total_cost']).round(2)
        
        max_revenue = result['total_revenue'].max() if not result.empty else 1
        max_conv = result['conversion_rate'].max() if not result.empty else 1
        max_aov = result['avg_price'].max() if not result.empty else 1
        
        result['revenue_score'] = np.where(max_revenue > 0, (result['total_revenue'] / max_revenue * 30), 0).round(2)
        result['conv_score'] = np.where(max_conv > 0, (result['conversion_rate'] / max_conv * 25), 0).round(2)
        result['aov_score'] = np.where(max_aov > 0, (result['avg_price'] / max_aov * 20), 0).round(2)
        
        valid_roi = result[result['roi'].notna()]['roi']
        if len(valid_roi) > 0:
            max_roi = valid_roi.max()
            min_roi = valid_roi.min()
            roi_range = max_roi - min_roi if max_roi != min_roi else 1
            result['roi_score'] = np.where(
                result['roi'].notna(),
                ((result['roi'] - min_roi) / roi_range * 25).round(2),
                0
            )
        else:
            result['roi_score'] = 0
        
        result['total_score'] = (result['revenue_score'] + result['conv_score'] + result['aov_score'] + result['roi_score']).round(2)
        
        def get_suggestion(row):
            roi = row['roi']
            conv_rate = row['conversion_rate']
            cost = row['total_cost']
            revenue = row['total_revenue']
            
            if roi is None:
                return '暂未录入成本，请补充投放成本数据'
            
            if roi >= 200:
                if conv_rate > 0.03:
                    return 'ROI极高且转化稳定，建议加大投放预算，抢占更多流量'
                else:
                    return 'ROI高但转化偏低，建议优化落地页提升转化率，进一步放大收益'
            elif roi >= 100:
                if cost > 15000:
                    return 'ROI良好但成本较高，可尝试精细化投放控制成本'
                else:
                    return 'ROI良好且成本可控，建议维持当前投放节奏'
            elif roi >= 50:
                if conv_rate < 0.02:
                    return 'ROI一般且转化偏低，优先优化转化链路降低获客成本'
                else:
                    return 'ROI中等，建议测试新素材提升点击和转化'
            elif roi >= 0:
                if cost > 10000:
                    return 'ROI偏低且成本高，建议缩窄投放人群，减少低效流量'
                else:
                    return 'ROI偏低，建议分析客户质量，考虑提升客单价策略'
            else:
                if conv_rate > 0.025:
                    return 'ROI为负但转化尚可，建议从客单价和成本两端优化，先保本再盈利'
                else:
                    return 'ROI为负且转化低，建议暂停投放或全面调整投放策略'
        
        result['suggestion'] = result.apply(get_suggestion, axis=1)
        
        def get_roi_level(roi):
            if roi is None:
                return 'unknown'
            if roi >= 200:
                return 'excellent'
            elif roi >= 100:
                return 'good'
            elif roi >= 50:
                return 'medium'
            elif roi >= 0:
                return 'low'
            else:
                return 'negative'
        
        result['roi_level'] = result['roi'].apply(get_roi_level)
        
        result['click_rate'] = result['click_rate'].round(4)
        result['conversion_rate'] = result['conversion_rate'].round(4)
        result['avg_price'] = result['avg_price'].round(2)
        result['total_revenue'] = result['total_revenue'].round(2)
        result['total_cost'] = result['total_cost'].round(2)
        
        result = result[[
            'channel_id', 'channel_name', 'channel_type',
            'exposure_count', 'click_count', 'arrival_count',
            'click_rate', 'conversion_rate', 'avg_price',
            'total_revenue', 'total_cost', 'profit', 'roi', 'roi_level',
            'revenue_score', 'conv_score', 'aov_score', 'roi_score',
            'total_score', 'suggestion'
        ]]
        
        result = ChannelService._sort_data(result, sort_by, sort_order)
        
        return result.to_dict('records')
