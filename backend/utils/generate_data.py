import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def generate_stores():
    stores = [
        {'store_id': 'S001', 'store_name': '朝阳旗舰店', 'city': '北京', 'area': '朝阳区', 'open_date': '2022-03-15'},
        {'store_id': 'S002', 'store_name': '海淀精品店', 'city': '北京', 'area': '海淀区', 'open_date': '2022-06-20'},
        {'store_id': 'S003', 'store_name': '浦东中心店', 'city': '上海', 'area': '浦东新区', 'open_date': '2021-11-08'},
        {'store_id': 'S004', 'store_name': '徐汇形象店', 'city': '上海', 'area': '徐汇区', 'open_date': '2023-01-10'},
        {'store_id': 'S005', 'store_name': '天河总店', 'city': '广州', 'area': '天河区', 'open_date': '2022-08-25'},
        {'store_id': 'S006', 'store_name': '南山概念店', 'city': '深圳', 'area': '南山区', 'open_date': '2023-04-18'},
        {'store_id': 'S007', 'store_name': '武林广场店', 'city': '杭州', 'area': '下城区', 'open_date': '2022-12-01'},
        {'store_id': 'S008', 'store_name': '春熙路店', 'city': '成都', 'area': '锦江区', 'open_date': '2023-07-22'},
    ]
    df = pd.DataFrame(stores)
    df.to_csv(os.path.join(DATA_DIR, 'stores.csv'), index=False)
    print(f'Generated stores.csv: {len(df)} records')
    return stores

def generate_store_metrics(stores):
    months = pd.date_range(start='2024-01-01', end='2024-12-01', freq='MS').strftime('%Y-%m').tolist()
    
    base_revenue = {
        'S001': 850000, 'S002': 680000, 'S003': 920000, 'S004': 550000,
        'S005': 780000, 'S006': 620000, 'S007': 590000, 'S008': 480000
    }
    
    records = []
    for store in stores:
        store_id = store['store_id']
        base = base_revenue.get(store_id, 600000)
        for i, month in enumerate(months):
            seasonal_factor = 1 + 0.15 * np.sin(i * np.pi / 6)
            random_factor = 0.9 + 0.2 * np.random.random()
            
            revenue = base * seasonal_factor * random_factor
            customer_price = 380 + 50 * np.random.random() + 20 * seasonal_factor
            visit_frequency = 2.8 + 0.8 * np.random.random() + 0.3 * seasonal_factor
            new_customers = int(45 + 25 * np.random.random() + 15 * seasonal_factor)
            repeat_rate = 0.62 + 0.15 * np.random.random()
            
            records.append({
                'store_id': store_id,
                'stat_month': month,
                'revenue': round(revenue, 2),
                'customer_price': round(customer_price, 2),
                'visit_frequency': round(visit_frequency, 2),
                'new_customers': new_customers,
                'repeat_rate': round(repeat_rate, 4)
            })
    
    df = pd.DataFrame(records)
    df.to_csv(os.path.join(DATA_DIR, 'store_metrics.csv'), index=False)
    print(f'Generated store_metrics.csv: {len(df)} records')

def generate_projects():
    projects = [
        {'project_id': 'P001', 'project_name': '面部清洁护理', 'category': '皮肤管理', 'price': 298, 'cost': 85},
        {'project_id': 'P002', 'project_name': '光子嫩肤', 'category': '皮肤管理', 'price': 1280, 'cost': 320},
        {'project_id': 'P003', 'project_name': '水光针', 'category': '皮肤管理', 'price': 1680, 'cost': 450},
        {'project_id': 'P004', 'project_name': '热玛吉', 'category': '抗衰紧致', 'price': 8800, 'cost': 2800},
        {'project_id': 'P005', 'project_name': '冰点脱毛', 'category': '脱毛', 'price': 580, 'cost': 120},
        {'project_id': 'P006', 'project_name': '半永久纹眉', 'category': '纹绣', 'price': 2680, 'cost': 580},
        {'project_id': 'P007', 'project_name': '美甲', 'category': '美甲美睫', 'price': 268, 'cost': 65},
        {'project_id': 'P008', 'project_name': '美睫嫁接', 'category': '美甲美睫', 'price': 388, 'cost': 95},
        {'project_id': 'P009', 'project_name': '祛痘护理', 'category': '皮肤管理', 'price': 498, 'cost': 135},
        {'project_id': 'P010', 'project_name': '玻尿酸填充', 'category': '抗衰紧致', 'price': 3800, 'cost': 1600},
    ]
    df = pd.DataFrame(projects)
    df.to_csv(os.path.join(DATA_DIR, 'projects.csv'), index=False)
    print(f'Generated projects.csv: {len(df)} records')
    return projects

