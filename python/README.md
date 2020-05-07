
/Volumes/Data/proxy/env/lib/python3.7/site-packages/urllib3/connectionpool.py:986: InsecureRequestWarning: Unverified HTTPS request is being made to host 'example.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
  InsecureRequestWarning,

1. 
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

2.
https://certifi.io/en/latest/
download https://mkcert.org/generate/
