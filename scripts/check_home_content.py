import requests

base = 'http://127.0.0.1:8000'
s = requests.Session()

print('Checking home page for sample uniforms...')
r = s.get(base + '/')
print('Status', r.status_code)
print('--- page snippet ---')
print(r.text[:1000])
print('--- end snippet ---')
for name in ['Classic White Shirt','Navy Polo','Pink Blouse','Gray Trousers','Black Cap']:
    print(name, 'found' , (name in r.text))
