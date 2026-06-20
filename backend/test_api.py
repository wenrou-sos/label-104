import requests
import json

BASE_URL = 'http://127.0.0.1:5000/api/v1'

def test_endpoint(name, url):
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get('code') == 200:
            result_data = data.get('data')
            if isinstance(result_data, list):
                print(f'✅ {name}: 成功，返回 {len(result_data)} 条记录')
            elif isinstance(result_data, dict):
                print(f'✅ {name}: 成功，返回数据包含 {list(result_data.keys())}')
            else:
                print(f'✅ {name}: 成功')
            return True
        else:
            print(f'❌ {name}: 失败，code={data.get("code")}, message={data.get("message")}')
            return False
    except Exception as e:
        print(f'❌ {name}: 异常 - {str(e)}')
        return False

def main():
    print('=' * 60)
    print('美容连锁门店经营分析系统 - API 接口测试')
    print('=' * 60)
    
    tests = [
        ('健康检查', f'{BASE_URL}/health'),
        ('门店指标', f'{BASE_URL}/stores/metrics'),
        ('门店排名', f'{BASE_URL}/stores/ranking?sortBy=revenue&sortOrder=desc'),
        ('门店趋势', f'{BASE_URL}/stores/trend'),
        ('项目销售', f'{BASE_URL}/projects/sales'),
        ('项目毛利', f'{BASE_URL}/projects/margin'),
        ('项目矩阵', f'{BASE_URL}/projects/matrix'),
        ('员工排行', f'{BASE_URL}/employees/ranking'),
        ('员工客单', f'{BASE_URL}/employees/orders'),
        ('会员周期', f'{BASE_URL}/members/cycle'),
        ('会员复充', f'{BASE_URL}/members/recharge'),
        ('会员流失', f'{BASE_URL}/members/churn'),
        ('渠道转化', f'{BASE_URL}/channels/conversion'),
        ('渠道客单', f'{BASE_URL}/channels/aov'),
        ('渠道评估', f'{BASE_URL}/channels/evaluation'),
    ]
    
    results = []
    for name, url in tests:
        result = test_endpoint(name, url)
        results.append(result)
    
    print('=' * 60)
    passed = sum(results)
    total = len(results)
    print(f'测试结果: {passed}/{total} 通过')
    
    if passed == total:
        print('🎉 所有接口测试通过！')
    else:
        print(f'⚠️  有 {total - passed} 个接口测试失败')
    
    return passed == total

if __name__ == '__main__':
    main()
