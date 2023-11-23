from django.contrib import admin

# Register your models here.
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    #Creo esta clase porque no quiero mostrar el slug ya que se va a generar automaticamente
    fields = ('title', 'description', 'products', 'image')
    #mostar en el administrador aparte del title que es el str, mostrar el slug y created_at
    list_display = ('__str__', 'slug', 'created_at')

admin.site.register(Category,CategoryAdmin )