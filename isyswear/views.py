from django.shortcuts import render
from products.models import Uniform


def home(request):
    """UNISSU institutional storefront home page."""
    featured_uniforms = Uniform.objects.all().order_by('-created_at')[:4]
    return render(request, 'pages/home.html', {
        'featured_uniforms': featured_uniforms
    })
