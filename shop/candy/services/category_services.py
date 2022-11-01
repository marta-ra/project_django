from candy.models import Category


class CategoryServices:
    @staticmethod
    def get_categories():
        return Category.objects.all()

    @staticmethod
    def get_category(category_id):
        return Category.objects.get(pk=category_id)
