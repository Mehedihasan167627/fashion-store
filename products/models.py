
import uuid
from django.utils.html import format_html
from django.db import models
from accounts.models import CustomUser
import ast 
from django.utils.text import slugify


# Create your models here.
class BaseModel(models.Model):
    slug=models.SlugField(unique=True,blank=True,null=True)
    updated=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract=True 


class Category(BaseModel):
    name=models.CharField(max_length=255,unique=True)
    slug=models.SlugField(unique=True,blank=True,null=True)

    def __str__(self) -> str:
        return self.name 

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        return super().save(*args,**kwargs)

class SubCategory(BaseModel):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=255,unique=True)
    slug=models.SlugField(blank=True,null=True)

    def __str__(self) -> str:
        return self.name 

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        return super().save(*args,**kwargs)


class Product(BaseModel):
    sub_category=models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    title=models.CharField(max_length=255,unique=True)
    thumbnail=models.ImageField(upload_to="media")
    price=models.PositiveBigIntegerField()
    discount_price=models.PositiveBigIntegerField(blank=True,null=True)
    description=models.TextField()
    MEN_OR_WOMEN=(("Men's","Men's"),("Women's","Women's"),("Kid's","Kid's"),("Everyone","Everyone"))
    men_or_women=models.CharField(max_length=8,choices=MEN_OR_WOMEN)
    is_active=models.BooleanField(default=True)
    sale_count=models.PositiveBigIntegerField(default=0)

    def __str__(self) -> str:
        return self.title 

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        return super().save(*args,**kwargs)


    def get_all_images(self):
        images=f"<img src='{self.thumbnail.url}' height='25' width='25' style='border-radius:50%;'> - "
        img_list=ProductImage.objects.filter(product__id=self.id)
        for img in img_list:
            images+=f"<img src='{str(img.image.url)}' height='25' width='25' style='border-radius:50%;'> - "
            
        return format_html(images)

    def multiple_image(self):
        img_list=ProductImage.objects.filter(product__id=self.id)
        images=[]
        for obj in img_list:
            images.append(obj.image.url)
        return images



class ProductImage(models.Model):
    product=models.ForeignKey(Product,related_name='product',on_delete=models.CASCADE)
    image=models.ImageField(upload_to="media")

    def __str__(self):
        return self.product.title


def create_random_code():
    code="ES-"+str(uuid.uuid4()).replace("-","").upper()[:10]
    order=Order.objects.filter(unique_id=code)
    while True:
        if order.exists():
            code="ES-"+str(uuid.uuid4()).replace("-","").upper()[:12]
        else:
            break
    return code 

class Order(models.Model):
    unique_id=models.CharField(max_length=12,default=create_random_code,blank=True,null=True)
    name_and_quantity=models.TextField()
    total=models.PositiveBigIntegerField()
    status=models.CharField(max_length=10,choices=(("Pending","Pending"),("Received","Received")),default="Pending")
    paid=models.BooleanField(default=False)
    order_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    updated=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.unique_id

    def save(self,*args,**kwargs):
        if self.status=="Received":
            self.paid=True 
        return super().save(*args,**kwargs)

    def product_list(self):
        text=ast.literal_eval(self.name_and_quantity)
        data=""
        for i in text:
           obj=Product.objects.get(id=i["id"])
           data+=f"<img src='{obj.thumbnail.url}' style='height:25px;weight:25px;border-radius:50%;'> {Product.objects.get(id=i['id']).title}( {i['quantity']} )<br>"
        return format_html(data)

    
    def customer_details(self):
        address=Address.objects.filter(order__id=self.id).last()
        detail=""
        detail+=f'<p>Name : {address.full_name}</p>'
        detail+=f'<p>Phone : {address.mobile}</p>'
        detail+=f'<p>Email : {address.email}</p>'
        detail+=f'<p>Address : {address.address},{address.city},{address.country}</p>'
        return format_html(detail)




class Address(models.Model):
    full_name=models.CharField(max_length=255)
    email=models.EmailField()
    mobile=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    zip_code=models.CharField(max_length=255)
    country=models.CharField(max_length=8,default="Bangladesh")
    address=models.CharField(max_length=255)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.full_name +" | "+self.email+" | "+self.mobile+" | "+self.address



class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    star=models.CharField(max_length=1,default="1",choices=(
        ("1","1"),("2","2"),
        ("3","3"),("4","4"),("5","5")))
    description=models.TextField()
    review_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.product.title

    @staticmethod
    def get_all_reviews(product_id):
        return Review.objects.filter(product__id=product_id)
