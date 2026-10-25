import MasterMind

test_cases = [
    {'c1': [1,1,1,1], 'c2': [1,1,1,1], 'dist': [2,2,2,2]},
    {'c1': [1,1,1,1], 'c2': [1,1,1,2], 'dist': [2,2,2]},
    {'c1': [1,1,1,1], 'c2': [1,1,3,2], 'dist': [2,2]},
    {'c1': [1,1,1,1], 'c2': [2,1,3,4], 'dist': [2]},
    {'c1': [1,2,3,4], 'c2': [4,3,2,1], 'dist': [1,1,1,1]},
    {'c1': [1,1,2,2], 'c2': [2,2,1,1], 'dist': [1,1,1,1]},
    {'c1': [1,1,2,3], 'c2': [2,2,1,1], 'dist': [1,1,1]},
    {'c1': [1,3,6,2], 'c2': [1,1,2,2], 'dist': [2,2]}
]

def test():
    for case in test_cases:
        dist = MasterMind.calc_distance(case['c1'], case['c2'])
        if dist == case['dist']:
            print(case, 'PASS')
        else:
            print(case, 'FAIL', 'expected', case['dist'], 'got', dist)
        print('distance evaluation', MasterMind.evaluate_distance(dist))

test()
