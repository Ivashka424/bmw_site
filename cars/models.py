from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class CarSeries(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()
    logo = models.ImageField(upload_to='series_logos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Car Series"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('model_list') + f'?series={self.id}'

class CarModel(models.Model):
    BODY_TYPES = [
        ('SEDAN', 'Sedan'),
        ('COUPE', 'Coupe'),
        ('TOURING', 'Touring'),
        ('GRAN_COUPE', 'Gran Coupe'),
        ('SUV', 'SUV'),
    ]

    series = models.ForeignKey(
        CarSeries,
        on_delete=models.CASCADE,
        related_name='models'
    )
    model_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    generation = models.CharField(max_length=50)
    year_start = models.IntegerField()
    year_end = models.IntegerField(null=True, blank=True)
    body_type = models.CharField(max_length=20, choices=BODY_TYPES)
    engine_options = models.TextField()
    power_range = models.CharField(max_length=100)
    acceleration_0_100 = models.CharField(max_length=20)
    top_speed = models.CharField(max_length=20)
    fuel_consumption = models.CharField(max_length=50)
    price_range = models.CharField(max_length=100)
    description = models.TextField()
    main_image = models.ImageField(upload_to='car_images/')
    image_1 = models.ImageField(upload_to='car_images/', null=True, blank=True)
    image_2 = models.ImageField(upload_to='car_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['series', 'model_name', 'generation']

    def __str__(self):
        return f"BMW {self.series.name} {self.model_name} ({self.generation})"

    def get_absolute_url(self):
        return reverse('model_detail', args=[str(self.id)])

class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)
    date_published = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "News"
        ordering = ['-date_published']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.slug)])