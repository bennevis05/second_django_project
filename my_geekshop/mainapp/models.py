from django.db import models

class ProductCategory(models.Model):
    title = models.CharField(verbose_name='Название категории', max_length=50, unique=True)
    image = models.ImageField(upload_to='categories_images', blank=True)
    description = models.TextField(verbose_name='Описание категории', blank=True)
    is_active = models.BooleanField(verbose_name="Категория активна", default=True)

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Название товара', max_length=100, unique=True)
    product_image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField(verbose_name='Краткое описание товара', max_length=100, blank=True)
    detailed_desc = models.TextField(verbose_name='Подробное описание товара', blank=True)
    appearance = models.TextField(verbose_name='Описание внешнего вида товара', blank=True)
    specifications = models.TextField(verbose_name='Характеристики товара')
    price = models.DecimalField(verbose_name='Стоимость товара', max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='Количество товара в наличии', default=0)
    is_active = models.BooleanField(verbose_name="Товар активен", default=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.name} ({self.category.title})'

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by("category", "name")
