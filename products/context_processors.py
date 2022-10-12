import ast
from .models import Category,Product, SubCategory,Order 
import json 

def sub_category_list(request):
    sub_category_list=Category.objects.all()
    return {"sub_category_list":sub_category_list}


def men_sub_category(request):
    queryset=Product.objects.filter(men_or_women="Men's",is_active=True)
    ids=[i.sub_category.id for i in queryset]
    ids=list(set(ids))
    queryset=SubCategory.objects.filter(id__in=ids)
    return {"men_sub_category":queryset}

def women_sub_category(request):
    queryset=Product.objects.filter(men_or_women="Women's",is_active=True)
    ids=[i.sub_category.id for i in queryset]
    ids=list(set(ids))
    queryset=SubCategory.objects.filter(id__in=ids)
    return {"women_sub_category":queryset}

def kid_sub_category(request):
    queryset=Product.objects.filter(men_or_women="kid's")
    ids=[i.sub_category.id for i in queryset]
    ids=list(set(ids))
    queryset=SubCategory.objects.filter(id__in=ids)
    return {"kid_sub_category":queryset}


def best_sellers(request):
 
    queryset=Product.objects.filter(is_active=True).order_by("-id")[:4]
    return {"best_sellers":queryset}

