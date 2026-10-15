from django.db import models


class Uniform(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Unisex', 'Unisex'),
    ]
    
    CATEGORY_CHOICES = [
    ('uniforms', 'Campus Uniforms'),
    ('department', 'Department Uniforms'),
    ('organization', 'Organization Uniforms'),
    ('bottoms', 'Slacks & Pants'),
    ('lanyards', 'Lanyards & IDs'),
    ]


    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.TextField(default='')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Unisex')
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        blank=True,
        default='',
    )
    color = models.CharField(max_length=100, blank=True)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='uniforms/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)  # ← new
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name


    def get_size_display(self):
        return "Multiple sizes available" if "\n" in self.size or "," in self.size else self.size


    def get_gender_display(self):
        return self.gender

    @property
    def display_image_url(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        fallback_map = {
            1: '/static/images/mdfem.jpg',
            2: '/static/images/mdmale.jpg',
            3: '/static/images/tdfem.jpg',
            4: '/static/images/tdmale.jpg',
            5: '/static/images/slacksF.jpg',
            6: '/static/images/slacksM.jpg',
            7: '/static/images/wed.jpg',
            8: '/static/images/thu.jpg',
            9: '/static/images/newlace.jpg',
            10: '/static/images/oldlace.jpg',
        }
        return fallback_map.get(self.id, '/static/images/thu.jpg')

    class Meta:
        ordering = ['-created_at']




class UniformSize(models.Model):
    SIZE_CHOICES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('XXXL', 'XXXL'),
        ('ONE_SIZE', 'One Size Fits All'),
    ]


    uniform = models.ForeignKey(Uniform, on_delete=models.CASCADE, related_name='sizes')
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    stock = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f"{self.uniform.name} - {self.size} ({self.stock} in stock)"


    class Meta:
        unique_together = ('uniform', 'size')
        ordering = ['size']
