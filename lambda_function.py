import datetime
import json
import uuid

def lambda_handler(event, context):
    try:
        doc = json.loads(event['body'])
    except (KeyError, json.JSONDecodeError):
        return {'error': 'Could not parse input as JSON'}
    norm = flatten_json(doc)
    out = add_metadata(norm)
    return out

def flatten_json(d, prefix=''):
    out = dict()
    for k,v in d.items():
        if isinstance(v, dict):
            out.update(flatten_json(v, prefix=f'{prefix}{k}_'))
        else:
            out[prefix + k] = v
    return out

def add_metadata(d):
    out = dict(d.items())
    out['_id'] = str(uuid.uuid4())
    out['_timestamp'] = datetime.datetime.now().isoformat()
    return out
