from lambda_function import flatten_json

def test_depth_one():
    d = {'a': 1, 'b': 2}
    flat = flatten_json(d)
    assert flat == d

def test_depth_two():
    d = {'a': {'b': 1}}
    flat = flatten_json(d)
    assert flat == {'a_b': 1}

def test_deep():
    d = {'a': {'b': {'c': {'d': 1}}}}
    flat = flatten_json(d)
    assert flat == {'a_b_c_d': 1}

def test_no_collision():
    d = {'a': {'b': 1}, 'b': 2}
    flat = flatten_json(d)
    assert flat == {'a_b': 1, 'b': 2}
