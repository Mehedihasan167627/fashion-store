from django.contrib import admin
from .models import* 


class SubCategoryAdmin(admin.StackedInline):
    model=SubCategory 
    exclude=["slug"]

class CategoryAdmin(admin.ModelAdmin):
    inlines=[SubCategoryAdmin]   
    exclude=["slug"]

admin.site.register(Category,CategoryAdmin)



class MultiImageAdmin(admin.StackedInline):
    model=ProductImage

class ProductModelAdmin(admin.ModelAdmin):
    inlines=[MultiImageAdmin]
    list_display=["title","get_all_images","price","discount_price","men_or_women","is_active"]
    list_editable=("is_active",)
    exclude=["slug"]




admin.site.register(Product,ProductModelAdmin)


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display=["unique_id",'customer_details',"product_list","total","paid","status"]
    list_editable=("paid","status")
    exclude=['unique_id']


admin.site.register(Address)
admin.site.register(Review)
