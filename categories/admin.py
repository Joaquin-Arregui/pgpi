from django.contrib import admin

from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'products', 'image')
    list_display = ('__str__', 'slug', 'created_at')

admin.site.register(Category,CategoryAdmin )