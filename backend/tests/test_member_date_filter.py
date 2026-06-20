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

def test_churn_date_filter():
    print('=== CHURN DATE FILTER ===')
    params_all = {'storeIds': ALL_STORES, 'days': 60, 'limit': 1000, 'startDate': '2026-02-01', 'endDate': '2026-06-30'}
    params_mar = {'storeIds': ALL_STORES, 'days': 60, 'limit': 1000, 'startDate': '2026-03-01', 'endDate': '2026-03-31'}
    r_all = requests.get(BASE + '/api/v1/members/churn', params=params_all, timeout=10)
    r_mar = requests.get(BASE + '/api/v1/members/churn', params=params_mar, timeout=10)
    lst_all = r_all.json()['data']
    lst_mar = r_mar.json()['data']
    print(f"  all range churn count: {len(lst_all)}")
    print(f"  March only churn count: {len(lst_mar)}")
    if lst_all:
        dates_all = set(m['last_visit_date'][:7] for m in lst_all)
        print(f"  months in all range: {sorted(dates_all)}")
    if lst_mar:
        for m in lst_mar:
            assert m['last_visit_date'].startswith('2026-03'), f"should be March only, got {m['last_visit_date']}"
        print(f"  all March entries start with 2026-03: OK")
    assert len(lst_mar) <= len(lst_all), 'March subset should be <= all range'
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
