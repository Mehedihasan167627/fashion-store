import ast
from django.core.paginator import Paginator 

def currency():
    return "৳"

def html_path(folder,filename):
    return folder+"/"+filename+".html"

def string_to_list(text):
    queryset=ast.literal_eval(text)
    return queryset 



def make_paginator_list(queryset,cart,per_page_size,page_number):
        product_list=""
        ids=""
        if cart:  
            ids=list(cart.keys())

        product_list=[]
        for i in queryset:
            if i.slug in ids:
                product_list.append({
                    "id":i.id,"slug":i.slug,
                    "title":i.title,"image":i.thumbnail,
                    "price":i.price,"discount_price":i.discount_price,
                    "cart_quantity":cart.get(i.slug),
                    "sub_category":i.sub_category,"is_added_cart":True
                    })
            else:
                product_list.append({
                    "id":i.id,"slug":i.slug,
                    "title":i.title,"image":i.thumbnail,
                    "price":i.price,"discount_price":i.discount_price,
                    "sub_category":i.sub_category,"is_added_cart":False
                    })

        paginator = Paginator(product_list,per_page_size) # Show {perpagesize} products per page.
        
        if not page_number:
              page_number=1
        product_list = paginator.get_page(page_number)
        
        return product_list