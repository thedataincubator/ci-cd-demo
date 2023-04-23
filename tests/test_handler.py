import json
import pytest
from unittest.mock import patch

import lambda_function
    
def test_no_body():
    json_in = dict()
    res = lambda_function.lambda_handler(json_in, None)
    assert 'error' in res

def test_no_body():
    json_in = {'body': '}Invalid JSON{'}
    res = lambda_function.lambda_handler(json_in, None)
    assert 'error' in res

@patch('lambda_function.add_metadata')
@patch('lambda_function.flatten_json')
def test_handler_calls(mock_flatten_json, mock_add_metadata):
    json_in = {'body': '{"a": 1}'}
    lambda_function.lambda_handler(json_in, None)
    assert mock_flatten_json.called
    assert mock_add_metadata.called

@pytest.mark.integration
def test_handler():
    json_in = {'body': json.dumps({'a': {'b': 1}})}
    res = lambda_function.lambda_handler(json_in, None)
    assert res['a_b'] == 1
    assert '_id' in res
    assert '_timestamp' in res
