import json
import os
from typing import Any, Dict, List, Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
CHANNEL_COST_FILE = os.path.join(DATA_DIR, 'channel_costs.json')

DEFAULT_COSTS: Dict[str, Dict[str, float]] = {
    'C001': {'2024-01': 8000, '2024-02': 8500, '2024-03': 9000, '2024-04': 10000,
             '2024-05': 11000, '2024-06': 9500, '2024-07': 8000, '2024-08': 7500,
             '2024-09': 8000, '2024-10': 9000, '2024-11': 10000, '2024-12': 12000},
    'C002': {'2024-01': 12000, '2024-02': 15000, '2024-03': 18000, '2024-04': 20000,
             '2024-05': 22000, '2024-06': 18000, '2024-07': 15000, '2024-08': 14000,
             '2024-09': 16000, '2024-10': 18000, '2024-11': 20000, '2024-12': 25000},
    'C003': {'2024-01': 5000, '2024-02': 5500, '2024-03': 6000, '2024-04': 7000,
             '2024-05': 8000, '2024-06': 7500, '2024-07': 6000, '2024-08': 5500,
             '2024-09': 6000, '2024-10': 7000, '2024-11': 8000, '2024-12': 10000},
    'C004': {'2024-01': 2000, '2024-02': 2000, '2024-03': 2500, '2024-04': 2500,
             '2024-05': 3000, '2024-06': 2500, '2024-07': 2000, '2024-08': 2000,
             '2024-09': 2500, '2024-10': 2500, '2024-11': 3000, '2024-12': 3500},
    'C005': {'2024-01': 6000, '2024-02': 6500, '2024-03': 7000, '2024-04': 7500,
             '2024-05': 8000, '2024-06': 7000, '2024-07': 6000, '2024-08': 5500,
             '2024-09': 6000, '2024-10': 7000, '2024-11': 8000, '2024-12': 10000},
    'C006': {'2024-01': 7000, '2024-02': 7500, '2024-03': 8000, '2024-04': 8500,
             '2024-05': 9000, '2024-06': 8000, '2024-07': 7000, '2024-08': 6500,
             '2024-09': 7000, '2024-10': 8000, '2024-11': 9000, '2024-12': 11000},
}


class ChannelCostService:
    @staticmethod
    def _ensure_file():
        if not os.path.exists(CHANNEL_COST_FILE):
            os.makedirs(DATA_DIR, exist_ok=True)
            ChannelCostService._save_to_file(DEFAULT_COSTS)

    @staticmethod
    def _load_from_file() -> Dict[str, Dict[str, float]]:
        ChannelCostService._ensure_file()
        try:
            with open(CHANNEL_COST_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except (json.JSONDecodeError, FileNotFoundError):
            return DEFAULT_COSTS.copy()

    @staticmethod
    def _save_to_file(data: Dict[str, Dict[str, float]]):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(CHANNEL_COST_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def get_all_costs() -> Dict[str, Dict[str, float]]:
        return ChannelCostService._load_from_file()

    @staticmethod
    def get_channel_costs(channel_id: str) -> Dict[str, float]:
        all_costs = ChannelCostService._load_from_file()
        return all_costs.get(channel_id, {})

    @staticmethod
    def get_period_cost(channel_id: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> float:
        costs = ChannelCostService.get_channel_costs(channel_id)
        if not costs:
            return 0.0

        total = 0.0
        for month, cost in costs.items():
            if start_date and month < start_date[:7]:
                continue
            if end_date and month > end_date[:7]:
                continue
            total += float(cost)
        return total

    @staticmethod
    def set_channel_cost(channel_id: str, stat_month: str, cost: float) -> Dict[str, Dict[str, float]]:
        all_costs = ChannelCostService._load_from_file()
        if channel_id not in all_costs:
            all_costs[channel_id] = {}
        all_costs[channel_id][stat_month] = float(cost)
        ChannelCostService._save_to_file(all_costs)
        return all_costs

    @staticmethod
    def batch_set_costs(costs_data: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
        all_costs = ChannelCostService._load_from_file()
        for item in costs_data:
            channel_id = item.get('channelId') or item.get('channel_id')
            stat_month = item.get('statMonth') or item.get('stat_month')
            cost = item.get('cost') or item.get('channelCost') or 0
            if channel_id and stat_month:
                if channel_id not in all_costs:
                    all_costs[channel_id] = {}
                all_costs[channel_id][stat_month] = float(cost)
        ChannelCostService._save_to_file(all_costs)
        return all_costs

    @staticmethod
    def get_costs_by_period(start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, float]:
        all_costs = ChannelCostService._load_from_file()
        result = {}
        for channel_id, monthly_costs in all_costs.items():
            total = 0.0
            for month, cost in monthly_costs.items():
                if start_date and month < start_date[:7]:
                    continue
                if end_date and month > end_date[:7]:
                    continue
                total += float(cost)
            result[channel_id] = round(total, 2)
        return result
