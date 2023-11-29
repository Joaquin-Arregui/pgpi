from django.contrib import admin

from .models import Producer

class ProducerAdmin(admin.ModelAdmin):
    fields = ('title',)
    list_display = ('__str__', 'slug', 'created_at')

admin.site.register(Producer,ProducerAdmin)