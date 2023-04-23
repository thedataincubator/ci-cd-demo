from lambda_function import add_metadata

def test_metadata_keys():
    d = {'a': 1}
    out = add_metadata(d)
    assert '_id' in out
    assert '_timestamp' in out

def test_metadata_unique():
    md1 = add_metadata({'a': 1})
    md2 = add_metadata({'b': 1})
    assert md1['_id'] != md2['_id']
    # Timestamps should have microsecond precision, so they will be different
    assert md1['_timestamp'] != md2['_timestamp']

def test_no_mutation():
    d = {'a': 1}
    add_metadata(d)
    assert '_id' not in d
    assert '_timestamp' not in d
