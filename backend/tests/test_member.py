import requests
import json

BASE = 'http://127.0.0.1:5000'
params = {
    'startDate': '2024-01-01',
    'endDate': '2024-06-30',
    'storeIds': 'S001,S002,S003,S004,S005,S006,S007,S008',
}

def test_cycle():
    r = requests.get(BASE + '/api/v1/members/cycle', params=params, timeout=10)
    print('=== CYCLE ===')
    print('STATUS:', r.status_code)
    data = r.json()
    print('data keys:', list(data.get('data', {}).keys()))
    d = data.get('data', {})
    for k in ['avg_recharge_cycle', 'recharge_rate', 'total_members', 'active_members']:
        v = d.get(k)
        print(f'  {k} = {v} (type={type(v).__name__})')
    assert isinstance(d.get('avg_recharge_cycle'), (int, float)), 'avg_recharge_cycle missing'
    assert isinstance(d.get('recharge_rate'), (int, float)), 'recharge_rate missing'
    assert isinstance(d.get('total_members'), int), 'total_members missing'
    assert isinstance(d.get('active_members'), int), 'active_members missing'
    print('  [OK] cycle KPI structure correct')
    print()

def test_churn():
    r = requests.get(BASE + '/api/v1/members/churn', params={**params, 'days': 60, 'limit': 10}, timeout=10)
    print('=== CHURN (days=60, limit=10) ===')
    print('STATUS:', r.status_code)
    data = r.json()
    lst = data.get('data', [])
    print('  count:', len(lst))
    assert isinstance(lst, list), 'churn data should be list'
    if lst:
        sample = lst[0]
        print('  sample keys:', list(sample.keys()))
        for k in ['member_id', 'member_name', 'store_name', 'last_visit_date', 'days_since_last_visit', 'total_recharge', 'total_visits', 'level']:
            v = sample.get(k)
            print(f'    {k} = {v!r}')
        assert 'member_id' in sample and sample['member_id'], 'member_id missing'
        assert 'member_name' in sample and sample['member_name'], 'member_name missing'
        assert sample['level'] in ('high', 'medium', 'low'), f"invalid level: {sample['level']}"
        assert sample['days_since_last_visit'] >= 60, 'days should be >= 60'
    print('  [OK] churn list structure correct')
    print()

def test_churn_filter_days():
    r_60 = requests.get(BASE + '/api/v1/members/churn', params={**params, 'days': 60, 'limit': 500}, timeout=10)
    lst_60 = r_60.json().get('data', [])
    r_90 = requests.get(BASE + '/api/v1/members/churn', params={**params, 'days': 90, 'limit': 500}, timeout=10)
    lst_90 = r_90.json().get('data', [])
    print('=== CHURN FILTER (days=60 vs days=90) ===')
    print(f'  days=60 count: {len(lst_60)}, days=90 count: {len(lst_90)}')
    assert len(lst_60) > len(lst_90) > 0, 'days=60 should have more members than days=90'
    min_60 = min(m['days_since_last_visit'] for m in lst_60)
    min_90 = min(m['days_since_last_visit'] for m in lst_90)
    assert min_60 >= 60, f'days=60 min {min_60} should be >= 60'
    assert min_90 >= 90, f'days=90 min {min_90} should be >= 90'
    levels_60 = set(m['level'] for m in lst_60)
    levels_90 = set(m['level'] for m in lst_90)
    print(f'  days=60 levels: {levels_60}, days=90 levels: {levels_90}')
    assert 'low' in levels_60, 'days=60 should include low-risk members'
    assert 'low' not in levels_90, 'days=90 should NOT include low-risk members'
    print('  [OK] churn days filter + level logic correct')
    print()

def test_member_name_consistent():
    r = requests.get(BASE + '/api/v1/members/churn', params={**params, 'days': 60, 'limit': 50}, timeout=10)
    lst1 = r.json().get('data', [])
    r2 = requests.get(BASE + '/api/v1/members/churn', params={**params, 'days': 60, 'limit': 50}, timeout=10)
    lst2 = r2.json().get('data', [])
    print('=== NAME CONSISTENCY ===')
    if lst1 and lst2:
        names1 = {m['member_id']: m['member_name'] for m in lst1}
        names2 = {m['member_id']: m['member_name'] for m in lst2}
        for mid in names1:
            if mid in names2:
                assert names1[mid] == names2[mid], f'name mismatch for {mid}'
        print(f'  checked {len(names1)} members, all consistent')
    print('  [OK] name generation is deterministic')
    print()

if __name__ == '__main__':
    try:
        test_cycle()
        test_churn()
        test_churn_filter_days()
        test_member_name_consistent()
        print('=== ALL TESTS PASSED ===')
    except Exception as e:
        print(f'!!! TEST FAILED: {e}')
        raise
