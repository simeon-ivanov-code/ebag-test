from django.db import models
from pathlib import Path

class Category(models.Model):
    name = models.CharField(verbose_name='Name', max_length=100)
    parent = models.ForeignKey('self', verbose_name='Parent Category', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'categories'
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        if self.parent:
            return f'{self.parent} / {self.name}'
        return self.name


class Product(models.Model):
    title = models.CharField(verbose_name='Title', max_length=100)
    description = models.TextField(verbose_name='Description', max_length=4000)
    image = models.ImageField(verbose_name='Image', upload_to='products', null=True, blank=True)
    sku = models.CharField(verbose_name='SKU', max_length=20, unique=True)
    price = models.FloatField(verbose_name='Price')
    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'
        ordering = ['category__name', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        old_image = ''
        if self.id:
            product = Product.objects.get(id=self.id)
            if product.image:
                old_image = product.image.path
        super().save(*args, **kwargs)
        if (not self.image or old_image != self.image.path) and old_image:
            file = Path(old_image)
            if file.exists():
                file.unlink()

    def delete(self):
        if self.image:
            file = Path(self.image.path)
            if file.exists():
                file.unlink()
        super().delete()

class SearchRequest:
    title: str = ''
    sku: str = ''
    from_price: float = 0
    to_price: float = 0
    category: str = ''
    has_image: bool = True
