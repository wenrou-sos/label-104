import requests
import json

BASE_URL = 'http://127.0.0.1:5000/api/v1'

def print_sample(name, url, count=1):
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get('code') == 200:
            result = data.get('data')
            print(f'\n=== {name} ===')
            if isinstance(result, list):
                for item in result[:count]:
                    print(json.dumps(item, ensure_ascii=False, indent=2))
            elif isinstance(result, dict):
                print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f'{name} 错误: {data}')
    except Exception as e:
        print(f'{name} 异常: {str(e)}')

# 门店趋势
print_sample('门店趋势', f'{BASE_URL}/stores/trend', 1)

# 门店指标
print_sample('门店指标', f'{BASE_URL}/stores/metrics', 2)

# 项目销售
print_sample('项目销售', f'{BASE_URL}/projects/sales', 3)

# 项目毛利
print_sample('项目毛利', f'{BASE_URL}/projects/margin', 3)

# 项目矩阵
print_sample('项目矩阵', f'{BASE_URL}/projects/matrix')

# 员工排行
print_sample('员工排行', f'{BASE_URL}/employees/ranking', 3)

# 员工排行带筛选
print_sample('员工排行(皮肤管理)', f'{BASE_URL}/employees/ranking?serviceType=%E7%9A%AE%E8%82%A4%E7%AE%A1%E7%90%86', 3)
