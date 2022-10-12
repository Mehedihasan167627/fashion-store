
from django.urls import path
from .views import*
from accounts.middlewares import customer_middleware
app_name="pages"
urlpatterns = [
       path("",HomeView.as_view(),name='home'),
       path("shop/",ProductListView.as_view(),name='product-list'),
       path("cart/",CartView.as_view(),name='cart'),
       path("checkout/",customer_middleware(CheckoutView.as_view()),name='checkout'),
       path("order/",customer_middleware(OrderView.as_view()),name='order'),
       path("product/detail-of-<slug:slug>/",ProductDetailView.as_view(),name='product-detail'),
       

       path("add-to-cart/",AddToCartView.as_view(),name="add-to-cart"),
       path("category/<slug:slug>/",SubCategoryView.as_view(),name="sub_category-list"),
       path("product/detail-of-<slug:slug>/review/",ProductReviewView.as_view(),name='product-review'),


       path("search-product/<str:query>/",get__names)
      
      

]