def generate_project_sales(stores, projects):
    months = pd.date_range(start='2024-01-01', end='2024-12-01', freq='MS').strftime('%Y-%m').tolist()
    
    popularity = {
        'P001': 1.5, 'P002': 1.2, 'P003': 1.0, 'P004': 0.3, 'P005': 1.8,
        'P006': 0.6, 'P007': 2.0, 'P008': 1.6, 'P009': 0.9, 'P010': 0.4
    }
    
    records = []
    for store in stores:
        store_id = store['store_id']
        store_factor = 0.7 + 0.6 * np.random.random()
        for project in projects:
            project_id = project['project_id']
            price = project['price']
            pop_factor = popularity.get(project_id, 1.0)
            for i, month in enumerate(months):
                seasonal = 1 + 0.2 * np.sin(i * np.pi / 6 + np.random.random())
                base_count = int(20 * pop_factor * store_factor * seasonal)
                sales_count = max(5, base_count + np.random.randint(-8, 8))
                sales_amount = sales_count * price * (0.95 + 0.1 * np.random.random())
                
                records.append({
                    'store_id': store_id,
                    'project_id': project_id,
                    'stat_month': month,
                    'sales_count': sales_count,
                    'sales_amount': round(sales_amount, 2)
                })
    
    df = pd.DataFrame(records)
    df.to_csv(os.path.join(DATA_DIR, 'project_sales.csv'), index=False)
    print(f'Generated project_sales.csv: {len(df)} records')

def generate_employees(stores):
    positions = ['高级美容师', '美容师', '美甲师', '纹绣师', '店长']
    service_types = ['皮肤管理', '抗衰紧致', '脱毛', '纹绣', '美甲美睫']
    
    first_names = ['张', '李', '王', '刘', '陈', '杨', '黄', '周', '吴', '赵', '孙', '马', '朱', '胡', '林']
    last_names = ['美丽', '雅', '芳', '娜', '敏', '静', '丽', '莉', '婷', '雨', '欣', '语', '佳', '怡', '萱']
    
    emp_id = 1
    employees = []
    
    for store in stores:
        store_id = store['store_id']
        num_employees = np.random.randint(6, 10)
        for i in range(num_employees):
            fn = np.random.choice(first_names)
            ln = np.random.choice(last_names)
            position = np.random.choice(positions)
            service_type = np.random.choice(service_types)
            
            employees.append({
                'emp_id': f'E{emp_id:03d}',
                'emp_name': fn + ln,
                'store_id': store_id,
                'position': position,
                'service_type': service_type
            })
            emp_id += 1
    
    df = pd.DataFrame(employees)
    df.to_csv(os.path.join(DATA_DIR, 'employees.csv'), index=False)
    print(f'Generated employees.csv: {len(df)} records')
    return employees

def generate_employee_performance(employees, stores):
    months = pd.date_range(start='2024-01-01', end='2024-12-01', freq='MS').strftime('%Y-%m').tolist()
    
    records = []
    for emp in employees:
        emp_id = emp['emp_id']
        store_id = emp['store_id']
        base_card = 30000 + 25000 * np.random.random()
        base_orders = 60 + 40 * np.random.random()
        
        for i, month in enumerate(months):
            seasonal = 1 + 0.15 * np.sin(i * np.pi / 6)
            random_factor = 0.85 + 0.3 * np.random.random()
            
            card_amount = base_card * seasonal * random_factor
            order_count = int(base_orders * seasonal * (0.9 + 0.2 * np.random.random()))
            avg_price = card_amount / max(order_count, 1)
            
            records.append({
                'emp_id': emp_id,
                'store_id': store_id,
                'stat_month': month,
                'card_amount': round(card_amount, 2),
                'order_count': order_count,
                'avg_price': round(avg_price, 2)
            })
    
    df = pd.DataFrame(records)
    df.to_csv(os.path.join(DATA_DIR, 'employee_performance.csv'), index=False)
    print(f'Generated employee_performance.csv: {len(df)} records')

