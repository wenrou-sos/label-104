import json
import os
from typing import Any, Dict

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
WARNING_CONFIG_FILE = os.path.join(DATA_DIR, 'warning_config.json')

DEFAULT_WARNING_CONFIG: Dict[str, Any] = {
    'storeRevenueDropThreshold': 10.0,
    'memberChurnDaysThreshold': 60,
    'memberChurnHighRiskDays': 120,
    'memberChurnMediumRiskDays': 90,
}


class WarningService:
    @staticmethod
    def _ensure_config_file():
        if not os.path.exists(WARNING_CONFIG_FILE):
            os.makedirs(DATA_DIR, exist_ok=True)
            WarningService.save_config(DEFAULT_WARNING_CONFIG)

    @staticmethod
    def get_config() -> Dict[str, Any]:
        WarningService._ensure_config_file()
        try:
            with open(WARNING_CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
            merged = {**DEFAULT_WARNING_CONFIG, **config}
            return merged
        except (json.JSONDecodeError, FileNotFoundError):
            return DEFAULT_WARNING_CONFIG.copy()

    @staticmethod
    def save_config(config: Dict[str, Any]) -> Dict[str, Any]:
        os.makedirs(DATA_DIR, exist_ok=True)
        merged = {**DEFAULT_WARNING_CONFIG, **config}
        with open(WARNING_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(merged, f, ensure_ascii=False, indent=2)
        return merged

    @staticmethod
    def get_store_revenue_drop_threshold() -> float:
        config = WarningService.get_config()
        return float(config.get('storeRevenueDropThreshold', DEFAULT_WARNING_CONFIG['storeRevenueDropThreshold']))

    @staticmethod
    def get_member_churn_days_threshold() -> int:
        config = WarningService.get_config()
        return int(config.get('memberChurnDaysThreshold', DEFAULT_WARNING_CONFIG['memberChurnDaysThreshold']))

    @staticmethod
    def get_member_churn_levels() -> Dict[str, int]:
        config = WarningService.get_config()
        return {
            'high': int(config.get('memberChurnHighRiskDays', DEFAULT_WARNING_CONFIG['memberChurnHighRiskDays'])),
            'medium': int(config.get('memberChurnMediumRiskDays', DEFAULT_WARNING_CONFIG['memberChurnMediumRiskDays'])),
        }
