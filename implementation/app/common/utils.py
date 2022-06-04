from typing import Union
import json
from hashlib import md5

def get_ETag(elem: Union[dict, list[dict]]):
  json_encoded = json.dumps(elem, sort_keys=True).encode('utf-8')

  return md5(json_encoded).hexdigest()