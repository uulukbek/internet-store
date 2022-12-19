from django.contrib import admin
from django.db.models import Avg

from applications.product.models import Product, Image, Order




class ImageAdmin(admin.TabularInline):
    model = Image
    fields = ('image',)
    max_num = 10


class ProductAdmin(admin.ModelAdmin):
    list_display = [ 'id', 'rating', 'likes']
    inlines = [ImageAdmin]

    def likes(self, obj):
        return obj.likes.filter(like=True).count()


    def rating(self, obj):
        return obj.ratings.all().aggregate(Avg('rating'))['rating__avg']


admin.site.register(Product, ProductAdmin)
admin.site.register(Image)
admin.site.register(Order)