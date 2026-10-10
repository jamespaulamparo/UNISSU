from django.shortcuts import render, get_object_or_404
from .models import Uniform, UniformSize


def home(request):
    """Institutional landing page featured items."""
    featured = Uniform.objects.all().order_by('-created_at')[:4]
    return render(request, 'pages/home.html', {'featured_uniforms': featured})



def uniforms(request):
    """Catalog view with category, gender, size, and search filters."""
    selected_category = request.GET.get('category', '').strip()
    selected_genders = request.GET.getlist('gender')
    selected_size = request.GET.get('size', '').strip()
    search_query = request.GET.get('q', '').strip()

    # Start with the complete catalog.
    qs = Uniform.objects.all()

    # Search by product name.
    if search_query:
        qs = qs.filter(name__icontains=search_query)

    # Filter by category.
    valid_categories = {
        value for value, label in Uniform.CATEGORY_CHOICES
    }

    if selected_category in valid_categories:
        qs = qs.filter(category=selected_category)

    # Filter by one or more genders.
    valid_genders = {
        value for value, label in Uniform.GENDER_CHOICES
    }

    selected_genders = [
        gender for gender in selected_genders
        if gender in valid_genders
    ]

    if selected_genders:
        qs = qs.filter(gender__in=selected_genders)

    # Filter by available size.
    valid_sizes = {
        value for value, label in UniformSize.SIZE_CHOICES
    }

    if selected_size in valid_sizes:
        qs = qs.filter(
            sizes__size=selected_size
        ).distinct()

    context = {
        'uniforms': qs,
        'sizes': [value for value, label in UniformSize.SIZE_CHOICES],
        'GENDER_CHOICES': Uniform.GENDER_CHOICES,
        'CATEGORY_CHOICES': Uniform.CATEGORY_CHOICES,
        'selected_category': selected_category,
        'selected_genders': selected_genders,
        'selected_size': selected_size,
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
