from django import template
from products.models import Product
import ast 
from django.utils.html import format_html


register=template.Library()

@register.filter(name="currency")
def currency(price):
    return "৳"+str(price)


@register.filter(name="sub_cat_pro_count")
def sub_category_product_count(obj):
    count=Product.objects.filter(sub_category=obj).count()
    return count


@register.filter(name="show_discount_percentage")
def show_discount_percentage(cost_price,sale_price):
    loss=cost_price-sale_price
    loss=(loss/cost_price)*100
    if loss<1:
        loss=1 
    return str(int(loss))+'%off'


@register.filter(name="star_count")
def review_star_count(count):
    count=int(count)
    star=""
    if count==5:
        star='<ion-icon name="star"></ion-icon><ion-icon name="star"></ion-icon><ion-icon name="star"></ion-icon><ion-icon name="star"></ion-icon><ion-icon name="star"></ion-icon>'
    elif count==4:
        star='<ion-icon name="star"></ion-icon><ion-icon name="star"></ion-icon><ion-icon name="star"></ion-icon><ion-icon name="star"></ion-icon><ion-icon name="star-outline"></ion-icon>'
    elif count==3:
        star='<ion-icon name="star"></ion-icon><ion-icon name="star"></ion-icon><ion-icon name="star"></ion-icon><ion-icon name="star-outline"></ion-icon><ion-icon name="star-outline"></ion-icon>'     
    elif count==2:
        star='<ion-icon name="star"></ion-icon><ion-icon name="star"></ion-icon><ion-icon name="star-outline"></ion-icon><ion-icon name="star-outline"></ion-icon><ion-icon name="star-outline"></ion-icon>'
    elif count==1:
        star='<ion-icon name="star"></ion-icon><ion-icon name="star-outline"></ion-icon><ion-icon name="star-outline"></ion-icon><ion-icon name="star-outline"></ion-icon><ion-icon name="star-outline"></ion-icon>'  

    return format_html(star)