from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import LoginView, LogoutView, RegisterView


urlpatterns = [
    path('admin/', admin.site.urls),

    path("",include("pages.urls",namespace="pages")), 
    path("login/",LoginView.as_view(),name="login"),
    path("register/",RegisterView.as_view(),name="register"),
    path("logout/",LogoutView.as_view(),name="logout"),
]


urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

