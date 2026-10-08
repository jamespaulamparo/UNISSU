from django.shortcuts import render, get_object_or_404
from .models import Uniform, UniformSize


def home(request):
    """Institutional landing page featured items."""
    featured = Uniform.objects.all().order_by('-created_at')[:4]
    return render(request, 'pages/home.html', {'featured_uniforms': featured})


def uniforms(request):
    """Catalog view with filter and search capability."""
    selected_size = request.GET.get('size', '').strip()
    selected_gender = request.GET.get('gender', '').strip()
    search_query = request.GET.get('q', '').strip()

    qs = Uniform.objects.all()

    if search_query:
        qs = qs.filter(name__icontains=search_query)

    if selected_gender:
        qs = qs.filter(gender__iexact=selected_gender)

    if selected_size:
        qs = qs.filter(sizes__size=selected_size).distinct()

    sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL', 'ONE_SIZE']
    gender_choices = Uniform.GENDER_CHOICES

    context = {
        'uniforms': qs,
        'sizes': sizes,
        'GENDER_CHOICES': gender_choices,
        'selected_size': selected_size,
        'selected_gender': selected_gender,
        'search_query': search_query,
    }
    return render(request, 'pages/uniforms.html', context)


def uniform_detail(request, pk):
    """Product detail page."""
    uniform = get_object_or_404(Uniform, pk=pk)
    available_sizes = uniform.sizes.all()
    return render(request, 'pages/uniformDetails.html', {
        'uniform': uniform,
        'available_sizes': available_sizes,
    })
