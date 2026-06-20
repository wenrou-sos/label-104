import requests

BASE = 'http://127.0.0.1:5000'
ALL_STORES = 'S001,S002,S003,S004,S005,S006,S007,S008'

def test_cycle_date_filter():
    print('=== CYCLE DATE FILTER ===')
    params_all = {'storeIds': ALL_STORES, 'startDate': '2024-01-01', 'endDate': '2026-12-31'}
    params_2024 = {'storeIds': ALL_STORES, 'startDate': '2024-01-01', 'endDate': '2024-12-31'}
    params_2025 = {'storeIds': ALL_STORES, 'startDate': '2025-01-01', 'endDate': '2025-12-31'}
    r_all = requests.get(BASE + '/api/v1/members/cycle', params=params_all, timeout=10)
    r_2024 = requests.get(BASE + '/api/v1/members/cycle', params=params_2024, timeout=10)
    r_2025 = requests.get(BASE + '/api/v1/members/cycle', params=params_2025, timeout=10)
    d_all = r_all.json()['data']
    d_2024 = r_2024.json()['data']
    d_2025 = r_2025.json()['data']
    print(f"  all:  total_members={d_all['total_members']}, avg_cycle={d_all['avg_recharge_cycle']}")
    print(f"  2024: total_members={d_2024['total_members']}, avg_cycle={d_2024['avg_recharge_cycle']}")
    print(f"  2025: total_members={d_2025['total_members']}, avg_cycle={d_2025['avg_recharge_cycle']}")
    assert d_all['total_members'] == 2210, f"all should be 2210, got {d_all['total_members']}"
    assert 0 < d_2024['total_members'] < d_all['total_members'], '2024 subset should exist and be smaller'
    assert 0 < d_2025['total_members'] < d_all['total_members'], '2025 subset should exist and be smaller'
    assert d_2024['total_members'] + d_2025['total_members'] <= d_all['total_members'], 'sums should not exceed total'
    print('  [OK] cycle date filter works')
    print()

def _unwrap_churn(resp_data):
    if isinstance(resp_data, dict) and 'list' in resp_data:
        return resp_data['list']
    return resp_data


def _unwrap_churn_total(resp_data):
    if isinstance(resp_data, dict) and 'total' in resp_data:
        return resp_data['total']
    return len(resp_data) if isinstance(resp_data, list) else 0


def test_churn_date_filter():
    print('=== CHURN DATE FILTER ===')
    params_all = {'storeIds': ALL_STORES, 'days': 60, 'limit': 1000, 'startDate': '2024-06-01', 'endDate': '2024-12-31'}
    params_q3 = {'storeIds': ALL_STORES, 'days': 60, 'limit': 1000, 'startDate': '2024-07-01', 'endDate': '2024-09-30'}
    r_all = requests.get(BASE + '/api/v1/members/churn', params=params_all, timeout=10)
    r_q3 = requests.get(BASE + '/api/v1/members/churn', params=params_q3, timeout=10)
    raw_all = r_all.json()['data']
    raw_q3 = r_q3.json()['data']
    lst_all = _unwrap_churn(raw_all)
    lst_q3 = _unwrap_churn(raw_q3)
    total_all = _unwrap_churn_total(raw_all)
    total_q3 = _unwrap_churn_total(raw_q3)
    print(f"  2024 H2 total churn: {total_all} (list {len(lst_all)})")
    print(f"  2024 Q3  total churn: {total_q3} (list {len(lst_q3)})")
    assert total_all > 0, '2024 H2 should have some churned members'
    assert total_q3 <= total_all, 'Q3 subset should be <= H2 total'
    print('  [OK] churn date filter works')
    print()

if __name__ == '__main__':
    try:
        test_cycle_date_filter()
        test_churn_date_filter()
        print('=== ALL MEMBER DATE FILTER TESTS PASSED ===')
    except Exception as e:
        print(f'!!! TEST FAILED: {e}')
        import traceback; traceback.print_exc()
        raise