def generate_members(stores):
    records = []
    member_id = 1
    
    for store in stores:
        store_id = store['store_id']
        num_members = np.random.randint(200, 350)
        
        for i in range(num_members):
            register_days_ago = np.random.randint(30, 730)
            register_date = (datetime.now() - timedelta(days=register_days_ago)).strftime('%Y-%m-%d')
            
            last_visit_days_ago = np.random.randint(0, 120)
            last_visit_date = (datetime.now() - timedelta(days=last_visit_days_ago)).strftime('%Y-%m-%d')
            
            total_recharge = round(3000 + 15000 * np.random.random(), 2)
            total_visits = np.random.randint(2, 80)
            recharge_cycle_days = np.random.randint(45, 180)
            recharged_in_90d = 1 if np.random.random() > 0.4 else 0
            
            records.append({
                'member_id': f'M{member_id:05d}',
                'store_id': store_id,
                'register_date': register_date,
                'total_recharge': total_recharge,
                'last_visit_date': last_visit_date,
                'total_visits': total_visits,
                'recharge_cycle_days': recharge_cycle_days,
                'recharged_in_90d': recharged_in_90d
            })
            member_id += 1
    
    df = pd.DataFrame(records)
    df.to_csv(os.path.join(DATA_DIR, 'members.csv'), index=False)
    print(f'Generated members.csv: {len(df)} records')

def generate_channels():
    channels = [
        {'channel_id': 'C001', 'channel_name': '美团', 'channel_type': '本地生活'},
        {'channel_id': 'C002', 'channel_name': '抖音', 'channel_type': '短视频'},
        {'channel_id': 'C003', 'channel_name': '小红书', 'channel_type': '社交种草'},
        {'channel_id': 'C004', 'channel_name': '老客推荐', 'channel_type': '口碑传播'},
        {'channel_id': 'C005', 'channel_name': '微信朋友圈', 'channel_type': '社交媒体'},
        {'channel_id': 'C006', 'channel_name': '大众点评', 'channel_type': '本地生活'},
    ]
    df = pd.DataFrame(channels)
    df.to_csv(os.path.join(DATA_DIR, 'channels.csv'), index=False)
    print(f'Generated channels.csv: {len(df)} records')
    return channels

def generate_channel_data(stores, channels):
    months = pd.date_range(start='2024-01-01', end='2024-12-01', freq='MS').strftime('%Y-%m').tolist()
    
    channel_performance = {
        'C001': {'exposure': 8000, 'conv_rate': 0.035, 'aov': 420},
        'C002': {'exposure': 15000, 'conv_rate': 0.02, 'aov': 380},
        'C003': {'exposure': 6000, 'conv_rate': 0.045, 'aov': 520},
        'C004': {'exposure': 500, 'conv_rate': 0.25, 'aov': 680},
        'C005': {'exposure': 4000, 'conv_rate': 0.025, 'aov': 360},
        'C006': {'exposure': 5000, 'conv_rate': 0.04, 'aov': 450},
    }
    
    records = []
    for store in stores:
        store_id = store['store_id']
        store_factor = 0.7 + 0.5 * np.random.random()
        for channel in channels:
            channel_id = channel['channel_id']
            perf = channel_performance.get(channel_id, {'exposure': 3000, 'conv_rate': 0.03, 'aov': 400})
            for i, month in enumerate(months):
                seasonal = 1 + 0.2 * np.sin(i * np.pi / 6)
                
                exposure = int(perf['exposure'] * store_factor * seasonal * (0.9 + 0.2 * np.random.random()))
                click_rate = 0.1 + 0.05 * np.random.random()
                click_count = int(exposure * click_rate)
                arrival_count = int(click_count * perf['conv_rate'] * (0.9 + 0.2 * np.random.random()))
                avg_price = perf['aov'] * (0.9 + 0.2 * np.random.random())
                
                records.append({
                    'store_id': store_id,
                    'channel_id': channel_id,
                    'stat_month': month,
                    'exposure_count': exposure,
                    'click_count': click_count,
                    'arrival_count': arrival_count,
                    'avg_price': round(avg_price, 2)
                })
    
    df = pd.DataFrame(records)
    df.to_csv(os.path.join(DATA_DIR, 'channel_data.csv'), index=False)
    print(f'Generated channel_data.csv: {len(df)} records')

def main():
    ensure_data_dir()
    
    np.random.seed(42)
    
    print('Generating mock data...')
    stores = generate_stores()
    generate_store_metrics(stores)
    projects = generate_projects()
    generate_project_sales(stores, projects)
    employees = generate_employees(stores)
    generate_employee_performance(employees, stores)
    generate_members(stores)
    channels = generate_channels()
    generate_channel_data(stores, channels)
    
    print('All data generated successfully!')

if __name__ == '__main__':
    main()
