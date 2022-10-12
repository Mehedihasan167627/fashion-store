from django.db.models.signals import pre_delete
from .models import Product, ProductImage
from django.dispatch import receiver







@receiver(pre_delete,sender=Product)
def delete_product_image(sender,instance,*args,**kwargs):
    if instance.thumbnail:
        instance.thumbnail.delete()


@receiver(pre_delete,sender=ProductImage)
def delete_product_image(sender,instance,*args,**kwargs):
    if instance.image:
        instance.image.delete()

