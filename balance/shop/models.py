from django.db import models
from django.urls import reverse
from imagekit.processors import Resize
from imagekit.models import ProcessedImageField


class ShoeSize(models.Model):
    size = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Размер обуви'
    )

    class Meta:
        verbose_name = 'Размер обуви'
        verbose_name_plural = 'Размеры обуви'

    def __str__(self):
        return str(self.size)


class Brand(models.Model):
    brand_name = models.CharField(
        max_length=50,
        verbose_name='Название бренда',
    )

    class Meta:
        verbose_name = 'Наименование бренда'
        verbose_name_plural = 'Наименования брендов'

    def __str__(self):
        return self.brand_name


class ProductModel(models.Model):
    model_name = models.CharField(
        max_length=50,
        verbose_name='Название модели',
    )

    class Meta:
        verbose_name = 'Наименование модели'
        verbose_name_plural = 'Наименования моделей'

    def __str__(self):
        return self.model_name


class ProductColor(models.Model):
    color_name = models.CharField(
        max_length=50,
        verbose_name='Цвет',
    )

    class Meta:
        verbose_name = 'Наименование цвета'
        verbose_name_plural = 'Наименования цветов'

    def __str__(self):
        return self.color_name


class ProductMaterial(models.Model):
    material_name = models.CharField(
        max_length=50,
        verbose_name='Материал',
    )

    class Meta:
        verbose_name = 'Наименование материала'
        verbose_name_plural = 'Наименования материалов'

    def __str__(self):
        return self.material_name


class Gender(models.Model):
    GENDER_CHOICES = (
        ('м', 'мужской'),
        ('ж', 'женский'),
        ('д', 'детский')
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
    )

    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Пол'

    def __str__(self):
        return self.gender


class ProductImage(models.Model):
    image = ProcessedImageField(
        upload_to='products/%Y/%m/%d',
        blank=True,
        processors=[Resize(width=800, height=600)],
        format='JPEG',
        options={'quality': 90},
        verbose_name='Изображение',
    )

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return f'Изображение товара {self.pk}'


class Category(models.Model):

    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Ссылка',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name='Категория',
    )
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Ссылка',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
    )

    size = models.ManyToManyField(
        ShoeSize,
        verbose_name='Размер',
    )

    brand = models.ManyToManyField(
        Brand,
        verbose_name='Бренд',
    )

    model = models.ManyToManyField(
        ProductModel,
        verbose_name='Модель',
    )

    color = models.ManyToManyField(
        ProductColor,
        verbose_name='Цвет',
    )

    material = models.ManyToManyField(
        ProductMaterial,
        verbose_name='Материал',
    )

    gender = models.ManyToManyField(
        Gender,
        verbose_name='Пол',
    )

    product_code = models.BigIntegerField(
        verbose_name='Код товара',
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена',
    )

    image = models.ManyToManyField(
        ProductImage,
        verbose_name='Изображения товара',
    )

    available = models.BooleanField(
        default=True,
        verbose_name='В наличии',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения',
    )

    class Meta:
        ordering = ('name', )
        index_together = (('id', 'slug'),)
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.pk, self.slug])