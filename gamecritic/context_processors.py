from blog.models import Genre


def global_context(request):
    """
    Global context processor to make commonly used data available in all templates
    """
    return {
        'genres': Genre.objects.all().order_by('name'),
    }
