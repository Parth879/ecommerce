from category.models import Category


def menu_link(request):
    link = Category.objects.all()
    return dict({'links':link})