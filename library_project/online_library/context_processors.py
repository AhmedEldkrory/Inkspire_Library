from .models import Category

def categories_processor(request):
    """
    Context processor that adds all categories to the context
    """
    return {
        'categories': Category.objects.all()
    }
