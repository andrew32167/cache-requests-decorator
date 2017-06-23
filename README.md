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
from cache_decorator import CacheDecorator
import requests
from datetime import datetime
import time


@CacheDecorator
def delayed_get_request(url, **kwargs):
    time.sleep(10)
    return requests.get(url, **kwargs)

for t in range(2):
    start = datetime.now()
    resp = delayed_get_request('https://github.com/andrew32167/cache-requests-decorator')
    end = datetime.now()
    print(resp)
    print('Time spent: {}'.format(end - start))

```