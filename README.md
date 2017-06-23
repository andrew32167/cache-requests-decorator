# cache-requests-decorator
Decorator to cache python get requests
# Installation
Create new virtual environment clone repo there and install necessary packages
```
git clone git@github.com:andrew32167/cache-requests-decorator.git
pip install -r cache-requests-decorato/requirements.txt
```
# Usage
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cache_decorator import CacheDecorator
import requests
from datetime import datetime


@CacheDecorator
def get_request(url, **kwargs):
    return requests.get(url, **kwargs)

for t in range(2):
    start = datetime.now()
    resp = get_request('https://github.com/andrew32167/cache-requests-decorator')
    end = datetime.now()
    print(resp)
    print('Time spent: {}'.format(end - start))

```