
from django.http import  HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View
from products.forms import ProductReviewForm

from products.models import Order, Product ,Address, Review, SubCategory
from django.contrib import messages
from django.db.models import Q 
from .utils import*
from django.core.paginator import Paginator

#0  for cartView and AddToCartView classes
def cart_obj_and_total(cart):
    ids=list(cart.keys())
    obj_list=Product.objects.filter(slug__in=ids,is_active=True)
    product_list=[]
    for i in obj_list:
        if i.discount_price:sub_total=i.discount_price
        else:sub_total=i.price
        data={
            "id":i.id,"slug":i.slug,"title":i.title,"image":i.thumbnail,
            "price":i.price,"discount_price":i.discount_price,
            "cart_quantity":cart.get(i.slug),
            "sub_total":sub_total*int(cart.get(i.slug))
        }
        product_list.append(data) 

    sum=0
    for i in product_list:
        sum+=i["sub_total"]

    return product_list,sum 

#00 index page
class HomeView(View):
    def get(self,request):
        return redirect("pages:product-list")
        
        sub_cat=SubCategory.objects.all()
        context={
            "sub_cat":sub_cat,
        }
        return render(request,html_path("pages","index"),context)

#1 show all products
class ProductListView(View):
    def get(self,request):
        cart=request.session.get("cart")
        if request.GET.get("qry"):
            queryset=Product.objects.filter(Q(title__icontains=request.GET.get("qry")))
        else:
            queryset=Product.objects.filter(is_active=True).order_by("-id")
        page_number=request.GET.get("page")
        # get code from custom utils file
        product_list=make_paginator_list(queryset,cart,8,page_number)
        

        context={
            "obj_list":product_list
        }
        return render(request,html_path("pages","product"),context)

#2 show all products by categories
class SubCategoryView(View):
  def get(self,request,slug):
        cart=request.session.get("cart")
        queryset=Product.objects.filter(sub_category__slug=slug,is_active=True).order_by("-id")
        page_number=request.GET.get("page")
        # get code from custom utils file
        product_list=make_paginator_list(queryset,cart,8,page_number)
        
       
        context={
            "obj_list":product_list,
            "sub_category":slug
        }
        return render(request,html_path("pages","product"),context)

#3  show product details
class ProductDetailView(View):
    def get(self,request,slug):
        review_list=""
        try:
            obj=Product.objects.get(slug=slug,is_active=True)
            review_list=Review.get_all_reviews(obj.id).order_by("-id")
        except:
            return HttpResponse("invalid url")
        page_number=request.GET.get("page")
        # get code from custom utils file
        paginator = Paginator(review_list,4) # Show {perpagesize} products per page.
        
        if not page_number:
              page_number=1
        review_list = paginator.get_page(page_number)
        
        context={
            "obj":obj,
            "review_list":review_list
           
        }
        return render(request,html_path("pages","product-detail"),context)


#4 show all sessions cart items
class CartView(View):
    def get(self,request):
        cart=request.session.get("cart")
        product_list=""
        sum=0
        if cart:
            product_list,sum=cart_obj_and_total(cart)
        context={
            "obj_list":product_list,
            "total_price":float(sum)
        }
        return render(request,html_path("pages","cart"),context)
    


