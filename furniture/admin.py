from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . import models
# Register your models here.


class GalleryAdmin(admin.TabularInline):
    list_display=["id","product"]
    model = models.Gallery

class ProductAdmin(admin.ModelAdmin):
    list_display=["id","name","price"]
    inlines=[GalleryAdmin]

admin.site.register(models.Product,ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','title','parent']

admin.site.register(models.Categories,CategoryAdmin)
admin.site.register(models.CartItem)
admin.site.register(models.Customer)
