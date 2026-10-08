from django.core.management.base import BaseCommand
from products.models import Uniform, UniformSize


class Command(BaseCommand):
    help = 'Seed real uniform data'


    def handle(self, *args, **kwargs):
        Uniform.objects.all().delete()  # also deletes UniformSize via CASCADE
        
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE products_uniform AUTO_INCREMENT = 1")
        
        self.stdout.write(self.style.WARNING('Reset auto-increment to 1'))


        image_mappings = {
            1: '/static/images/mdfem.jpg',
            2: '/static/images/mdmale.jpg', 
            3: '/static/images/tdfem.jpg',
            4: '/static/images/tdmale.jpg',
            5: '/static/images/slacksF.jpg',
            6: '/static/images/slacksM.jpg',
            7: '/static/images/wed.jpg',
            8: '/static/images/thu.jpg',
            9: '/static/images/newlace.jpg',
        }

        uniforms = [
            dict(name="DMMMSU Uniform Top", gender="Female", color="Type A", price=450.00, stock=25,
                 size='XS: Bust 30-32", Waist 24-26"\nS: Bust 32-34", Waist 26-28"\nM: Bust 34-36", Waist 28-30"\nL: Bust 36-39", Waist 30-33"\nXL: Bust 39-42", Waist 33-36"\nXXL: Bust 42-45", Waist 36-39"\nXXXL: Bust 45-48", Waist 39-42"',
                 description="Official DMMMSU uniform top for female students.",
                 sizes={'XS': 4, 'S': 4, 'M': 4, 'L': 4, 'XL': 3, 'XXL': 3, 'XXXL': 3}),
            dict(name="DMMMSU Uniform Top", gender="Male", color="Type A", price=450.00, stock=20,
                 size='XS: Chest 34-36", Waist 28-30"\nS: Chest 36-38", Waist 30-32"\nM: Chest 38-40", Waist 32-34"\nL: Chest 40-43", Waist 34-36"\nXL: Chest 43-46", Waist 36-39"\nXXL: Chest 46-49", Waist 39-42"\nXXXL: Chest 49-52", Waist 42-45"',
                 description="Official DMMMSU uniform top for male students.",
                 sizes={'XS': 3, 'S': 3, 'M': 3, 'L': 3, 'XL': 3, 'XXL': 3, 'XXXL': 2}),
            dict(name="CIS Tuesday Uniform", gender="Female", color="Type A", price=650.00, stock=15,
                 size='XS: Bust 32-34", Waist 25-27"\nS: Bust 34-36", Waist 27-29"\nM: Bust 36-38", Waist 29-31"\nL: Bust 38-41", Waist 31-34"\nXL: Bust 41-44", Waist 34-37"\nXXL: Bust 44-47", Waist 37-40"\nXXXL: Bust 47-50", Waist 40-43"',
                 description="CIS Tuesday uniform for female students.",
                 sizes={'XS': 2, 'S': 2, 'M': 3, 'L': 3, 'XL': 2, 'XXL': 2, 'XXXL': 1}),
            dict(name="CIS Tuesday Uniform", gender="Male", color="Type A", price=650.00, stock=15,
                 size='XS: Chest 34-36", Waist 28-30"\nS: Chest 36-38", Waist 30-32"\nM: Chest 38-40", Waist 32-34"\nL: Chest 40-43", Waist 34-36"\nXL: Chest 43-46", Waist 36-39"\nXXL: Chest 46-49", Waist 39-42"\nXXXL: Chest 49-52", Waist 42-45"',
                 description="CIS Tuesday uniform for male students.",
                 sizes={'XS': 2, 'S': 2, 'M': 3, 'L': 3, 'XL': 2, 'XXL': 2, 'XXXL': 1}),
            dict(name="CIS Uniform Bottom", gender="Female", color="Slacks", price=450.00, stock=22,
                 size='XS: Waist 24-26", Hips 32-34"\nS: Waist 26-28", Hips 34-36"\nM: Waist 28-30", Hips 36-38"\nL: Waist 30-33", Hips 38-41"\nXL: Waist 33-36", Hips 41-44"\nXXL: Waist 36-39", Hips 44-47"\nXXXL: Waist 39-42", Hips 47-50"',
                 description="Official CIS bottom uniform for female students.",
                 sizes={'XS': 3, 'S': 3, 'M': 4, 'L': 4, 'XL': 3, 'XXL': 3, 'XXXL': 2}),
            dict(name="CIS Uniform Bottom", gender="Male", color="Slacks", price=450.00, stock=18,
                 size='XS: Waist 26-28", Hips 34-36"\nS: Waist 28-30", Hips 36-38"\nM: Waist 30-32", Hips 38-40"\nL: Waist 32-35", Hips 40-43"\nXL: Waist 35-38", Hips 43-46"\nXXL: Waist 38-41", Hips 46-49"\nXXXL: Waist 41-44", Hips 49-52"',
                 description="Official CIS bottom uniform for male students.",
                 sizes={'XS': 2, 'S': 3, 'M': 3, 'L': 3, 'XL': 3, 'XXL': 2, 'XXXL': 2}),
            dict(name="CIS Wednesday Uniform", gender="Unisex", color="Polo", price=450.00, stock=20,
                 size="XSmall, Small, Medium, Large, XL, XXL, XXXL",
                 description="CIS Wednesday uniform.",
                 sizes={'XS': 3, 'S': 3, 'M': 3, 'L': 3, 'XL': 3, 'XXL': 3, 'XXXL': 2}),
            dict(name="CIS Thursday Uniform", gender="Unisex", color="Polo", price=450.00, stock=20,
                 size="XSmall, Small, Medium, Large, XL, XXL, XXXL",
                 description="CIS Thursday uniform.",
                 sizes={'XS': 3, 'S': 3, 'M': 3, 'L': 3, 'XL': 3, 'XXL': 3, 'XXXL': 2}),
            dict(name="DMMMSU Lanyard", gender="Unisex", color="ID Lace", price=65.00, stock=100,
                 size="One Size Fits All",
                 description="DMMMSU official and latest lanyard.",
                 sizes={'ONE_SIZE': 100}),
        ]


        for data in uniforms:
            sizes = data.pop('sizes')
            uniform = Uniform.objects.create(**data)
            # Set image_url based on auto ID
            if uniform.id in image_mappings:
                uniform.image_url = image_mappings[uniform.id]
                uniform.save()
            for size_code, stock in sizes.items():
                UniformSize.objects.create(uniform=uniform, size=size_code, stock=stock)


        self.stdout.write(self.style.SUCCESS(f'Seeded {len(uniforms)} uniforms with sizes.'))