class CheckoutView(View):
    def get(self,request):
        cart=request.session.get("cart")
        length=0
        if cart:
            length=len(list(cart))
        if length<1:
            messages.warning(request,"Please add some product in your cart")
            return redirect("pages:cart")
        
        sum=0
        if cart:
            _,sum=cart_obj_and_total(cart)
        context={
            "total_price":float(sum)
        }
        return render(request,html_path("pages","checkout"),context)
    def post(self,request):
        if not request.user.is_authenticated:
            return redirect("/login/?return_url=/checkout/")
        cart=request.session.get("cart")
        if not cart:
            messages.success(request,"Please add some product in your cart")
            return redirect("pages:product-list")   

        product_list,sum=cart_obj_and_total(cart)
        post_data=[]
        for obj in product_list:
            if obj["discount_price"]:
                data={
                    "id":obj["id"],
                    "title":obj["title"],
                    "image":obj["image"].url,
                    "price":float(obj["discount_price"]),
                    "quantity":obj["cart_quantity"],
                     "sub_total":float(obj["sub_total"]), 
                    }
                post_data.append(data)
            else:
                data={
                    "id":obj["id"],
                    "title":obj["title"],
                    "image":obj["image"].url,
                    "price":float(obj["price"]),
                    "quantity":obj["cart_quantity"], 
                    "sub_total":float(obj["sub_total"]), 

                    }
                post_data.append(data)
            
        
        order=Order(name_and_quantity=str(post_data),total=sum,order_by=request.user)
        order.save()
        addr=Address(
                    full_name=request.POST.get("full_name"),
                    email=request.POST.get("email"),
                    mobile=request.POST.get("mobile"),
                    city=request.POST.get("city"),
                    zip_code=request.POST.get("zip_code"),
                    country=request.POST.get("country"),
                    address=request.POST.get("address"),
                    order=order,

            )
        addr.save()
        if order and addr:
            request.session["cart"]=""
            product_list=""
            messages.success(request,"Your Order placed Successfully!!!")
            return redirect("pages:order")

        context={
            "total_price":sum
        }
        return render(request,html_path("pages","checkout"),context)
#5 show all unique user orders
class OrderView(View):
    def get(self,request):
        queryset=Order.objects.filter(order_by=request.user).order_by("-created_at")
        obj_list=[]
        for obj in queryset:
            obj_list.append({
                "order_id":obj.unique_id,
                "results":string_to_list(obj.name_and_quantity),
                "total":float(obj.total),"paid":obj.paid,
                "created_at":obj.created_at, 
                "updated_at":obj.updated, 
                 })
        return render(request,html_path("pages","order"),{"obj_list":obj_list})


#6 cart items add,remove,increase quantityand dicreease quantity 
class AddToCartView(View):
    def post(self,request):
        cart=request.session.get("cart")
        slug= request.POST.get("slug")
        sender=request.POST.get("sender")

        if not cart:
            cart={}
            
        if sender=="detail_page":
            quantity=request.POST.get("quantity")
            ex_quanity=cart.get(slug)
            if ex_quanity:
                cart[slug]=int(ex_quanity)+int(quantity)
            else:
                cart[slug]=int(quantity)
        elif sender=='increase':
            ex_quanity=cart.get(slug)
            cart[slug]=int(ex_quanity)+1
        elif sender=="dicrease":
            ex_quanity=cart.get(slug)
            if ex_quanity >1:
                cart[slug]=int(ex_quanity)-1
        elif sender=="remove":
            cart.pop(slug)

        request.session["cart"]=cart 
        _,sum=cart_obj_and_total(cart)
        product=Product.objects.get(slug=slug,is_active=True)
        return JsonResponse(
            {
                "slug":product.title,
                "quantity":cart.get(slug),
                "item_count":len(cart),
                "total_price":currency()+str(float(sum))
            }
        )



class ProductReviewView(View):
    def get(self,request,slug):
        if not request.user.is_authenticated:
            messages.warning(request,"Please login your account")
            return redirect(f"/login/?return_url=/product/detail-of-{slug}/review")
        try:
            product=Product.objects.get(slug=slug)
        except:
            return HttpResponse("invalid url")
        
        context={
            "form":ProductReviewForm(),
            "obj":product
        }
        return render(request,html_path("pages","review"),context)


    def post(self,request,slug):
        try:
            product=Product.objects.get(slug=slug)
        except:
            return HttpResponse("invalid url")
        form=ProductReviewForm(request.POST or None)

        if form.is_valid():
            review=form.save(commit=False)
            review.product=product 
            review.review_by=request.user 
            review.save()
            return redirect(f"/product/detail-of-{slug}?#review")
        
        context={
            "form":ProductReviewForm(),
            "obj":product
        }
        return render(request,html_path("pages","review"),context)




def get__names(request,query):
    data=[]
    objs=Product.objects.filter(title__istartswith=query) 

    for i in objs:
        data.append({"title":i.title,"slug":i.slug})
    
    return JsonResponse({"payload":data})

