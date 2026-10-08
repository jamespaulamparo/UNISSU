import os
import sys
import django

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isyswear.settings')
django.setup()

from products.models import Uniform
from decimal import Decimal

# Create 5 sample uniforms if they don't exist
uniforms = [
    {
        'name': 'Classic White Shirt',
        'description': 'A crisp white dress shirt, perfect for business and formal occasions.',
        'price': Decimal('499.00'),
        'size': 'M',
        'gender': 'U',
        'color': 'White',
        'stock': 25,
    },
    {
        'name': 'Navy Blue Polo',
        'description': 'Premium navy polo shirt with embroidered logo space.',
        'price': Decimal('599.00'),
        'size': 'M',
        'gender': 'U',
        'color': 'Navy Blue',
        'stock': 30,
    },
    {
        'name': 'Black Blazer',
        'description': 'Professional black blazer for formal business wear.',
        'price': Decimal('1299.00'),
        'size': 'L',
        'gender': 'M',
        'color': 'Black',
        'stock': 15,
    },
    {
        'name': 'Gray Work Pants',
        'description': 'Comfortable gray work pants, perfect for office environments.',
        'price': Decimal('799.00'),
        'size': 'M',
        'gender': 'M',
        'color': 'Gray',
        'stock': 40,
    },
    {
        'name': 'Pink Blouse',
        'description': 'Elegant pink blouse for professional and casual settings.',
        'price': Decimal('649.00'),
        'size': 'S',
        'gender': 'F',
        'color': 'Pink',
        'stock': 20,
    },
]

for uniform_data in uniforms:
    uniform, created = Uniform.objects.get_or_create(
        name=uniform_data['name'],
        defaults=uniform_data
    )
    if created:
        print(f'Created: {uniform.name}')
    else:
        print(f'Already exists: {uniform.name}')

print('Sample uniforms loaded successfully!')
