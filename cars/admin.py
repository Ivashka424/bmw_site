from django.contrib import admin
from .models import CarModel, News, CarSeries
from django.utils.html import format_html


class CarSeriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')


class CarModelAdmin(admin.ModelAdmin):
    list_display = (
        'model_name',
        'series',
        'generation',
        'year_start',
        'year_end',
        'is_featured',
        'image_preview'
    )
    list_filter = ('series', 'body_type', 'year_start', 'is_featured')
    search_fields = ('model_name', 'generation', 'series__name')
    prepopulated_fields = {'slug': ('model_name',)}
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    fieldsets = (
        ('Basic Info', {
            'fields': ('series', 'model_name', 'slug', 'generation', 'is_featured')
        }),
        ('Specifications', {
            'fields': (
                'body_type', 'year_start', 'year_end',
                'engine_options', 'power_range', 'acceleration_0_100',
                'top_speed', 'fuel_consumption', 'price_range'
            )
        }),
        ('Content', {
            'fields': ('description',)
        }),
        ('Images', {
            'fields': (
                'main_image', 'image_preview',
                'image_1', 'image_2'
            )
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def image_preview(self, obj):
        if obj.main_image:
            return format_html(
                '<img src="{}" style="max-height: 100px;"/>',
                obj.main_image.url
            )
        return "-"

    image_preview.short_description = 'Preview'


class NewsAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'date_published',
        'is_published',
        'image_preview'
    )
    list_filter = ('date_published', 'author', 'is_published')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date_published'
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px;"/>',
                obj.image.url
            )
        return "-"

    image_preview.short_description = 'Preview'


admin.site.register(CarSeries, CarSeriesAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(News, NewsAdmin)