import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

class CsvLoader:
    _cache = {}
    
    @classmethod
    def load_csv(cls, filename):
        if filename in cls._cache:
            return cls._cache[filename]
        
        filepath = os.path.join(DATA_DIR, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f'CSV file not found: {filepath}')
        
        df = pd.read_csv(filepath)
        cls._cache[filename] = df
        return df
    
    @classmethod
    def reload(cls, filename=None):
        if filename:
            if filename in cls._cache:
                del cls._cache[filename]
        else:
            cls._cache.clear()
    
    @classmethod
    def get_stores(cls):
        return cls.load_csv('stores.csv')
    
    @classmethod
    def get_store_metrics(cls):
        return cls.load_csv('store_metrics.csv')
    
    @classmethod
    def get_projects(cls):
        return cls.load_csv('projects.csv')
    
    @classmethod
    def get_project_sales(cls):
        return cls.load_csv('project_sales.csv')
    
    @classmethod
    def get_employees(cls):
        return cls.load_csv('employees.csv')
    
    @classmethod
    def get_employee_performance(cls):
        return cls.load_csv('employee_performance.csv')
    
    @classmethod
    def get_members(cls):
        return cls.load_csv('members.csv')
    
    @classmethod
    def get_channels(cls):
        return cls.load_csv('channels.csv')
    
    @classmethod
    def get_channel_data(cls):
        return cls.load_csv('channel_data.csv')
